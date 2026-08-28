"""H1 primary common-exposure DiD and robustness checks.

The final aggregate design compares five treated commodities with the fixed
nine-commodity donor pool. Observations through July 2021 form the untreated
period, August-December 2021 are excluded as the staggered transition period,
and January 2022 onward is the common treated period.

The same design is re-estimated under district-liquidity / outlier filters and
leave-one-treated-commodity-out specifications.

For each specification it reports:

1. the p-value returned by the commodity-clustered PanelOLS fit; and
2. the same clustered t statistic evaluated against a t(G-1) reference.

The second quantity is a degrees-of-freedom sensitivity check and is
labelled p_t_Gminus1.

INPUT : 02_data/clean/vol_panel_monthly.csv
OUTPUT: 04_empirics/H1_volatility/output/c1_robustness.csv
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
    H1_COMMON_POST_START,
)

ROOT = Path(__file__).resolve().parents[1]

OUTDIR = (
    ROOT /
    "04_empirics" /
    "H1_volatility" /
    "output"
)


def did(df):
    """Two-way-FE DiD on lnrv, clustered by commodity."""

    d = df.copy()

    # Drop the staggered adoption interval so that every retained treated
    # observation is either genuinely untreated or jointly exposed.
    transition = (
        (d.date >= H1_TRANSITION_START)
        &
        (d.date < H1_COMMON_POST_START)
    )
    d = d[~transition].copy()

    d["banned"] = (
        d.commodity
        .isin(FINAL_H1_TREATED)
        .astype(int)
    )

    d["unit"] = (
        d.commodity +
        "_" +
        d.district.astype(str)
    )

    d["lnrv"] = np.log(
        d.rv30.replace(0, np.nan)
    )

    d = (
        d.dropna(subset=["lnrv"])
        .set_index(["unit", "date"])
    )

    d["treat_post"] = (
        d.banned *
        (
            d.index.get_level_values("date")
            >= H1_COMMON_POST_START
        ).astype(int)
    )

    clusters = (
        d.reset_index()
        .set_index(["unit", "date"])
        .commodity
    )

    res = PanelOLS.from_formula(
        (
            "lnrv ~ treat_post + "
            "EntityEffects + TimeEffects"
        ),
        data=d
    ).fit(
        cov_type="clustered",
        clusters=clusters
    )

    b = res.params["treat_post"]
    t = res.tstats["treat_post"]

    G = int(
        clusters.nunique()
    )

    p_t_gm1 = float(
        2 *
        stats.t.sf(
            abs(t),
            df=G - 1
        )
    )

    return {
        "beta":
            round(b, 4),

        "effect_pct":
            round(
                100 * (np.exp(b) - 1),
                1
            ),

        "p_default":
            round(
                float(
                    res.pvalues["treat_post"]
                ),
                4
            ),

        "p_t_Gminus1":
            round(
                p_t_gm1,
                4
            ),

        "G_clusters":
            G,

        "nobs":
            int(res.nobs),

        "n_units":
            int(
                d.index
                .get_level_values("unit")
                .nunique()
            ),
    }


def main():
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

    df["unit"] = (
        df.commodity +
        "_" +
        df.district.astype(str)
    )

    mo = (
        df.groupby("unit")
        .size()
    )

    treated = [
        c for c in FINAL_H1_TREATED
        if c in df.commodity.unique()
    ]

    def winsor(d, p=0.99):
        d = d.copy()

        d.rv30 = np.minimum(
            d.rv30,

            d.groupby("commodity")
            .rv30
            .transform(
                lambda s:
                s.quantile(p)
            ),
        )

        return d

    specs = {
        "baseline (primary)":
            df,

        "winsorize rv30 @p99":
            winsor(df),

        "drop rv30>5 (noisy tail)":
            df[df.rv30 <= 5],

        "min 24 months/district":
            df[
                df.unit.isin(
                    mo[mo >= 24].index
                )
            ],

        "min 36 months/district":
            df[
                df.unit.isin(
                    mo[mo >= 36].index
                )
            ],

        "robust (min24 + winsor + tail)":
            winsor(
                df[
                    (df.rv30 <= 5)
                    &
                    (
                        df.unit.isin(
                            mo[mo >= 24].index
                        )
                    )
                ]
            ),
    }

    for c in treated:
        specs[f"ex-{c}"] = (
            df[
                df.commodity != c
            ]
        )

    rows = []

    print(
        f"{'spec':34s} "
        f"{'effect':>8s} "
        f"{'p_dflt':>7s} "
        f"{'p_t(G-1)':>9s} "
        f"{'G':>3s} "
        f"{'nobs':>8s}"
    )

    for name, d in specs.items():
        r = {
            "spec": name,
            **did(d)
        }

        rows.append(r)

        flag = (
            "  <- t(G-1) reference not sig"
            if r["p_t_Gminus1"] >= 0.05
            else ""
        )

        print(
            f"{name:34s} "
            f"{r['effect_pct']:+7.1f}% "
            f"{r['p_default']:6.4f} "
            f"{r['p_t_Gminus1']:8.4f} "
            f"{r['G_clusters']:3d} "
            f"{r['nobs']:8d}"
            f"{flag}"
        )

    OUTDIR.mkdir(
        parents=True,
        exist_ok=True
    )

    out = (
        OUTDIR /
        "c1_robustness.csv"
    )

    pd.DataFrame(
        rows
    ).to_csv(
        out,
        index=False
    )

    print(
        f"\nwrote {out}"
    )

    print(
        "p_t_Gminus1 is the commodity-clustered t statistic "
        "evaluated using a t(G-1) reference distribution."
    )


if __name__ == "__main__":
    main()
