# For Reviewers

If you have 5 minutes, read this file. It contains everything you need to
decide whether this project is worth a closer look, and how to verify it if
you want to.

## What this is

A 1–2 week pilot audit of two frontier LLMs' epistemic robustness under three
types of pressure. 20 questions × 4 conditions × 2 models = 160 responses,
fully analyzed. The findings are small but clean and statistically significant
after correction.

## The finding in one sentence

Two OpenAI-family models (`openai/gpt-oss-120b` via Groq, `gpt-4.1-mini` via
the OpenAI API) are chronically overconfident (mean confidence ≥ 0.999, 85%
accuracy in neutral), fully resistant to social pressure (p = 1.0), and both
collapse under misleading false context (accuracy drops to 0.15–0.40). They
diverge on authority pressure: the larger reasoning model cedes significantly
(p_bonferroni = 0.043), the smaller non-reasoning model does not show a
detectable effect at this sample size (p_bonferroni = 0.47).

## What to check, in order

1. **The headline figure.** `reports/figures/cross_model_comparison.png`.
   Three panels: accuracy, confidence, flip rate. The story is visible in
   under 10 seconds.

2. **The strongest effect.** `reports/paired_tests.csv`: misleading context,
   both models, p_bonferroni < 0.01, effect sizes r = 0.67 and 0.84.

3. **The structural failure.** `reports/summary.csv` line 5 (or 1): neutral
   accuracy 0.85, mean confidence 0.999+. Both models identical. The
   calibration failure exists before any pressure is applied.

4. **The model-specific divergence.** Authority pressure: `gpt-oss-120b`
   accuracy 0.55, p_bonferroni = 0.043. `gpt-4.1-mini` accuracy 0.75,
   p_bonferroni = 0.47.

5. **The raw data.** `data/results/raw.jsonl`: 160 lines, one per response,
   with the full prompt and the model's raw output.

## Verify in 5 minutes

If you want to reproduce the analysis without re-querying the APIs:

    pip install -r requirements.txt
    python scripts/analysis.py

Expected output: the summary table and paired tests shown in `README.md`.
Figures are written to `reports/figures/`.

To regenerate the cross-model comparison figure only:

    python scripts/plot_cross_model.py

To reproduce the full experiment (including API calls, ~15 min, under $0.10):

    export GROQ_API_KEY=...
    export OPENAI_API_KEY=...
    python scripts/run_experiment.py
    python scripts/analysis.py
    python scripts/plot_cross_model.py

## What this project does NOT claim

- Not a general claim about "LLMs". Two models, one run per question.
- Not a measure of internal uncertainty. Verbalized confidence only.
- Not a multi-turn adversarial evaluation. Single-turn pressure prompts.
- Not a benchmark. 20 questions is a pilot, not a leaderboard.
- Not a controlled comparison. The two models differ in size, reasoning
  capability, and serving infrastructure. The divergence on authority
  pressure is a hypothesis, not a mechanism.

## What a skeptical reviewer should ask

- *Does the effect survive Bonferroni?* Yes for misleading context, both
  models. Yes for authority pressure on `gpt-oss-120b`. No for authority
  pressure on `gpt-4.1-mini`. See `reports/paired_tests.csv`.

- *Is the parser cherry-picking successes?* No. Parsing failures: 0/160.
  See `scripts/diagnose.py`.

- *Is the model just guessing?* No. Neutral accuracy is 0.85 for both models,
  well above chance on this question set.

- *Why two models from the same family?* Scoped as a pilot. Cross-family
  replication is stated as next work in `README.md` § Limitations.

- *Why does `gpt-4.1-mini` show "no effect" on authority?* At n = 20, absence
  of a detectable effect is not evidence of no effect. The claim is
  deliberately weak: "no statistically detectable effect at this sample size."

- *Is 20 questions enough?* For effects at r > 0.6, yes — the two misleading
  context effects are robust. For effects around r = 0.3–0.5, borderline.
  This is flagged in Limitations.

## Reading order

- **30 seconds**: this file, section "The finding in one sentence".
- **2 minutes**: `README.md`, sections TL;DR + Key results + the figure.
- **10 minutes**: this file in full + `reports/summary.md`.
- **30 minutes**: the whole repo, including scripts and raw data.

## Time and cost

- Development: ~2 weeks part-time.
- API cost: under $0.10 for the full 160-call run.
- Reproduction: 5 minutes for analysis only, 15 minutes including API calls.

## Repository

https://github.com/cbsnet/epistemic-calibration-audit

## Contact

Tony Sale
info@tonysale.com