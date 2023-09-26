import json
import os
from typing import List

import regex as re

from cloni.completions import generate_completion
from cloni.prepare_data import CLONI_PROMPTS_PATH, CLONI_CONSTRAINTS_PATH
from cloni.models import MODELS
from cloni.tasks import Task, TASKS


CLONI_RESULTS_ROOT = "results/"
CLONI_RESPONSES_PATH = "results/{provider}_{model}/{task.task_id:02}_{task.short_name}/responses_{prompt_type}.jsonl"
CLONI_RESULTS_PATH = "results/{provider}_{model}/{task.task_id:02}_{task.short_name}/results_{prompt_type}.jsonl"
CLONI_TASK_SUMMARY_PATH = "results/{provider}_{model}/{task.task_id:02}_{task.short_name}/summary_{prompt_type}.jsonl"
CLONI_MODEL_SUMMARY_PATH = "results/{provider}_{model}/summary.jsonl"
CLONI_ALL_MODEL_PERFORMANCE_PATH = "results/summary_all-models.csv"


def get_responses(provider: str, model: str, task: Task, prompt_type: str):
    prompts_file_path = CLONI_PROMPTS_PATH.format(**vars())
    responses_file_path = CLONI_RESPONSES_PATH.format(**vars())
    os.makedirs(os.path.dirname(responses_file_path), exist_ok=True)
    with open(prompts_file_path) as prompts_file, open(responses_file_path, "a+") as responses_file:
        responses_file.seek(0)
        for prompt_line in prompts_file:
            response_line = responses_file.readline()
            if not response_line:
                q = json.loads(prompt_line)
                q["response"] = generate_completion(q["prompt"], provider, model, temperature=0, max_tokens=256)
                responses_file.write(json.dumps(q) + "\n")
    return


def evaluate_response(response_text: str, constraint_regex: str) -> int:
    pattern = re.compile(constraint_regex)
    if pattern.search(response_text):
        return 1
    else:
        return 0


def evaluate_responses(provider: str, model: str, task: Task, prompt_type: str):
    responses_file_path = CLONI_RESPONSES_PATH.format(**vars())
    constraints_file_path = CLONI_CONSTRAINTS_PATH.format(**vars())
    results_file_path = CLONI_RESULTS_PATH.format(**vars())
    with open(responses_file_path) as responses_file, \
        open(constraints_file_path) as constraints_file, \
        open(results_file_path, 'w') as results_file:
        for line in responses_file:
            question = json.loads(line)
            constraint_regex = json.loads(constraints_file.readline())["constraint_regex"]
            question["constraint_regex"] = constraint_regex
            question["result"] = evaluate_response(question["response"], constraint_regex)
            results_file.write(json.dumps(question) + "\n")
    return


def summarize_task_results(provider: str, model: str, task: Task, prompt_type: str):
    results_file_path = CLONI_RESULTS_PATH.format(**vars())
    summary_file_path = CLONI_TASK_SUMMARY_PATH.format(**vars())
    question_count = 0
    correct_count = 0
    with open(results_file_path) as results_file:
        for line in results_file:
            q = json.loads(line)
            question_count += 1
            correct_count += q["result"]
    results_summary = {
        "question_count": question_count,
        "correct_count": correct_count
    }
    with open(summary_file_path, 'w') as summary_file:
        summary_file.write(json.dumps(results_summary))
    return


def evaluate_task(provider: str, model: str, task: Task, prompt_types: List[str] = ["affirmative", "negated"]):
    for prompt_type in prompt_types:
        summary_file_path = CLONI_TASK_SUMMARY_PATH.format(**vars())
        # Check if task has already been evaluated
        if not os.path.isfile(summary_file_path):
            get_responses(provider, model, task, prompt_type)
            evaluate_responses(provider, model, task, prompt_type)
            summarize_task_results(provider, model, task, prompt_type)
    return


def summarize_model_results(provider: str, model: str, prompt_types: List[str] = ["affirmative", "negated"]):
    model_summary_file_path = CLONI_MODEL_SUMMARY_PATH.format(**vars())
    model_totals = {
        "task_id": "totals",
        "question_count": 0,
    }
    for prompt_type in prompt_types:
        model_totals[prompt_type + "_correct_count"] = 0
    with open(model_summary_file_path, 'w') as totals_file:
        for task in TASKS:
            new_task_summary = {"task_id": task.task_id}
            for prompt_type in prompt_types:
                task_summary_file_path = CLONI_TASK_SUMMARY_PATH.format(**vars())
                with open(task_summary_file_path) as task_summary_file:
                    task_summary = json.loads(task_summary_file.readline())
                    if "question_count" in new_task_summary:
                        if not new_task_summary["question_count"] == task_summary["question_count"]:
                            raise ValueError(f"Inconsistent question count for task id {task.task_id}")
                    else:
                        new_task_summary["question_count"] = task_summary["question_count"]
                        model_totals["question_count"] += task_summary["question_count"]
                    new_task_summary[prompt_type + "_correct_count"] = task_summary["correct_count"]
                    model_totals[prompt_type + "_correct_count"] += task_summary["correct_count"]
            totals_file.write(json.dumps(new_task_summary) + "\n")
        totals_file.write(json.dumps(model_totals) + "\n")       
    return


def evaluate_model(provider: str, model: str, prompt_types: List[str] = ["affirmative", "negated"]):
    model_summary_file_path = CLONI_MODEL_SUMMARY_PATH.format(**vars())
    # Check if model has already been evaluated
    if not os.path.isfile(model_summary_file_path):
        for task in TASKS:
            evaluate_task(provider, model, task, prompt_types)
        summarize_model_results(provider, model, prompt_types)
    return


def create_all_models_summary_csv():
    csv_file_path = CLONI_ALL_MODEL_PERFORMANCE_PATH
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(
            "provider, model, affirmative_correct_ratio, negated_correct_ratio, negation_understanding_ratio\n"
        )
        for model in MODELS:
            provider, model = model.provider, model.model
            model_summary_path = CLONI_MODEL_SUMMARY_PATH.format(**vars())
            if os.path.isfile(model_summary_path):
                with open(model_summary_path) as model_summary_file:
                    for line in model_summary_file:
                        task_summary = json.loads(line)
                        if task_summary["task_id"] == "totals":
                            affirmative_correct_ratio = (
                                task_summary["affirmative_correct_count"] / task_summary["question_count"]
                            )
                            negated_correct_ratio = (
                                task_summary["negated_correct_count"] / task_summary["question_count"]
                            )
                            negation_understanding_ratio = (
                                task_summary["negated_correct_count"] / task_summary["affirmative_correct_count"]
                            )
                            csv_file.write(
                                f"{provider}, {model}, {affirmative_correct_ratio}, {negated_correct_ratio}, "
                                f"{negation_understanding_ratio}\n"
                            )


if __name__ == "__main__":
    all_model_performance_file_path = CLONI_ALL_MODEL_PERFORMANCE_PATH
    new_model = False
    for model in MODELS:
        provider, model = model.provider, model.model
        model_summary_file_path = CLONI_MODEL_SUMMARY_PATH.format(**vars())
        # Check if model has already been evaluated, else evaluate it
        if not os.path.isfile(model_summary_file_path):    
            evaluate_model(provider, model)
            new_model = True
    # If any new model added, recreate all-model performance csv
    if new_model:
        if os.path.isfile(all_model_performance_file_path):
            os.remove(all_model_performance_file_path)
        create_all_models_summary_csv()