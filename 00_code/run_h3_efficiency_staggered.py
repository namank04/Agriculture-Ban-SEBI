"""
H3 staggered-timing robustness analysis.

Purpose
-------
Re-estimate the H3 spot-efficiency and spatial-integration comparisons using
each treated commodity's actual derivatives-suspension date.

For each treated commodity, all control commodities are split at the SAME date
as that treated commodity. This creates a treated-vs-controls comparison for
each suspension cohort without assigning a fictitious treatment date to the
controls.

This script does NOT overwrite the existing common-date H3 outputs.

OUTPUT:
04_empirics/H3_spot_efficiency/output_staggered/
"""

from pathlib import Path

import numpy as np
import pandas as pd

import run_h3_efficiency as h3
from utils import log_returns

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "04_empirics" / "H3_spot_efficiency" / "output_staggered"
OUT.mkdir(parents=True, exist_ok=True)

TREAT_DATE = {
    "chana": pd.Timestamp("2021-08-16"),
    "mustard": pd.Timestamp("2021-10-08"),
    "soybean": pd.Timestamp("2021-12-20"),
    "moong": pd.Timestamp("2021-12-20"),
}

CONTROLS = ["castor", "guarseed413", "jeera", "turmeric", "cotton"]


# ----------------------------------------------------------------------
# PART A — variance-ratio efficiency
# ----------------------------------------------------------------------

def vr_change(slug, t0, q):
    s = h3.load_national(slug)

    if s.empty:
        return None

    r = log_returns(s)

    pre = h3._winsor(r[r.index < t0])
    post = h3._winsor(r[r.index >= t0])

    vr_pre, z1_pre, z2_pre = h3.lomac_vr(pre.values, q)
    vr_post, z1_post, z2_post = h3.lomac_vr(post.values, q)

    if pd.isna(vr_pre) or pd.isna(vr_post):
        return None

    return {
        "n_pre": len(pre),
        "n_post": len(post),
        "vr_pre": vr_pre,
        "vr_post": vr_post,
        "z2_pre": z2_pre,
        "z2_post": z2_post,
        "ineff_pre": abs(vr_pre - 1),
        "ineff_post": abs(vr_post - 1),
        "d_ineff": abs(vr_post - 1) - abs(vr_pre - 1),
    }


def part_a():
    treated_rows = []
    control_rows = []

    for treated, t0 in TREAT_DATE.items():

        for q in [2, 5, 10]:

            tr = vr_change(treated, t0, q)
            if tr is None:
                continue

            controls_here = []

            for control in CONTROLS:
                co = vr_change(control, t0, q)

                if co is None:
                    continue

                controls_here.append(co["d_ineff"])

                control_rows.append({
                    "treated_reference": treated,
                    "treat_date": t0.date(),
                    "control": control,
                    "q": q,
                    **co,
                })

            control_mean = np.mean(controls_here)

            treated_rows.append({
                "treated": treated,
                "treat_date": t0.date(),
                "q": q,
                **tr,
                "control_mean_d_ineff": control_mean,
                "treated_minus_control": tr["d_ineff"] - control_mean,
            })

    treated_df = pd.DataFrame(treated_rows)
    control_df = pd.DataFrame(control_rows)

    treated_df.to_csv(
        OUT / "A_staggered_by_treated.csv",
        index=False
    )

    control_df.to_csv(
        OUT / "A_staggered_controls.csv",
        index=False
    )

    summary = (
        treated_df.groupby("q")
        .agg(
            treated_mean_d_ineff=("d_ineff", "mean"),
            control_mean_d_ineff=("control_mean_d_ineff", "mean"),
            mean_treated_minus_control=("treated_minus_control", "mean"),
            n_treated=("treated", "count"),
        )
        .reset_index()
    )

    summary.to_csv(
        OUT / "A_staggered_summary.csv",
        index=False
    )

    print("\nPART A — staggered variance-ratio comparison")
    print(summary.round(4).to_string(index=False))

    print("\nCommodity-level q=10 contrasts:")
    print(
        treated_df[treated_df.q == 10][
            [
                "treated",
                "treat_date",
                "d_ineff",
                "control_mean_d_ineff",
                "treated_minus_control",
            ]
        ].round(4).to_string(index=False)
    )

    return treated_df, control_df, summary


# ----------------------------------------------------------------------
# PART B — cross-mandi spatial integration
# ----------------------------------------------------------------------

