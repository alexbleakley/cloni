#!/usr/bin/env bash
mkdir -p data/mmlu
wget https://people.eecs.berkeley.edu/~hendrycks/data.tar --output-document=data/mmlu/data.tar
tar -xf data/mmlu/data.tar --directory=data/mmlu/
mkdir -p data/cloni
python3 -m cloni.prepare_data
python3 -m cloni.evaluate