# Constraining language models outputs with negated instructions (CLONI)

This repository contains the code, data, and results from my exploration of how well langauge models respond to negated instructions that constrain their responses. A [blog post detailing my findings](TODO) is available on TBD.

To reproduce my results, delete the `data`, `figures`, and `results` directories and their contents, install the requirements from `requirements.txt` into an active python environment, and then run `run-all.sh`.

To run the CLONI benchmark against a different model, add the model name to `cloni/models.py` and then run `python3 -m cloni.evaluate`. If the model comes from a provider other than AI21, Anthropic, Cohere, or OpenAI, or is running in a local environment, you will also need to add a new completion function to `cloni/completions.py`.

If you have questions or feedback, please communicate with me through GitHub Issues.