\# Assumptions Log



This file tracks modeling assumptions, limitations, and future improvements for the NBA Fantasy Decision System.



\## Phase 2 — Baseline Player Value Model



Date: 2026-06-24



\### Current scoring assumptions



1\. The league is treated as a standard Yahoo 9-category fantasy basketball league.

2\. The core categories are:

&#x20;  - Points

&#x20;  - Rebounds

&#x20;  - Assists

&#x20;  - Steals

&#x20;  - Blocks

&#x20;  - Three-pointers

&#x20;  - Field goal percentage

&#x20;  - Free throw percentage

&#x20;  - Turnovers

3\. Counting categories are scored with z-scores.

4\. Turnovers are treated as a negative category.

5\. FG% and FT% are not scored as raw percentages.

6\. FG% impact is estimated as:



&#x20;  ```text

&#x20;  (player FG% - player-pool average FG%) \* FGA

