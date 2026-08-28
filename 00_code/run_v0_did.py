"""H1 primary aggregate DiD and pre-treatment event-study diagnostic.

Primary common-exposure design:
    <= Jul 2021 : all five treated commodities are genuinely untreated
    Aug-Dec 2021: staggered transition period, excluded
    >= Jan 2022 : all five treated commodities are suspended

The event-study figure is a pre-treatment diagnostic only. It uses genuine
months -18 through -1 relative to August 2021, with month -1 omitted.

INPUT : 02_data/clean/vol_panel_monthly.csv
OUTPUT: 04_empirics/V0_lost_results_replication/output/
        {did_results.txt, event_study.png}
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

from utils import (
    FINAL_H1_TREATED,
    FINAL_H1_COMMODITIES,
    H1_TRANSITION_START,
    H1_COMMON_POST_START,
)


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = (
    ROOT /
    "04_empirics" /
    "V0_lost_results_replication" /
    "output"
)


def load(panel_name):
    df = pd.read_csv(
        ROOT / "02_data" / "clean" / panel_name,
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
    panel_name = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "vol_panel_monthly.csv"
    )

    suffix = (
        f"_{sys.argv[2]}"
        if len(sys.argv) > 2
        else ""
    )

    drop = set(sys.argv[3:])

    df = load(panel_name)

    if drop:
        df = df[
            ~df.commodity.isin(drop)
        ].copy()

        print(
            f"dropped: {sorted(drop)}"
        )

    # --------------------------------------------------------
    # Primary common-exposure DiD
    # --------------------------------------------------------

    transition = (
        (df.date >= H1_TRANSITION_START)
        &
        (df.date < H1_COMMON_POST_START)
    )

    did = df[
        ~transition
    ].copy()

    did["treat_post"] = (
        did.banned *
        (
            did.date >= H1_COMMON_POST_START
        ).astype(int)
    )

    did_idx = did.set_index(
        ["unit", "date"]
    )

    clusters = (
        did_idx
        .commodity
    )

    res = PanelOLS.from_formula(
        (
            "lnrv ~ treat_post + "
            "EntityEffects + TimeEffects"
        ),
        data=did_idx,
    ).fit(
        cov_type="clustered",
        clusters=clusters,
    )

    OUTDIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    result_text = "\n".join(
        line.rstrip()
        for line in str(res).splitlines()
    ) + "\n"

    (
        OUTDIR /
        f"did_results{suffix}.txt"
    ).write_text(
        result_text
    )

    beta = res.params[
        "treat_post"
    ]

    print(
        "Primary common-exposure DiD:"
    )

    print(
        "  pre        : through Jul 2021"
    )

    print(
        "  transition : Aug-Dec 2021 excluded"
    )

    print(
        "  post       : Jan 2022 onward"
    )

    print(
        f"  beta       : {beta:.6f}"
    )

    print(
        "  effect     : "
        f"{100 * (np.exp(beta) - 1):+.2f}%"
    )

    print(
        "  clustered p: "
        f"{res.pvalues['treat_post']:.4f}"
    )

    # --------------------------------------------------------
    # Pre-treatment monthly event-study diagnostic
    # --------------------------------------------------------

    pre = df[
        df.date < H1_TRANSITION_START
    ].copy()

    pre["rel_m"] = relative_month(
        pre.date
    )

    pre = pre[
        (pre.rel_m >= -18)
        &
        (pre.rel_m <= -1)
    ].copy()

    dummies = pd.get_dummies(
        pre.rel_m,
        prefix="m",
        dtype=float,
    )

    # July 2021 (m=-1) is the reference month.
    dummies = dummies.drop(
        columns=["m_-1"]
    )

    inter = dummies.mul(
        pre.banned,
        axis=0,
    )

    idx = pre.set_index(
        ["unit", "date"]
    ).index

    X = inter.set_index(idx)

    es = PanelOLS(
        pre.set_index(
            ["unit", "date"]
        ).lnrv,
        X,
        entity_effects=True,
        time_effects=True,
    ).fit(
        cov_type="clustered",
        clusters=pre.set_index(
            ["unit", "date"]
        ).commodity,
    )

    coefs = es.params.filter(
        like="m_"
    )

    order = sorted(
        coefs.index,
        key=lambda c:
            int(c.split("_")[1]),
    )

    xs = [
        int(c.split("_")[1])
        for c in order
    ]

    plt.figure(
        figsize=(9, 4)
    )

    plt.axhline(
        0,
        linewidth=0.5,
    )

    plt.errorbar(
        xs,
        coefs[order],
        yerr=1.96 * es.std_errors[order],
        fmt="o",
        markersize=3,
    )

    plt.xlabel(
        "months before earliest suspension"
    )

    plt.ylabel(
        "treated-control log-volatility difference"
    )

    plt.title(
        "Pre-treatment event-study diagnostic"
    )

    plt.tight_layout()

    plt.savefig(
        OUTDIR /
        f"event_study{suffix}.png",
        dpi=150,
    )

    print(
        "Pre-trend figure: genuine months "
        "-18 through -2; July 2021 (m=-1) omitted."
    )


if __name__ == "__main__":
    main()
