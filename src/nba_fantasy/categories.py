"""
Fantasy basketball category definitions.

This module centralizes the category names and scoring assumptions used
throughout the project.
"""

STANDARD_9CAT_CATEGORIES = [
    "pts",
    "reb",
    "ast",
    "stl",
    "blk",
    "threes",
    "fg_impact",
    "ft_impact",
    "to",
]

COUNTING_CATEGORIES = [
    "pts",
    "reb",
    "ast",
    "stl",
    "blk",
    "threes",
]

PERCENTAGE_RATE_CATEGORIES = [
    "fg_pct",
    "ft_pct",
]

PERCENTAGE_VOLUME_CATEGORIES = [
    "fga",
    "fta",
]

PERCENTAGE_IMPACT_CATEGORIES = [
    "fg_impact",
    "ft_impact",
]

NEGATIVE_CATEGORIES = [
    "to",
]

PUNT_OPTIONS = {
    "balanced": [],
    "punt_fg": ["fg_impact"],
    "punt_ft": ["ft_impact"],
    "punt_to": ["to"],
    "punt_pts": ["pts"],
    "punt_reb": ["reb"],
    "punt_ast": ["ast"],
    "punt_stl": ["stl"],
    "punt_blk": ["blk"],
    "punt_threes": ["threes"],
    "punt_fg_ft": ["fg_impact", "ft_impact"],
    "punt_ft_to": ["ft_impact", "to"],
}

CATEGORY_LABELS = {
    "pts": "Points",
    "reb": "Rebounds",
    "ast": "Assists",
    "stl": "Steals",
    "blk": "Blocks",
    "threes": "Three-pointers",
    "fg_pct": "Field goal percentage",
    "fga": "Field goal attempts",
    "fg_impact": "Field goal percentage impact",
    "ft_pct": "Free throw percentage",
    "fta": "Free throw attempts",
    "ft_impact": "Free throw percentage impact",
    "to": "Turnovers",
}


def get_punt_categories(strategy: str) -> list[str]:
    """
    Return the categories excluded under a punt strategy.
    """
    if strategy not in PUNT_OPTIONS:
        valid = ", ".join(PUNT_OPTIONS.keys())
        raise ValueError(f"Unknown punt strategy: {strategy}. Valid options: {valid}")

    return PUNT_OPTIONS[strategy]