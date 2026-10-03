## Reading order

- 30 seconds: this file, section "The finding in one sentence".
- 2 minutes: README.md, sections Abstract + Key results.
- 10 minutes: FOR_REVIEWERS.md in full + reports/summary.md.
- 30 minutes: the whole repo, including scripts and raw data.

# For Reviewers

If you have 5 minutes, read this file. It contains everything you need to
decide whether this project is worth a closer look, and how to verify it if
you want to.

## What this is

A 1–2 week pilot audit of a frontier LLM's epistemic robustness under three
types of pressure. 20 questions × 4 conditions × 1 model = 80 responses,
fully analyzed. The finding is small but clean and statistically significant
after correction.

## The finding in one sentence

`openai/gpt-oss-120b` is chronically overconfident (99.95% mean confidence,
85% accuracy in neutral), fully resistant to social pressure (p = 1.0), and
significantly destabilized by authority pressure (accuracy 55%, p = 0.043)
and by plausible false context (accuracy 45%, p = 0.014) — while its
verbalized confidence stays far above what accuracy justifies in every
condition.

## What to check, in order

1. **The headline number.** `reports/summary.csv` line 3: neutral accuracy
   0.85, mean confidence 0.9995.
2. **The strongest effect.** `reports/paired_tests.csv` line 3:
   misleading_context, p_bonferroni = 0.014, r = 0.63.
3. **The figure.** `reports/figures/reliability_by_condition.png`: the
   neutral curve hugs the top of the plot while accuracy sits at 0.85.
4. **The raw data.** `data/results/raw.jsonl`: 80 lines, one per response,
   with the full prompt and the model's raw output.

## Verify in 5 minutes

If you want to reproduce the analysis without re-querying the API:

    pip install -r requirements.txt
    python scripts/analysis.py

Expected output: the summary table and paired tests shown in `README.md`.
Figures are written to `reports/figures/`.

To reproduce the full experiment (including API calls, ~15 min, ~$0.05):

    export GROQ_API_KEY=...
    python scripts/run_experiment.py
    python scripts/analysis.py

## What this project does NOT claim

- Not a general claim about "LLMs". One model, one run per question.
- Not a measure of internal uncertainty. Verbalized confidence only.
- Not a multi-turn adversarial evaluation. Single-turn pressure prompts.
- Not a benchmark. 20 questions is a pilot, not a leaderboard.

## What a skeptical reviewer should ask

- *Does the effect survive Bonferroni?* Yes. See `reports/paired_tests.csv`.
- *Is the parser cherry-picking successes?* No. Parsing failures: 0/80. See
  `scripts/diagnose.py`.
- *Is the model just guessing?* No. Neutral accuracy is 0.85, well above
  chance on this question set.
- *Why one model?* Scoped as a pilot. Cross-model replication is stated as
  next work in `README.md` § Limitations.

## Time and cost

- Development: ~2 weeks part-time.
- API cost: under $0.10 for the full run.
- Reproduction: 5 minutes for analysis only, 15 minutes including API calls.

## Contact

## Repository

https://github.com/cbsnet/epistemic-calibration-audit