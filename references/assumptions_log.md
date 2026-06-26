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



\---



\## Phase 3A — Connector Integration Assumptions



Date: 2026-06-25



\### Current connector assumptions



1\. Flaim Fantasy is the primary connector for Yahoo league-specific fantasy data.

2\. Flaim can currently return league information, roster context, standings, and free agents.

3\. DraftKings is optional and currently unavailable because the NBA configuration call returned HTTP 403 Access Denied.

4\. The project should not depend on DraftKings for core functionality.

5\. Free-agent output from Flaim does not currently provide enough statistical projection data to rank players by itself.

6\. Free-agent analysis will require merging Flaim availability data with a player projection/ranking dataset.



\### Project decision



Continue with a Flaim + Python architecture.



DraftKings should only be re-tested later if schedule or matchup context becomes necessary.



\---



\## Phase 3B — Validation and Schema Assumptions



Date: 2026-06-25



\### Current validation assumptions



1\. Any player dataset used by the scoring model must include required scoring columns.

2\. The required scoring columns are:

&#x20;  - player

&#x20;  - pts

&#x20;  - reb

&#x20;  - ast

&#x20;  - stl

&#x20;  - blk

&#x20;  - threes

&#x20;  - fg\_pct

&#x20;  - fga

&#x20;  - ft\_pct

&#x20;  - fta

&#x20;  - to

3\. Scoring stat columns must be numeric.

4\. Required scoring fields cannot contain missing values.

5\. Flaim free-agent data alone is not sufficient for scoring because it does not include full statistical projections.

6\. Future waiver-wire analysis will require joining Flaim availability data to a projection or player-stat dataset.



\### Project decision



The scoring model should validate input data before calculating rankings.



Bad data should fail clearly before producing misleading fantasy rankings.



\---



\## Phase 3B — Validation and Schema Assumptions



Date: 2026-06-25



\### Current validation assumptions



1\. Any player dataset used by the scoring model must include required scoring columns.

2\. The required scoring columns are:

&#x20;  - player

&#x20;  - pts

&#x20;  - reb

&#x20;  - ast

&#x20;  - stl

&#x20;  - blk

&#x20;  - threes

&#x20;  - fg\_pct

&#x20;  - fga

&#x20;  - ft\_pct

&#x20;  - fta

&#x20;  - to

3\. Scoring stat columns must be numeric.

4\. Required scoring fields cannot contain missing values.

5\. Flaim free-agent data alone is not sufficient for scoring because it does not include full statistical projections.

6\. Future waiver-wire analysis will require joining Flaim availability data to a projection or player-stat dataset.



\### Project decision



The scoring model should validate input data before calculating rankings.



Bad data should fail clearly before producing misleading fantasy rankings.



\---



\## Phase 3C — Free-Agent Projection Join Assumptions



Date: 2026-06-25



\### Current assumptions



1\. Flaim free-agent data provides availability, player team, position, and status.

2\. Flaim free-agent data does not currently provide full fantasy stat projections.

3\. Free-agent ranking requires joining Flaim availability data to a projection dataset.

4\. Player-name matching currently uses a simple normalized name key.

5\. This name-matching approach handles simple punctuation differences such as:

&#x20;  - P.J. Washington vs PJ Washington

&#x20;  - De'Anthony Melton vs DeAnthony Melton

6\. The current projection dataset is manually created sample data.

7\. The current waiver ranking is a proof of concept, not a final recommendation engine.



\### Known limitations



1\. Name matching may fail for suffixes, nicknames, accents, or major spelling differences.

2\. The model does not yet use Yahoo player IDs for joining.

3\. The model does not yet account for my roster needs.

4\. The model does not yet compare available players against drop candidates.

5\. The model does not yet incorporate schedule volume.

6\. The model does not yet incorporate injury severity beyond retaining status labels.



\### Project decision



Use Flaim for availability and Python projection data for scoring.



The next waiver-wire version should compare ranked free agents against the weakest players on my roster.



\---



\## Phase 3D — Add/Drop Comparison Assumptions



Date: 2026-06-26



\### Current assumptions



1\. Rostered players and free agents can both be ranked with the same 9-category scoring model.

2\. Drop candidates are currently identified as the lowest projected rostered players.

3\. IL players are excluded from default drop-candidate logic because dropping them may not open an active roster slot.

4\. Add/drop recommendations are currently based on projected value delta.

5\. Positive value delta means the free agent projects better than the rostered drop candidate.

6\. This is still a proof-of-concept and should not yet be treated as final fantasy advice.



\### Known limitations



1\. The model does not yet account for category needs.

2\. The model does not yet account for positional scarcity.

3\. The model does not yet account for schedule volume.

4\. The model does not yet account for weekly matchup context.

5\. The model does not yet evaluate whether dropping an IL player is strategically acceptable.

6\. The model does not yet account for acquisition limits, waiver priority, or transaction timing.

7\. The projection data is still manually created sample data.



\### Project decision



Use projected 9-category value as the first-pass add/drop comparison.



Future versions should add category-fit logic and compare moves against the user's actual weekly matchup needs.



\---



\## Phase 3G — Recommendation Tier Assumptions



Date: 2026-06-26



\### Current assumptions



1\. Add/drop recommendations should include a decision tier, not only raw scores.

2\. The current recommendation tiers are:

&#x20;  - Strong add

&#x20;  - Moderate add

&#x20;  - Marginal add

&#x20;  - Avoid

3\. Recommendation tier is based on combined add/drop score.

4\. Confidence is based on score strength and simple injury/status flags.

5\. Injured or GTD add candidates are treated as lower-confidence recommendations.



\### Known limitations



1\. Confidence labels are rule-based and simple.

2\. Confidence does not yet account for real injury severity.

3\. Confidence does not yet account for projection source quality.

4\. Confidence does not yet account for schedule volume.

5\. Confidence does not yet account for player role volatility.

6\. Confidence does not yet account for recent news.



\### Project decision



Use recommendation tiers and confidence labels to make waiver reports easier to interpret.



Future versions should refine confidence using injury context, schedule context, minutes trends, and projection uncertainty.





\---



\## Phase 3E — Category-Fit Add/Drop Assumptions



Date: 2026-06-26



\### Current assumptions



1\. Total projected value is not enough for waiver-wire decisions.

2\. A free agent is more useful if they improve categories where the roster is weak.

3\. Team category profile is currently estimated by summing rostered players' category z-scores.

4\. Weak categories are currently the lowest team category z-score totals.

5\. Category-fit score is calculated by comparing the add player's z-score against the drop player's z-score in weak categories.

6\. Combined add/drop score is currently:



&#x20;  ```text

&#x20;  value\_delta + category\_fit\_score

