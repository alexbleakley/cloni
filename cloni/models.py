from typing import NamedTuple


Model = NamedTuple(
    "Model", 
    [
        ("provider", str), 
        ("model", str)
    ]
)

MODELS = [
    Model(
        provider = "ai21",
        model = "j2-mid"
    ),
    Model(
        provider = "ai21",
        model = "j2-ultra"
    ),
    Model(
        provider = "anthropic",
        model = "claude-1.3"
    ),
    Model(
        provider = "anthropic",
        model = "claude-2.0"
    ),
    Model(
        provider = "cohere",
        model = "command"
    ),
    Model(
        provider = "cohere",
        model = "command-light"
    ),
    Model(
        provider = "openai",
        model = "text-ada-001"
    ),
    Model(
        provider = "openai",
        model = "text-babbage-001"
    ),
    Model(
        provider = "openai",
        model = "text-curie-001"
    ),
    Model(
        provider = "openai",
        model = "text-davinci-001"
    ),
    Model(
        provider = "openai",
        model = "text-davinci-002"
    ),
    Model(
        provider = "openai",
        model = "text-davinci-003"
    ),
    Model(
        provider = "openai",
        model = "gpt-3.5-turbo-0613"
    ),
    Model(
        provider = "openai",
        model = "gpt-4-0613"
    ),
]