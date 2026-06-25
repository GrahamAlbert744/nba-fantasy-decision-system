\# Data Dictionary



This file defines the main fields used in the NBA Fantasy Decision System.



\## Player identity fields



| Field | Definition |

|---|---|

| player | Player name |

| team | NBA team abbreviation |

| position | Fantasy/NBA eligible positions |

| player\_id | Optional player identifier from Yahoo, Flaim, or another source |



\## Counting stat fields



| Field | Definition |

|---|---|

| pts | Points per game |

| reb | Rebounds per game |

| ast | Assists per game |

| stl | Steals per game |

| blk | Blocks per game |

| threes | Made three-pointers per game |

| to | Turnovers per game |



\## Percentage fields



| Field | Definition |

|---|---|

| fg\_pct | Field goal percentage |

| fga | Field goal attempts per game |

| ft\_pct | Free throw percentage |

| fta | Free throw attempts per game |



\## Derived percentage impact fields



| Field | Definition |

|---|---|

| fg\_impact | Volume-weighted field goal percentage impact |

| ft\_impact | Volume-weighted free throw percentage impact |



\## Z-score fields



| Field | Definition |

|---|---|

| pts\_z | Points z-score |

| reb\_z | Rebounds z-score |

| ast\_z | Assists z-score |

| stl\_z | Steals z-score |

| blk\_z | Blocks z-score |

| threes\_z | Three-pointers z-score |

| fg\_impact\_z | FG% impact z-score |

| ft\_impact\_z | FT% impact z-score |

| to\_z | Turnover z-score, inverted so fewer turnovers are better |

| total\_9cat\_z | Total fantasy value across included categories |



\## Punt strategy fields



| Field | Definition |

|---|---|

| punt\_strategy | Named strategy used to exclude one or more categories |

| punt\_categories | Specific categories excluded from total value |

