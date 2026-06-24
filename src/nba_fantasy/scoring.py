import pandas as pd


COUNTING_CATEGORIES = ["pts", "reb", "ast", "stl", "blk", "threes"]
PERCENTAGE_IMPACT_CATEGORIES = ["fg_impact", "ft_impact"]
NEGATIVE_CATEGORIES = ["to"]


def zscore(series: pd.Series) -> pd.Series:
    """Return z-scores for a numeric pandas Series."""
    std = series.std(ddof=0)

    if std == 0 or pd.isna(std):
        return series * 0

    return (series - series.mean()) / std


def add_percentage_impacts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add volume-weighted FG% and FT% impact estimates.

    Simple MVP logic:
    - FG impact = (player FG% - league/player-pool average FG%) * FGA
    - FT impact = (player FT% - league/player-pool average FT%) * FTA

    This is better than scoring raw FG% and FT% because volume matters.
    """
    out = df.copy()

    if {"fg_pct", "fga"}.issubset(out.columns):
        avg_fg = out["fg_pct"].mean()
        out["fg_impact"] = (out["fg_pct"] - avg_fg) * out["fga"]

    if {"ft_pct", "fta"}.issubset(out.columns):
        avg_ft = out["ft_pct"].mean()
        out["ft_impact"] = (out["ft_pct"] - avg_ft) * out["fta"]

    return out


def add_9cat_scores(df: pd.DataFrame, punt_categories=None) -> pd.DataFrame:
    """
    Add 9-category fantasy basketball z-score values.

    Parameters
    ----------
    df:
        Player stat dataframe.
    punt_categories:
        Optional list of categories to ignore, such as ["ft_impact"] or ["to"].

    Returns
    -------
    DataFrame sorted by total 9-category value.
    """
    if punt_categories is None:
        punt_categories = []

    out = add_percentage_impacts(df)

    score_columns = []

    for col in COUNTING_CATEGORIES + PERCENTAGE_IMPACT_CATEGORIES:
        if col in out.columns and col not in punt_categories:
            z_col = f"{col}_z"
            out[z_col] = zscore(out[col])
            score_columns.append(z_col)

    for col in NEGATIVE_CATEGORIES:
        if col in out.columns and col not in punt_categories:
            z_col = f"{col}_z"
            out[z_col] = -zscore(out[col])
            score_columns.append(z_col)

    out["total_9cat_z"] = out[score_columns].sum(axis=1)

    return out.sort_values("total_9cat_z", ascending=False).reset_index(drop=True)