import pandas as pd


COUNTING_CATEGORIES = ["pts", "reb", "ast", "stl", "blk", "threes"]
PERCENTAGE_CATEGORIES = ["fg_pct", "ft_pct"]
NEGATIVE_CATEGORIES = ["to"]


def zscore(series: pd.Series) -> pd.Series:
    """Return z-scores for a numeric pandas Series."""
    std = series.std(ddof=0)
    if std == 0 or pd.isna(std):
        return series * 0
    return (series - series.mean()) / std


def add_basic_9cat_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple 9-category z-score columns.

    This is an MVP version.
    Later we will improve FG% and FT% using volume-weighted impact.
    """
    out = df.copy()

    for col in COUNTING_CATEGORIES + PERCENTAGE_CATEGORIES:
        if col in out.columns:
            out[f"{col}_z"] = zscore(out[col])

    for col in NEGATIVE_CATEGORIES:
        if col in out.columns:
            out[f"{col}_z"] = -zscore(out[col])

    z_cols = [c for c in out.columns if c.endswith("_z")]
    out["total_9cat_z"] = out[z_cols].sum(axis=1)

    return out.sort_values("total_9cat_z", ascending=False)
