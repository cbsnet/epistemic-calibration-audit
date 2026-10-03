# Summary — Epistemic Calibration Audit under Pressure

**Model:** `openai/gpt-oss-120b` (via Groq)
**Date:** 2026-10-03
**Questions:** 20 (5 domains × 2 difficulties)
**Conditions:** 4 (neutral, social_pressure, authority_pressure, misleading_context)
**Total responses:** 80

## Headline

The model is chronically overconfident, fully robust to social pressure, and
significantly destabilized by authority pressure and misleading external
context. Confidence remains high in all conditions, including those where
accuracy collapses.

## Metrics

| Condition | n | Accuracy | Mean conf. | Brier | ECE | Flip rate |
|---|---|---|---|---|---|---|
| neutral | 20 | 0.85 | 0.9995 | 0.150 | 0.150 | — |
| social_pressure | 20 | 0.85 | 0.9950 | 0.148 | 0.145 | 0.10 |
| authority_pressure | 20 | 0.55 | 0.8910 | 0.289 | 0.341 | 0.40 |
| misleading_context | 20 | 0.45 | 0.9005 | 0.425 | 0.451 | 0.55 |

## Paired tests (Wilcoxon signed-rank, neutral vs. treatment)

| Treatment | Statistic | p | p (Bonferroni) | r |
|---|---|---|---|---|
| social_pressure | 0.0 | 1.000 | 1.000 | 0.00 |
| authority_pressure | 0.0 | 0.014 | 0.043 | 0.55 |
| misleading_context | 0.0 | 0.005 | 0.014 | 0.63 |

## Confidence distribution

**neutral:** 19× 1.00, 1× 0.99 — ceiling effect, no discriminative signal.

**social_pressure:** 10× 1.00, 10× 0.99 — identical to neutral.

**authority_pressure:** spread from 1.00 down to 0.62, with clusters at 0.99,
0.95, 0.71. Confidence responds to the conflict, but not proportionally to
accuracy.

**misleading_context:** spread from 1.00 down to 0.30, with the mode at 0.95.
The model registers the conflict but remains overconfident.

## Findings

1. **Chronic overconfidence.** Even in neutral, ECE = 0.150 and mean
   confidence = 0.9995 with accuracy 0.85.

2. **Social pressure has no effect.** Accuracy unchanged, p = 1.0.

3. **Authority pressure destabilizes.** Accuracy −30 pp, p = 0.014,
   Bonferroni-corrected 0.043, r = 0.55.

4. **Misleading context is the strongest attack.** Accuracy −40 pp, p = 0.005,
   Bonferroni-corrected 0.014, r = 0.63.

5. **Confidence does not track correctness.** Under both significant attacks,
   confidence drops but remains far above accuracy.

## Limitations

- Single model, single run per question.
- 20 questions per condition — wide CIs.
- Verbalized confidence is not internal uncertainty.
- Pressure prompts are single-turn templates.
- No analysis of reasoning traces.

## Files

- `figures/reliability_by_condition.png`
- `figures/accuracy_by_condition.png`
- `figures/confidence_by_condition.png`
- `summary.csv`
- `flip_rate.csv`
- `paired_tests.csv`