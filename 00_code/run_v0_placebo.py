"""H1 falsification and pre-treatment validation checks.

The checks match the final common-exposure aggregate DiD.

1. PLACEBO COMMON-EXPOSURE DESIGN
   Only genuinely untreated observations are used (before August 2021).
   A fake Aug-Dec 2019 transition period is removed and January 2020 is
   treated as a fake common-post start.

2. JOINT PRE-TREND TEST
   Genuine untreated months -18 through -1 are measured relative to
   August 2021, the earliest real suspension month. July 2021 (m=-1)
   is the reference period. The tested bins are:
       -18..-13
       -12..-7
       -6..-2

No observations are clipped into endpoint bins.

Inference is clustered at the commodity level. In addition to the PanelOLS
Wald p-value, the joint test is evaluated against an F(q, G-1) reference
distribution as a transparent few-cluster sensitivity check.

INPUT : 02_data/clean/vol_panel_monthly.csv
OUTPUT: 04_empirics/V0_lost_results_replication/output/placebo_results.txt
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from linearmodels.panel import PanelOLS

from utils import (
    FINAL_H1_TREATED,
    FINAL_H1_COMMODITIES,
    H1_TRANSITION_START,
)


ROOT = Path(__file__).resolve().parents[1]

OUTDIR = (
    ROOT /
    "04_empirics" /
    "V0_lost_results_replication" /
    "output"
)

FAKE_TRANSITION_START = pd.Timestamp(
    "2019-08-01"
)

FAKE_COMMON_POST_START = pd.Timestamp(
    "2020-01-01"
)


def load():
    df = pd.read_csv(
        ROOT /
        "02_data" /
        "clean" /
        "vol_panel_monthly.csv",
        parse_dates=["date"],
    )

    df = df[
        df.commodity.isin(
            FINAL_H1_COMMODITIES
        )
    ].copy()

    df["banned"] = (
        df.commodity
        .isin(FINAL_H1_TREATED)
        .astype(int)
    )

    df["unit"] = (
        df.commodity +
        "_" +
        df.district.astype(str)
    )

    df["lnrv"] = np.log(
        df.rv30.replace(0, np.nan)
    )

    return df.dropna(
        subset=["lnrv"]
    ).copy()


def relative_month(date):
    return (
        (date.dt.year - H1_TRANSITION_START.year) * 12
        +
        (date.dt.month - H1_TRANSITION_START.month)
    )


def main():
    OUTDIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = []
    df = load()

    # ========================================================
    # 1. PLACEBO COMMON-EXPOSURE DESIGN
    # ========================================================

    placebo = df[
        df.date < H1_TRANSITION_START
    ].copy()

    fake_transition = (
        (placebo.date >= FAKE_TRANSITION_START)
        &
        (placebo.date < FAKE_COMMON_POST_START)
    )

    placebo = placebo[
        ~fake_transition
    ].copy()

    placebo["treat_post"] = (
        placebo.banned *
        (
            placebo.date >=
            FAKE_COMMON_POST_START
        ).astype(int)
    )

    placebo_idx = placebo.set_index(
        ["unit", "date"]
    )

    placebo_clusters = (
        placebo_idx.commodity
    )

    res = PanelOLS.from_formula(
        (
            "lnrv ~ treat_post + "
            "EntityEffects + TimeEffects"
        ),
        data=placebo_idx,
    ).fit(
        cov_type="clustered",
        clusters=placebo_clusters,
    )

    b = res.params[
        "treat_post"
    ]

    t_stat = res.tstats[
        "treat_post"
    ]

    G_placebo = int(
        placebo_clusters.nunique()
    )

    p_t_gm1 = float(
        2 *
        stats.t.sf(
            abs(t_stat),
            df=G_placebo - 1,
        )
    )

    lines.append(
        "PLACEBO "
        "(fake transition Aug-Dec 2019 excluded; "
        "fake post Jan 2020; actual-treatment data excluded): "
        f"beta={b:.4f} "
        f"({100 * (np.exp(b) - 1):+.1f}%), "
        f"p={res.pvalues['treat_post']:.4f}, "
        f"p_t(G-1)={p_t_gm1:.4f}"
    )

    lines.append(
        "  pass rule: approximately zero and statistically "
        "insignificant; a placebo effect would weaken the design."
    )

    # ========================================================
    # 2. JOINT PRE-TREND TEST
    # ========================================================

    pre = df[
        df.date < H1_TRANSITION_START
    ].copy()

    pre["rel_m"] = relative_month(
        pre.date
    )

    # Genuine 18-month pre-treatment window only.
    # Nothing earlier than -18 is collapsed into the first bin.
    pre = pre[
        (pre.rel_m >= -18)
        &
        (pre.rel_m <= -1)
    ].copy()

    pre["lead_bin"] = pd.cut(
        pre.rel_m,
        bins=[
            -19,
            -13,
            -7,
            -2,
        ],
        labels=[
            "lead_18_13",
            "lead_12_7",
            "lead_6_2",
        ],
    )

    bins = (
        pd.get_dummies(
            pre.lead_bin,
            dtype=float,
        )
        .mul(
            pre.banned,
            axis=0,
        )
    )

    idx = pre.set_index(
        ["unit", "date"]
    ).index

    X = bins.set_index(idx)

    pre_idx = pre.set_index(
        ["unit", "date"]
    )

    clusters = (
        pre_idx.commodity
    )

    es = PanelOLS(
        pre_idx.lnrv,
        X,
        entity_effects=True,
        time_effects=True,
    ).fit(
        cov_type="clustered",
        clusters=clusters,
    )

    lead_cols = [
        "lead_18_13",
        "lead_12_7",
        "lead_6_2",
    ]

    R = np.zeros(
        (
            len(lead_cols),
            len(es.params),
        )
    )

    for i, c in enumerate(
        lead_cols
    ):
        R[
            i,
            list(es.params.index).index(c),
        ] = 1.0

    w = es.wald_test(
        restriction=R,
        value=np.zeros(
            len(lead_cols)
        ),
    )

    q = len(lead_cols)

    G = int(
        clusters.nunique()
    )

    # The PanelOLS Wald statistic has an asymptotic chi-square
    # reference. As a transparent small-cluster sensitivity,
    # divide by q and compare with F(q, G-1).
    f_ref = float(
        w.stat
    ) / q

    p_f_ref = float(
        stats.f.sf(
            f_ref,
            q,
            G - 1,
        )
    )

    for c in lead_cols:
        lines.append(
            f"  {c}: "
            f"beta={es.params[c]:+.4f}, "
            f"p={es.pvalues[c]:.4f}"
        )

    lines.append(
        "JOINT LEAD TEST "
        "(3 half-year lead bins = 0): "
        f"stat={float(w.stat):.2f}, "
        f"p={float(w.pval):.4f}, "
        f"F_ref={f_ref:.2f}, "
        f"p_F(3,{G - 1})={p_f_ref:.4f}"
    )

    if p_f_ref < 0.05:
        lines.append(
            "  interpretation: parallel pre-trends are rejected "
            "under the small-cluster F reference; the DiD "
            "coefficient should not be interpreted causally."
        )
    else:
        lines.append(
            "  interpretation: the small-cluster F reference does "
            "not reject the joint pre-trend restriction, although "
            "this does not prove parallel trends."
        )

    out = "\n".join(
        lines
    )

    (
        OUTDIR /
        "placebo_results.txt"
    ).write_text(
        out + "\n"
    )

    print(out)


if __name__ == "__main__":
    main()
