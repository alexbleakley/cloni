# Constraining language models outputs with negated instructions (CLONI)

This repository contains the code, data, and results from my exploration of how well langauge models respond to negated instructions that constrain their responses. I summarized my experiment and the key findings in a [blog post](https://alexbleakley.com/blog/saying-what-not-to-do).

## Results

The results directory contains the responses, evaluations ("results"), and summaries for each tested model for each of the 10 task types.

## Reproducing and extending the results

### Setup
1. Install the requirements from `requirements.txt` into an active python environment.
1. Copy `.env.template` to `.env` and replace `<your API key>` with your API key for each model provider.

### Reproducing the results
1. Delete the `data`, `figures`, and `results` directories and their contents.
1. Run `run-all.sh`.

### Evaluating a different model
1. If the model comes from a provider other than AI21, Anthropic, Cohere, or OpenAI, or is running in a local environment, add a new completion function to `cloni/completions.py` and add it to the `generate_completion` function of that module.
1. Add the model provider and name to `cloni/models.py`. 
1. Run `python3 -m cloni.evaluate`.

## Questions and feedback 
If you have questions or feedback, please communicate with me through GitHub Issues or use the contact form on [my website](https://alexbleakley.com).