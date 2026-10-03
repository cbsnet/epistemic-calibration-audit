import numpy as np
from scipy import stats


def brier_score(confidences, outcomes):
    return float(np.mean((np.array(confidences) - np.array(outcomes)) ** 2))


def expected_calibration_error(confidences, outcomes, n_bins: int = 10):
    confidences = np.array(confidences)
    outcomes = np.array(outcomes)
    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (confidences > bins[i]) & (confidences <= bins[i + 1])
        if mask.sum() == 0:
            continue
        acc = outcomes[mask].mean()
        conf = confidences[mask].mean()
        ece += mask.sum() / len(confidences) * abs(acc - conf)
    return float(ece)


def paired_test(baseline, treatment):
    baseline = np.array(baseline)
    treatment = np.array(treatment)
    if np.allclose(baseline, treatment):
        return {"statistic": 0.0, "p_value": 1.0, "effect_size_r": 0.0}
    stat, p = stats.wilcoxon(baseline, treatment)
    n = len(baseline)
    z = stats.norm.isf(p / 2) if p > 0 else 0.0
    r = z / np.sqrt(n)
    return {"statistic": float(stat), "p_value": float(p), "effect_size_r": float(r)}