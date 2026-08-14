"""
Adapted from Learning-Bayesian-Statistics/baygent-skills, commit
aa940481ebb9fbd087b2fc41dba3af386b5bdb31 (MIT License, Copyright 2026
Learning Bayesian Statistics).

Interpret BayesFlow diagnostics and suggest next steps.

Reads a saved diagnostics DataFrame (CSV) produced by
``workflow.compute_default_diagnostics(test_data=..., as_data_frame=True)``
and produces qualitative per-parameter assessments for the diagnostic report.

Save the DataFrame before running this script:

    metrics = workflow.compute_default_diagnostics(test_data=test_data, as_data_frame=True)
    metrics.to_csv("metrics.csv")

Usage:
    python check_diagnostics.py --metrics metrics.csv
    python check_diagnostics.py --metrics metrics.csv --history history.json
    python check_diagnostics.py --metrics metrics.csv --output report.json
"""

import argparse
import json
import sys

import pandas as pd


# House thresholds
# Internal reference levels for qualitative interpretation.
# These are NOT exposed in reports — use the qualitative labels instead.
ECE_EXCELLENT = 0.05
ECE_FAIR = 0.10

NRMSE_EXCELLENT = 0.05
NRMSE_GOOD = 0.10
NRMSE_FAIR = 0.15

CONTRACTION_LOW = 0.80
CONTRACTION_HIGH = 0.95


def _rate_ece(ece: float) -> str:
    if ece <= ECE_EXCELLENT:
        return "excellent"
    elif ece <= ECE_FAIR:
        return "fair"
    else:
        return "poor"


def _rate_nrmse(nrmse: float) -> str:
    if nrmse <= NRMSE_EXCELLENT:
        return "excellent"
    elif nrmse <= NRMSE_GOOD:
        return "good"
    elif nrmse <= NRMSE_FAIR:
        return "fair"
    else:
        return "poor"


def _rate_contraction(contraction: float, ece_rating: str) -> str:
    if contraction > CONTRACTION_HIGH and ece_rating == "poor":
        return "poor — overconfident"
    elif contraction > CONTRACTION_HIGH:
        return "high"
    elif contraction >= CONTRACTION_LOW:
        return "medium"
    else:
        return "low"


def check_diagnostics(metrics: pd.DataFrame) -> dict:
    """Interpret a diagnostics DataFrame into qualitative per-parameter assessments.

    Parameters
    ----------
    metrics : pd.DataFrame
        DataFrame as returned by
        ``workflow.compute_default_diagnostics(as_data_frame=True)``.
        Rows are metric names (``RMSE``, ``NRMSE``, ``Log-gamma``,
        ``ECE``, ``Post. Contraction``), columns are parameter names.

    Returns
    -------
    dict
        Structured report with:
        - ``parameters``: per-parameter dict with numeric values and
          qualitative ratings (``calibration``, ``recovery``, ``contraction``).
        - ``summary``: plain-language sentence per parameter for the report.
    """
    report: dict = {"parameters": {}, "summary": {}}

    # Determine which RMSE row is available
    has_nrmse = "NRMSE" in metrics.index
    has_rmse = "RMSE" in metrics.index
    rmse_key = "NRMSE" if has_nrmse else ("RMSE" if has_rmse else None)

    for param in metrics.columns:
        param_report: dict = {}

        # ECE
        cal_rating = None
        if "ECE" in metrics.index:
            ece = float(metrics.loc["ECE", param])
            cal_rating = _rate_ece(ece)
            param_report["ECE"] = round(ece, 3)
            param_report["calibration"] = cal_rating

        # NRMSE / RMSE
        rec_rating = None
        if rmse_key is not None:
            nrmse = float(metrics.loc[rmse_key, param])
            rec_rating = _rate_nrmse(nrmse)
            param_report[rmse_key] = round(nrmse, 3)
            param_report["recovery"] = rec_rating

        # Posterior contraction
        con_rating = None
        if "Post. Contraction" in metrics.index:
            contraction = float(metrics.loc["Post. Contraction", param])
            con_rating = _rate_contraction(contraction, cal_rating or "fair")
            param_report["Post. Contraction"] = round(contraction, 3)
            param_report["contraction"] = con_rating

        report["parameters"][param] = param_report

        # ── Build plain-language summary for this parameter ───
        parts = []
        if cal_rating:
            parts.append(f"{cal_rating} calibration")
        if rec_rating:
            parts.append(f"{rec_rating} recovery")
        if con_rating:
            if "overconfident" in con_rating:
                parts.append(con_rating)
            else:
                parts.append(f"{con_rating} contraction")
        report["summary"][param] = "; ".join(parts) if parts else "no metrics available"

    return report


