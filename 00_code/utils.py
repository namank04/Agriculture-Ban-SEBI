"""Shared utilities — agri ban project. Python 3.10+."""
import numpy as np
import pandas as pd

BAN_DATE = pd.Timestamp("2021-12-20")
BANNED = ["wheat", "chana", "cpo", "mustard", "soybean", "paddy", "moong"]
CORE = ["wheat", "chana", "cpo"]
CONTROL_CANDIDATES = ["guar", "castor", "turmeric", "jeera", "cotton"]
# Excluded from the PRIMARY C1 analysis (decision_log 2026-06-21):
#   paddy — MSP price-censored: 40.3% of daily returns are exactly flat (vs 1-6% for clean
#           commodities) because FCI/state procurement pins the spot price at the support
#           level for large stretches; realized vol on a government-administered price is a
#           mechanical artifact, not market volatility. Dropped from primary; not a control.
#   guar  — CEDA id 75 is gum-contaminated (corr 0.04 vs guar futures); the clean guar
#           underlying is guarseed413 (id 413, corr 0.99). Drop id 75 from controls.
EXCLUDE_PRIMARY = ["paddy", "guar"]

def trading_days_only(dates) -> pd.Series:
    """Boolean mask keeping weekday (Mon-Fri) observations only.

    Mandi spot files behave like 7-day CALENDAR grids: across hundreds of districts
    some market reports on nearly every calendar day, including weekends. Computing
    log returns across carried weekend rows while annualizing realized_vol by
    sqrt(252) *trading* days is a units mismatch (the 'calendar-grid' artifact flagged
    2026-06-13). Restricting to weekdays aligns the return frequency with the
    annualization. An exchange-holiday calendar is an optional further refinement.
    Authorized 2026-06-21 (researcher: 'clean it properly')."""
    return pd.to_datetime(dates).dt.dayofweek < 5

def log_returns(price: pd.Series) -> pd.Series:
    return np.log(price).diff()

def realized_vol(returns: pd.Series, window: int = 30, annualize: bool = True) -> pd.Series:
    """Rolling std of log returns; annualized with 252 trading days."""
    rv = returns.rolling(window, min_periods=int(window * 0.8)).std()
    return rv * np.sqrt(252) if annualize else rv

def parkinson_vol(high: pd.Series, low: pd.Series, window: int = 30) -> pd.Series:
    """Parkinson (1980) high-low estimator, rolling, annualized."""
    hl = (np.log(high / low)) ** 2 / (4 * np.log(2))
    return np.sqrt(hl.rolling(window).mean() * 252)

def make_post_dummy(idx: pd.DatetimeIndex, ban_date=BAN_DATE) -> pd.Series:
    return (idx >= ban_date).astype(int)

def winsorize(s: pd.Series, p: float = 0.01) -> pd.Series:
    lo, hi = s.quantile(p), s.quantile(1 - p)
    return s.clip(lo, hi)
