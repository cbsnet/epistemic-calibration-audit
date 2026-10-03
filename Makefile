.PHONY: install run analysis reproduce clean

install:
	pip install -e ".[dev]"

run:
	python scripts/run_experiment.py

analysis:
	jupyter nbconvert --execute notebooks/02_analysis.ipynb --to html --output-dir reports/

reproduce: install run analysis
	@echo "Reproduction complete. See reports/."

clean:
	rm -rf data/results/*.jsonl reports/*.html