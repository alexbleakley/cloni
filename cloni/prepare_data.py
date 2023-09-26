import csv
import json
import os
from typing import List

from cloni.tasks import Task, TASKS


MMLU_TEST_PATH = "data/mmlu/data/test/"
CLONI_QUESTIONS_PATH = "data/cloni/questions.jsonl"
CLONI_PROMPTS_PATH = "data/cloni/{task.task_id:02}_{task.short_name}/prompts_{prompt_type}.jsonl"
CLONI_CONSTRAINTS_PATH = "data/cloni/{task.task_id:02}_{task.short_name}/response-constraints.jsonl"

MMLU_CHOICES = ["A", "B", "C", "D"]


def create_prompt(task: Task, question: dict, format: str) -> str:
    """Create a formatted prompt for a specific task and question."""
    if format == "affirmative":
        constraint = task.constraint_affirmative
    elif format == "negated":
        constraint = task.constraint_negated
    else:
        raise NotImplementedError(f"Constraint format {format} not supported.")
    if task.short_name == "answer-letter-only": 
        answer_text = f"{question['correct_answer']}"
    else:
        answer_text = f"{question['correct_choice']}. {question['correct_answer']}" 
    prompt = (
        f"Question: {question['question_text']}\n"
        + "\n".join([f"{choice}. {answer}" for choice, answer in zip(MMLU_CHOICES, question["answers"])]) +
        "\n\n"
        f"Instruction: The correct answer to the question is "
        f"\"{answer_text}\". "
        f"{task.instruction} {constraint}"
        "\n\n"
        "Answer:"
    )
    return prompt


def prepare_questions():
    """Select the first two questions from each MMLU topic and save to questions file."""
    questions = []
    question_id = 1
    mmlu_test_dir = os.fsencode(MMLU_TEST_PATH)
    for file in os.listdir(mmlu_test_dir):
        file_path = os.fsdecode(file)
        with open(MMLU_TEST_PATH + file_path) as questions_csv:
            questions_reader = csv.reader(questions_csv, delimiter=',', quotechar='"')
            for _ in range(2):
                question = dict()
                question_text, A, B, C, D, correct_choice = next(questions_reader)
                answers = [A, B, C, D]
                question["question_id"] = question_id
                question["question_text"] = question_text
                question["answers"] = answers
                question["correct_choice"] = correct_choice
                question["correct_answer"] = dict(zip(MMLU_CHOICES, answers))[correct_choice]
                questions.append(question)
                question_id += 1
    os.makedirs(os.path.dirname(CLONI_QUESTIONS_PATH), exist_ok=True)
    with open(CLONI_QUESTIONS_PATH, "w") as f:
        for question in questions:
            f.write(json.dumps(question) + "\n")
    return


def prepare_prompts(prompt_types: List[str] = ["affirmative", "negated"]):
    """Create formatted prompts and write to prompts files, for each task."""
    with open(CLONI_QUESTIONS_PATH) as questions_file:
        questions = []
        for line in questions_file:
            question = json.loads(line)
            questions.append(question)
    for task in TASKS:
        for prompt_type in prompt_types:
            prompts = []
            for question in questions:
                question_id = question["question_id"]
                prompt_text = create_prompt(task, question, prompt_type)
                prompt = dict(
                    task_id=task.task_id,
                    question_id=question_id,
                    prompt_type=prompt_type,
                    prompt=prompt_text
                )
                prompts.append(prompt)
            prompts_file_path = CLONI_PROMPTS_PATH.format(**vars())
            os.makedirs(os.path.dirname(prompts_file_path), exist_ok=True)
            with open(prompts_file_path, "w") as questions_file:
                for prompt in prompts:
                    questions_file.write(json.dumps(prompt) + "\n")
    return


def prepare_constraints():
    """Create response constraints and write to constraints files, for each task."""
    with open(CLONI_QUESTIONS_PATH) as questions_file:
        questions = []
        for line in questions_file:
            question = json.loads(line)
            questions.append(question)
    for task in TASKS:
        constraints = []
        for question in questions:
            question_id = question["question_id"]
            constraint_regex = task.constraint_regex.format(correct_choice=question["correct_choice"])
            constraint = dict(
                task_id=task.task_id,
                question_id=question_id,
                constraint_regex=constraint_regex
            ) 
            constraints.append(constraint)
        constraints_file_path = CLONI_CONSTRAINTS_PATH.format(**vars())
        with open(constraints_file_path, "w") as questions_file:
            for constraint in constraints:
                questions_file.write(json.dumps(constraint) + "\n")
    return


def prepare_data(prompt_types: List[str] = ["affirmative", "negated"]):
    """Use questions from MMLU and tasks from tasks.py to create the CLONI test set."""
    prepare_questions()
    prepare_prompts(prompt_types)
    prepare_constraints()
    return


if __name__ == "__main__":
    prepare_data()