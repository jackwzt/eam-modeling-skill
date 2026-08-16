"""
Adapted from Learning-Bayesian-Statistics/baygent-skills, commit
aa940481ebb9fbd087b2fc41dba3af386b5bdb31 (MIT License, Copyright 2026
Learning Bayesian Statistics).

Inspect BayesFlow training convergence.

Reads a saved training history (JSON) and produces a structured report
checking for NaN, overfitting, and under-training.

The history file should contain the dict returned by
``history.history`` after a ``workflow.fit_*`` call:

    import json
    history = workflow.fit_online(...)
    with open("history.json", "w") as f:
        json.dump(history.history, f)

Note: ``validation_data`` should be passed to all ``fit_*`` calls (use an
integer for online training to auto-simulate validation sets). If ``val_loss``
is absent, the script still runs but cannot check for overfitting.

Usage:
    python inspect_bayesflow_training.py --history history.json
    python inspect_bayesflow_training.py --history history.json --output report.json
"""

import argparse
import json
import math
import sys


# Thresholds
OVERFIT_RELATIVE_GAP = 0.10
UNDERFIT_RELATIVE_IMPROVEMENT = 0.01


def inspect_history(history: dict) -> dict:
    """Analyse a Keras history dict and return a structured report.

    Parameters
    ----------
    history : dict
        A dictionary with at least a ``"loss"`` key mapping to a list
        of per-epoch loss values.  ``"val_loss"`` should be present
        (pass ``validation_data=`` to ``fit_*``). If absent, overfitting
        detection is skipped.

    Returns
    -------
    dict
        Structured report with keys: ``nan_check``, ``final_losses``,
        ``overfitting``, ``under_training``, ``overall``.
    """
    train_loss = history.get("loss")
    val_loss = history.get("val_loss")

    if train_loss is None or len(train_loss) == 0:
        return {"error": "History does not contain a 'loss' key or it is empty."}

    report: dict = {}

    # ── NaN check ─────────────────────────────────────────────
    try:
        train_loss = [float(value) for value in train_loss]
        val_loss = None if val_loss is None else [float(value) for value in val_loss]
    except (TypeError, ValueError):
        return {"error": "Training history loss values must be numeric."}

    train_has_nan = any(not math.isfinite(v) for v in train_loss)
    val_has_nan = val_loss is not None and any(not math.isfinite(v) for v in val_loss)
    report["nan_check"] = {
        "train_nan": train_has_nan,
        "val_nan": val_has_nan,
        "ok": not train_has_nan and not val_has_nan,
    }

    # ── Final losses ──────────────────────────────────────────
    report["final_losses"] = {
        "train": train_loss[-1],
        "val": val_loss[-1] if val_loss else None,
        "epochs": len(train_loss),
    }

    # ── Overfitting ───────────────────────────────────────────
    # For online training (fit_online) val_loss is absent by design: each epoch
    # draws freshly simulated data, so the network cannot overfit to a fixed
    # dataset and a train/val split is unnecessary.
    if val_loss is not None and len(val_loss) > 1:
        n_tail = max(1, math.ceil(len(train_loss) * 0.1))
        avg_val_tail = sum(val_loss[-n_tail:]) / n_tail
        avg_train_tail = sum(train_loss[-n_tail:]) / n_tail
        relative_gap = (avg_val_tail - avg_train_tail) / max(abs(avg_train_tail), 1e-12)
        overfit = relative_gap > OVERFIT_RELATIVE_GAP
        report["overfitting"] = {
            "detected": overfit,
            "avg_val_loss_last_10pct": avg_val_tail,
            "avg_train_loss_last_10pct": avg_train_tail,
            "relative_gap": round(relative_gap, 3),
            "threshold": OVERFIT_RELATIVE_GAP,
            "note": "Heuristic only; inspect full curves and held-out diagnostics.",
        }
    else:
        report["overfitting"] = {
            "detected": None,
            "message": (
                "No validation loss found. Pass validation_data= to fit_* calls "
                "to enable overfitting detection."
            ),
        }

    # ── Under-training ────────────────────────────────────────
    if len(train_loss) >= 4:
        n_tail = max(1, math.ceil(len(train_loss) * 0.1))
        current = sum(train_loss[-n_tail:]) / n_tail
        previous_slice = train_loss[-2 * n_tail : -n_tail]
        previous = sum(previous_slice) / len(previous_slice)
        relative_improvement = (previous - current) / max(abs(previous), 1e-12)
        still_decreasing = relative_improvement > UNDERFIT_RELATIVE_IMPROVEMENT
        report["under_training"] = {
            "detected": still_decreasing,
            "previous_tail_mean": previous,
            "current_tail_mean": current,
            "relative_improvement": round(relative_improvement, 3),
            "threshold": UNDERFIT_RELATIVE_IMPROVEMENT,
            "note": "Heuristic only; a plateau does not establish calibrated inference.",
        }
    else:
        report["under_training"] = {
            "detected": None,
            "message": "Fewer than 4 epochs — cannot assess under-training.",
        }

    # ── Overall ───────────────────────────────────────────────
    issues = []
    if report["nan_check"]["train_nan"]:
        issues.append("Training loss contains NaN — inspect simulator outputs and standardization")
    if report["nan_check"]["val_nan"]:
        issues.append("Validation loss contains NaN — inspect simulator outputs and standardization")
    if report["overfitting"].get("detected"):
        issues.append(
            f"Possible overfitting detected (relative validation gap {report['overfitting']['relative_gap']} over the final 10% of epochs) "
            "— reduce capacity, add regularization, or increase simulation budget"
        )
    if report["under_training"].get("detected"):
        issues.append("Loss still decreasing at final epoch — consider more epochs")

    report["overall"] = {
        "ok": len(issues) == 0,
        "issues": issues,
        "recommendation": (
            "Training looks healthy."
            if len(issues) == 0
            else "Address the following before proceeding: " + "; ".join(issues)
        ),
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="Inspect BayesFlow training convergence")
    parser.add_argument(
        "--history", required=True, help="Path to history JSON file (saved from history.history)"
    )
    parser.add_argument(
        "--output", default=None, help="Path to save JSON report (default: print to stdout)"
    )
    args = parser.parse_args()

    try:
        with open(args.history) as f:
            history = json.load(f)
    except Exception as e:
        print(json.dumps({"error": f"Could not load history: {e}"}))
        sys.exit(1)

    report = inspect_history(history)

    output = json.dumps(report, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