def select_mandis_at(panel, t0):
    pre_days = pd.bdate_range(
        "2017-01-01",
        t0 - pd.Timedelta(days=1)
    )

    post_days = pd.bdate_range(
        t0,
        panel.date.max()
    )

    npre = len(pre_days)
    npost = len(post_days)

    cov = (
        panel.assign(post=(panel.date >= t0))
        .groupby(["market_id", "post"])["date"]
        .nunique()
        .unstack("post")
        .fillna(0)
    )

    cov = cov.rename(
        columns={
            False: "n_pre",
            True: "n_post",
        }
    )

    if "n_pre" not in cov.columns:
        cov["n_pre"] = 0

    if "n_post" not in cov.columns:
        cov["n_post"] = 0

    cov["frac_pre"] = cov["n_pre"] / npre
    cov["frac_post"] = cov["n_post"] / npost

    cov["frac_min"] = cov[
        ["frac_pre", "frac_post"]
    ].min(axis=1)

    eligible = cov[
        (cov.frac_pre >= h3.MIN_COVERAGE_FRAC)
        &
        (cov.frac_post >= h3.MIN_COVERAGE_FRAC)
    ]

    chosen = (
        eligible
        .sort_values("frac_min", ascending=False)
        .head(h3.SELECT_TOP_MANDIS)
    )

    return list(chosen.index)


def integration_change(slug, t0):
    panel = h3.load_mandi_panel(slug)

    if panel.empty:
        return None

    markets = select_mandis_at(panel, t0)

    if len(markets) < 3:
        return None

    hi = panel.date.max() + pd.Timedelta(days=1)

    pre = h3.wide_log_prices(
        panel,
        markets,
        pd.Timestamp("2017-01-01"),
        t0,
    )

    post = h3.wide_log_prices(
        panel,
        markets,
        t0,
        hi,
    )

    share_pre, hl_pre, npairs_pre = h3.coint_window(pre)
    share_post, hl_post, npairs_post = h3.coint_window(post)

    return {
        "n_mandi": len(markets),
        "share_pre": share_pre,
        "share_post": share_post,
        "d_share": share_post - share_pre,
        "hl_pre": hl_pre,
        "hl_post": hl_post,
        "d_hl": hl_post - hl_pre,
        "npairs_pre": npairs_pre,
        "npairs_post": npairs_post,
    }


def part_b():
    treated_rows = []
    control_rows = []

    for treated, t0 in TREAT_DATE.items():

        tr = integration_change(treated, t0)

        if tr is None:
            continue

        control_d_share = []
        control_d_hl = []

        for control in CONTROLS:

            co = integration_change(control, t0)

            if co is None:
                continue

            control_d_share.append(co["d_share"])
            control_d_hl.append(co["d_hl"])

            control_rows.append({
                "treated_reference": treated,
                "treat_date": t0.date(),
                "control": control,
                **co,
            })

        mean_control_share = np.mean(control_d_share)
        mean_control_hl = np.mean(control_d_hl)

        treated_rows.append({
            "treated": treated,
            "treat_date": t0.date(),
            **tr,
            "control_mean_d_share": mean_control_share,
            "share_treated_minus_control":
                tr["d_share"] - mean_control_share,
            "control_mean_d_hl": mean_control_hl,
            "hl_treated_minus_control":
                tr["d_hl"] - mean_control_hl,
        })

    treated_df = pd.DataFrame(treated_rows)
    control_df = pd.DataFrame(control_rows)

    treated_df.to_csv(
        OUT / "B_staggered_by_treated.csv",
        index=False
    )

    control_df.to_csv(
        OUT / "B_staggered_controls.csv",
        index=False
    )

    summary = pd.DataFrame([{
        "treated_mean_d_share":
            treated_df["d_share"].mean(),

        "control_mean_d_share":
            treated_df["control_mean_d_share"].mean(),

        "mean_share_treated_minus_control":
            treated_df["share_treated_minus_control"].mean(),

        "treated_mean_d_hl":
            treated_df["d_hl"].mean(),

        "control_mean_d_hl":
            treated_df["control_mean_d_hl"].mean(),

        "mean_hl_treated_minus_control":
            treated_df["hl_treated_minus_control"].mean(),

        "n_treated":
            len(treated_df),
    }])

    summary.to_csv(
        OUT / "B_staggered_summary.csv",
        index=False
    )

    print("\nPART B — staggered spatial-integration comparison")
    print(summary.round(4).to_string(index=False))

    print("\nCommodity-level integration contrasts:")
    print(
        treated_df[
            [
                "treated",
                "treat_date",
                "d_share",
                "control_mean_d_share",
                "share_treated_minus_control",
                "d_hl",
                "control_mean_d_hl",
                "hl_treated_minus_control",
            ]
        ].round(4).to_string(index=False)
    )

    return treated_df, control_df, summary


def main():
    print("=" * 72)
    print("H3 staggered-timing robustness")
    print("=" * 72)

    part_a()
    part_b()

    print("\nOutputs written to:")
    print(OUT)


if __name__ == "__main__":
    main()
