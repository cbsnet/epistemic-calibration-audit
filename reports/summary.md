# Summary — Epistemic Calibration Audit under Pressure

**Models:** `openai/gpt-oss-120b` (via Groq), `gpt-4.1-mini` (via OpenAI API)
**Date:** 2026-10-03
**Questions:** 20 (5 domains × 2 difficulties)
**Conditions:** 4 (neutral, social_pressure, authority_pressure, misleading_context)
**Total responses:** 160 (2 models × 20 questions × 4 conditions)

## Headline

Both models are chronically overconfident (mean confidence ≥ 0.999 in neutral,
accuracy 0.85) and fully resist social pressure (p = 1.0). Both collapse under
misleading external context, though `gpt-4.1-mini` is hit harder (accuracy 0.15
vs. 0.40). They diverge on authority pressure: `gpt-oss-120b` cedes
significantly (p_bonferroni = 0.043), `gpt-4.1-mini` does not show a
statistically detectable effect at this sample size (p_bonferroni = 0.47).

## Metrics by model and condition

| Model | Condition | n | Accuracy | Mean conf. | Brier | ECE | Flip rate |
|---|---|---|---|---|---|---|---|
| gpt-4.1-mini | neutral | 20 | 0.85 | 1.0000 | 0.150 | 0.150 | — |
| gpt-4.1-mini | social_pressure | 20 | 0.85 | 0.9900 | 0.146 | 0.140 | 0.05 |
| gpt-4.1-mini | authority_pressure | 20 | 0.75 | 0.9525 | 0.218 | 0.203 | 0.15 |
| gpt-4.1-mini | misleading_context | 20 | 0.15 | 0.6500 | 0.395 | 0.500 | 0.85 |
| gpt-oss-120b | neutral | 20 | 0.85 | 0.9990 | 0.149 | 0.149 | — |
| gpt-oss-120b | social_pressure | 20 | 0.85 | 0.9945 | 0.147 | 0.145 | 0.10 |
| gpt-oss-120b | authority_pressure | 20 | 0.55 | 0.8855 | 0.299 | 0.336 | 0.45 |
| gpt-oss-120b | misleading_context | 20 | 0.40 | 0.8495 | 0.392 | 0.450 | 0.60 |

## Paired tests (Wilcoxon signed-rank, neutral vs. treatment)

| Model | Treatment | Statistic | p | p (Bonferroni) | r |
|---|---|---|---|---|---|
| gpt-4.1-mini | social_pressure | 0.0 | 1.000 | 1.000 | 0.00 |
| gpt-4.1-mini | authority_pressure | 0.0 | 0.157 | 0.472 | 0.32 |
| gpt-4.1-mini | misleading_context | 0.0 | 0.00018 | 0.00055 | 0.84 |
| gpt-oss-120b | social_pressure | 0.0 | 1.000 | 1.000 | 0.00 |
| gpt-oss-120b | authority_pressure | 0.0 | 0.014 | 0.043 | 0.55 |
| gpt-oss-120b | misleading_context | 0.0 | 0.0027 | 0.0081 | 0.67 |

## Findings

### Structural across both models

1. **Chronic overconfidence in the neutral condition.** Both models declare
   mean confidence ≥ 0.999 with 85% accuracy. ECE = 0.150 for both. The
   failure exists before any adversarial pressure is applied.

2. **Full resistance to social pressure.** Flip rate 5–10%, accuracy unchanged
   at 0.85, p = 1.0 for both. A user who merely disagrees does not move either
   model.

3. **Collapse under misleading external context.** Both models cede, with
   p_bonferroni < 0.01 and very large effect sizes (r = 0.67 for
   `gpt-oss-120b`, r = 0.84 for `gpt-4.1-mini`). `gpt-4.1-mini` is hit harder:
   accuracy drops to 0.15 with confidence still at 0.65, giving the worst
   calibration failure in the study (ECE = 0.500).

### Model-specific

4. **Authority pressure divides the two models.** `gpt-oss-120b` (larger,
   reasoning-based) cedes significantly: accuracy 0.55, flip rate 0.45,
   p_bonferroni = 0.043, r = 0.55. `gpt-4.1-mini` (smaller, non-reasoning)
   shows no statistically detectable effect at this sample size: accuracy 0.75,
   flip rate 0.15, p_bonferroni = 0.47, r = 0.32.

## Confidence behaviour

**Neutral condition, both models.** Confidence is at ceiling: `gpt-4.1-mini`
reports 1.00 in all 20 responses; `gpt-oss-120b` reports ≥ 0.99 in all 20.
No discriminative signal.

**Social pressure, both models.** Essentially unchanged from neutral.

**Authority pressure.**
- `gpt-4.1-mini`: mean confidence 0.9525, distribution concentrated at 0.95–1.00.
- `gpt-oss-120b`: mean confidence 0.8855, distribution spread from 1.00 down
  to 0.62.

**Misleading context.**
- `gpt-4.1-mini`: mean confidence 0.6500. Confidence drops, but accuracy is
  0.15, so the model is still dramatically overconfident.
- `gpt-oss-120b`: mean confidence 0.8495. Same pattern, less extreme.

In all conditions where accuracy collapses, confidence drops less than
proportionally. Confidence under pressure is not a usable proxy for
reliability under pressure.

## Limitations

- **Two models only.** Both from the OpenAI family. Cross-family generalization
  is an open question.
- **Small n.** 20 questions per condition per model. Effects at
  p_bonferroni < 0.01 are robust; effects in the 0.01–0.05 range are within
  the margin of sample variation. The null result on authority for
  `gpt-4.1-mini` is absence of evidence, not evidence of absence.
- **Confounded comparison.** The two models differ in size, reasoning
  capability, and serving infrastructure. The divergence on authority pressure
  cannot be attributed to any single factor.
- **Verbalized confidence is not internal uncertainty.** We measure stated
  confidence only.
- **Single-turn pressure prompts.** Template-based, not adaptive.
- **No reasoning-trace analysis.**

## Files

- `figures/reliability_by_condition.png`
- `figures/accuracy_by_condition.png`
- `figures/confidence_by_condition.png`
- `summary.csv`
- `flip_rate.csv`
- `paired_tests.csv`