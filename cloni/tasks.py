from typing import NamedTuple


Task = NamedTuple(
    "Task", 
    [
        ("task_id", int), 
        ("short_name", str),
        ("instruction", str),
        ("constraint_affirmative", str),
        ("constraint_negated", str),
        ("constraint_regex", str)
    ]
)


TASKS = [
    Task(
        task_id = 1,
        short_name = "no-uppercase-letters",
        instruction = "Answer the question and provide an explanation.",
        constraint_affirmative = "Use only lowercase letters in your response.",
        constraint_negated = "Do not use uppercase letters in your response.",
        constraint_regex = "^\P{{Lu}}*+$"
    ),
    Task(
        task_id = 2,
        short_name = "no-lowercase-letters",
        instruction = "Answer the question and provide an explanation.",
        constraint_affirmative = "Use only uppercase letters in your response.",
        constraint_negated = "Do not use lowercase letters in your response.",
        constraint_regex = "^\P{{Ll}}*+$"
    ),
    Task(
        task_id = 3,
        short_name = "max-words",
        instruction = "Answer the question and provide an explanation.",
        constraint_affirmative = "Use at most 20 words in your response.",
        constraint_negated = "Do not use more than 20 words in your response.",
        constraint_regex = "^\W*+(\w++\W*+){{0,20}}+$"
    ),
    Task(
        task_id = 4,
        short_name = "min-words",
        instruction = "Answer the question and provide an explanation.",
        constraint_affirmative = "Use at least 100 words in your response.",
        constraint_negated = "Do not use fewer than 100 words in your response.",
        constraint_regex = "^\W*+(\w++\W*+){{100,}}+$"
    ),
    Task(
        task_id = 5,
        short_name = "short-words-only",
        instruction = "Answer the question and provide an explanation.",
        constraint_affirmative = "Use only words with at most 5 letters in your response.",
        constraint_negated = "Do not use any words longer than 5 letters in your response.",
        constraint_regex = "^\W*+(\\b\w{{1,5}}+\W*+)*+$"
    ),
    Task(
        task_id = 6,
        short_name = "answer-letter-only",
        instruction = "Answer the question.",
        constraint_affirmative = "Include only the letter corresponding to the correct answer in your response.",
        constraint_negated = (
            "Do not include anything except the letter corresponding to the correct answer in your response."
        ),
        constraint_regex = "^\W*{correct_choice}\W*+$"
    ),
    Task(
        task_id = 7,
        short_name = "exact-words-only",
        instruction = "Help the user answer the question.",
        constraint_affirmative = (
            "Include only the text \"Let's work through this together. What ideas do you have about this question?\" "
            "in your response."
        ),
        constraint_negated = (
            "Do not include anything except the text "
            "\"Let's work through this together. What ideas do you have about this question?\" "
            "in your response."
        ),
        constraint_regex = "^\W*Let's work through this together\. What ideas do you have about this question\?\W*+$"
    ),
    Task(
        task_id = 8,
        short_name = "start-with-exact-words",
        instruction = "Answer the question and provide an explanation.",
        constraint_affirmative = "Start your response with the exact text \"Let's think step by step.\"",
        constraint_negated = (
            "Do not start your response with anything except the exact text \"Let's think step by step.\""
        ),
        constraint_regex = "^\W*Let's think step by step\."
    ),
    Task(
        task_id = 9,
        short_name = "end-with-exact-words",
        instruction = "Answer the question and provide an explanation.",
        constraint_affirmative = "End your response with the exact text \"Does that make sense?\"",
        constraint_negated = "Do not end your response with anything except the exact text \"Does that make sense?\"",
        constraint_regex = "Does that make sense\?\W*+$"
    ),
    Task(
        task_id = 10,
        short_name = "only-exclamation-marks-for-punctuation",
        instruction = "Answer the question and provide an explanation.",
        constraint_affirmative = "Use only exclamation marks for punctuation.",
        constraint_negated = "Do not use anything except exclamation marks for punctuation.",
        constraint_regex = "^(\P{{P}}|\!)*+$"
    )
]