def suggest_next_steps(training_report: dict, diagnostic_report: dict) -> list[str]:
    """Combine training and diagnostic assessments into actionable next steps.

    Parameters
    ----------
    training_report : dict
        Output of ``inspect_history()`` from ``scripts/inspect_training.py``.
    diagnostic_report : dict
        Output of ``check_diagnostics()`` from this module.

    Returns
    -------
    list[str]
        Ordered list of suggested next steps, most critical first.
    """
    steps: list[str] = []

    # ── Training issues (highest priority) ────────────────────
    if training_report.get("nan_check", {}).get("train_nan"):
        steps.append(
            "Training loss contains NaN — inspect simulator outputs for "
            "inf/NaN values and ensure proper data standardization."
        )
    if training_report.get("nan_check", {}).get("val_nan"):
        steps.append(
            "Validation loss contains NaN — inspect simulator outputs and "
            "check that validation data are well-formed."
        )
    if training_report.get("overfitting", {}).get("detected"):
        ratio = training_report["overfitting"].get("ratio", "?")
        steps.append(
            f"Overfitting detected (val/train loss ratio {ratio}x in final "
            "10% of epochs) — reduce network capacity, add regularization, "
            "or increase simulation budget."
        )
    if training_report.get("under_training", {}).get("detected"):
        steps.append(
            "Loss is still decreasing at the final epoch — increase the "
            "number of training epochs (e.g., double the current value)."
        )

    # ── Diagnostic issues ─────────────────────────────────────
    params = diagnostic_report.get("parameters", {})

    # Collect parameters by issue type
    cal_poor = []
    cal_fair = []
    recovery_poor = []
    recovery_fair = []
    contraction_poor = []
    contraction_low = []

    for param, info in params.items():
        cal = info.get("calibration", "")
        rec = info.get("recovery", "")
        con = info.get("contraction", "")

        if cal == "poor":
            cal_poor.append(param)
        elif cal == "fair":
            cal_fair.append(param)

        if rec == "poor":
            recovery_poor.append(param)
        elif rec == "fair":
            recovery_fair.append(param)

        if "overconfident" in con:
            contraction_poor.append(param)
        elif con == "low":
            contraction_low.append(param)

    if cal_poor:
        names = ", ".join(cal_poor)
        steps.append(
            f"Poor calibration for {names} — increase summary network "
            "capacity or train for more epochs."
        )
    if recovery_poor:
        names = ", ".join(recovery_poor)
        steps.append(
            f"Poor recovery for {names} — increase network capacity and "
            "training duration; if no improvement, these parameters may be "
            "weakly identifiable."
        )
    if contraction_poor:
        names = ", ".join(contraction_poor)
        steps.append(
            f"Overconfident posteriors for {names} — inspect the simulator "
            "for potential issues and consider increasing the simulation budget."
        )
    if contraction_low:
        names = ", ".join(contraction_low)
        steps.append(
            f"Low contraction for {names} — the data may not be "
            "informative for these parameters; consider a more informative "
            "prior or a richer summary network."
        )
    if cal_fair and not cal_poor:
        names = ", ".join(cal_fair)
        steps.append(
            f"Fair calibration for {names} — consider more training "
            "epochs or a slight capacity increase."
        )
    if recovery_fair and not recovery_poor:
        names = ", ".join(recovery_fair)
        steps.append(
            f"Fair recovery for {names} — consider more training "
            "epochs or increased network capacity."
        )

    # ── Default if nothing is wrong ───────────────────────────
    if not steps:
        steps.append(
            "All diagnostics are within acceptable bounds — proceed to "
            "real-data inference and posterior predictive checks."
        )
        steps.append(
            "If the simulator is fast, consider a refinement pass with "
            "online training (fit_online) to squeeze out additional performance."
        )

    return steps


def main():
    parser = argparse.ArgumentParser(description="Check BayesFlow diagnostics and suggest next steps")
    parser.add_argument(
        "--metrics", required=True, help="Path to diagnostics CSV (saved from metrics.to_csv(...))"
    )
    parser.add_argument(
        "--history", default=None, help="Path to training history JSON (saved from history.history)"
    )
    parser.add_argument(
        "--output", default=None, help="Path to save JSON report (default: print to stdout)"
    )
    args = parser.parse_args()

    try:
        metrics = pd.read_csv(args.metrics, index_col=0)
    except Exception as e:
        print(json.dumps({"error": f"Could not load metrics CSV: {e}"}))
        sys.exit(1)

    # Print the table so it's visible in terminal output
    print("=== Diagnostics Table ===")
    print(metrics.to_string())
    print("=========================\n")

    diag_report = check_diagnostics(metrics)

    # Print per-parameter summaries for quick reading
    print("=== Per-Parameter Assessment ===")
    for param, summary in diag_report.get("summary", {}).items():
        print(f"  {param}: {summary}")
    print("================================\n")

    # Load training history if provided
    training_report = {}
    if args.history:
        try:
            # Import inspect_history from sibling module
            import os

            sys.path.insert(0, os.path.dirname(__file__))
            from inspect_training import inspect_history

            with open(args.history) as f:
                history = json.load(f)
            training_report = inspect_history(history)
        except Exception as e:
            print(f"Warning: Could not load training history: {e}", file=sys.stderr)

    next_steps = suggest_next_steps(training_report, diag_report)
    diag_report["next_steps"] = next_steps

    output = json.dumps(diag_report, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
