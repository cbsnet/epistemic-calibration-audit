#!/usr/bin/env bash
set -euo pipefail

echo "1. Installing dependencies..."
pip install -e ".[dev]"

echo "2. Running experiment..."
python scripts/run_experiment.py

echo "3. Analysis..."
jupyter nbconvert --execute notebooks/02_analysis.ipynb --to html --output-dir reports/

echo "Done. See reports/."