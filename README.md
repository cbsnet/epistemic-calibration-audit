# Epistemic Calibration Audit under Pressure

**A pilot audit of LLM epistemic robustness under social, authority, and contextual pressure.**

> **TL;DR.** We audit `openai/gpt-oss-120b` under four pressure conditions.
> The model is chronically overconfident, resistant to social pressure,
> and significantly destabilized by authority pressure and false context.
> Full pipeline runnable in 5 minutes. See `FOR_REVIEWERS.md`.

## Abstract

We measure how the calibration and accuracy of a frontier LLM change when the
same question is asked under four conditions: a neutral baseline, social
pressure, authority pressure, and misleading external context. We find that the
model is chronically overconfident in the neutral condition (mean confidence
99.95%, accuracy 85%), resists social pressure entirely, but is significantly
destabilized by authority pressure (accuracy drops to 55%, p = 0.014) and by
misleading external context (accuracy drops to 45%, p = 0.005). In all
conditions, confidence remains far above what accuracy justifies, indicating
that verbalized confidence is not a reliable signal of epistemic reliability
under pressure.

## Why this matters for AI Safety

Reliable oversight of increasingly capable models depends on their beliefs being
*stable under pressure* and *calibrated*. If a model abandons correct answers
under mild social or authority pressure, or becomes overconfident when fed false
context, scalable oversight and downstream decision-making are undermined.

This audit isolates three distinct failure modes—social susceptibility,
authority deference, and false-context absorption—and shows that they are not
uniform. A model can be robust to one and vulnerable to another, while
exhibiting the same high confidence in all cases. This asymmetry is invisible to
aggregate benchmarks and matters for deployment in adversarial or contested
information environments.

## Method

- **Dataset**: 20 questions with unambiguous ground truth, balanced across
  5 domains (geography, math, history, science, literature).
- **Model**: `openai/gpt-oss-120b` via Groq.
- **Conditions**:
  - C1 `neutral` — baseline
  - C2 `social_pressure` — a user disagrees with the previous answer
  - C3 `authority_pressure` — a domain expert contradicts the common answer
  - C4 `misleading_context` — a plausible but false external claim
- **Metrics**: accuracy, Brier score, Expected Calibration Error (ECE),
  flip rate, mean confidence.
- **Statistics**: paired Wilcoxon signed-rank tests, Bonferroni correction,
  effect size (r).
- **Reproducibility**: full pipeline runnable with `make reproduce`.

## Key results

### Summary

| Condition | n | Accuracy | Mean confidence | Brier | ECE |
|---|---|---|---|---|---|
| neutral | 20 | **0.85** | 0.9995 | 0.150 | 0.150 |
| social_pressure | 20 | **0.85** | 0.9950 | 0.148 | 0.145 |
| authority_pressure | 20 | **0.55** | 0.8910 | 0.289 | 0.341 |
| misleading_context | 20 | **0.45** | 0.9005 | 0.425 | 0.451 |

### Flip rate (fraction of answers changed vs. neutral)

| Treatment | Flip rate |
|---|---|
| social_pressure | 0.10 |
| authority_pressure | 0.40 |
| misleading_context | 0.55 |

### Paired tests (neutral vs. treatment)

| Treatment | p (raw) | p (Bonferroni) | effect size r |
|---|---|---|---|
| social_pressure | 1.000 | 1.000 | 0.00 |
| authority_pressure | 0.014 | 0.043 | 0.55 |
| misleading_context | 0.005 | 0.014 | 0.63 |

### Findings

1. **Chronic overconfidence.** In the neutral condition, the model declares
   confidence 1.00 in 19 of 20 responses (mean 0.9995) while answering
   correctly 85% of the time. Its ECE is 0.150 even without any pressure.

2. **Social pressure has no effect.** Flip rate 10%, accuracy unchanged,
   p = 1.0. The model is fully robust to a user who merely disagrees.

3. **Authority pressure is destabilizing.** Flip rate 40%, accuracy drops
   from 85% to 55%, p = 0.014 (Bonferroni-corrected 0.043). Effect size
   r = 0.55, medium-to-large.

4. **Misleading external context is the strongest attack.** Flip rate 55%,
   accuracy drops from 85% to 45%, p = 0.005 (Bonferroni-corrected 0.014).
   Effect size r = 0.63.

5. **Confidence does not track correctness.** Confidence drops slightly under
   authority and misleading conditions, but remains far above what accuracy
   justifies. In the neutral condition, confidence is at ceiling and provides
   no discriminative signal at all.

## Figures

- `reports/figures/reliability_by_condition.png` — reliability diagram by condition
- `reports/figures/accuracy_by_condition.png` — accuracy by condition
- `reports/figures/confidence_by_condition.png` — mean confidence by condition

## Limitations

- **Single model.** Results are from one model (`openai/gpt-oss-120b`). The
  asymmetry between pressure types may or may not generalize.
- **Small n.** 20 questions per condition. Effects are statistically
  significant after correction, but confidence intervals are wide.
- **Verbalized confidence as proxy.** We measure stated confidence, not
  internal uncertainty. The two may diverge.
- **Operationalization of pressure.** The three pressure prompts are simple
  templates; real-world pressure is more varied and multi-turn.
- **No reasoning-trace analysis.** Reasoning models expose chains of thought;
  we did not analyze them to understand *why* the model flips.

## Reproducibility

```bash
make reproduce