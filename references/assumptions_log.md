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





\---



\## Phase 3H — Reusable Waiver Workflow Assumptions



Date: 2026-06-26



\### Current assumptions



1\. The waiver-wire process should be runnable from one script.

2\. The workflow currently uses sample free-agent, roster, and projection CSVs.

3\. The workflow produces a markdown report in `data/outputs/`.

4\. The workflow uses balanced 9-category scoring by default.

5\. The workflow can later support other punt strategies by changing the `punt\_strategy` argument.



\### Known limitations



1\. The workflow is not yet pulling live Flaim data directly into local CSVs.

2\. The workflow still depends on manually created sample projection data.

3\. The workflow does not yet include schedule volume.

4\. The workflow does not yet include live matchup context.

5\. The workflow does not yet include transaction limits or waiver priority.



\### Project decision



Use `scripts/run\_waiver\_analysis.py` as the main reusable waiver-wire entry point.



Future versions should replace sample CSV inputs with live Flaim snapshots and real projection data.


---

## Phase 3I — Flaim Snapshot Assumptions

Date: 2026-06-28

### Current assumptions

1. Flaim roster and free-agent responses should be converted into local dataframe snapshots.
2. Snapshot files should retain Yahoo/Flaim identifiers such as `player_key` and `player_id`.
3. Snapshot files should retain player metadata such as team, position, status, and roster slot.
4. Free-agent snapshots should retain `percent_owned` when available, even though current values may be null.
5. Local snapshots are a bridge between live connector output and the Python analysis pipeline.

### Known limitations

1. The current snapshot builder uses manually pasted Flaim response examples.
2. The workflow does not yet call Flaim directly from Python.
3. The current projections are still sample data.
4. The waiver pipeline does not yet consume snapshot files directly.
5. Snapshot filenames are currently sample names, not date-stamped production names.

### Project decision

Use `src/nba_fantasy/snapshots.py` as the conversion layer between Flaim connector output and local CSV snapshots.

Future versions should date-stamp snapshots and feed them into the waiver analysis workflow.

---

## Phase 3K — Date-Stamped Waiver Report Assumptions

Date: 2026-06-29

### Current assumptions

1. Each waiver analysis run should produce a dated archive report.
2. The workflow should also maintain a stable latest report named `waiver_wire_report.md`.
3. Dated reports make it easier to compare recommendations across time.
4. The workflow still uses Flaim-style sample snapshot CSVs and sample projections.

### Known limitations

1. Snapshot files are not yet date-stamped automatically.
2. The workflow does not yet save dated intermediate ranked-player CSVs.
3. The workflow does not yet include live schedule, matchup, or transaction context.
4. The workflow still depends on sample projection data.

### Project decision

Use dated markdown reports for archived waiver analysis runs, while keeping `waiver_wire_report.md` as the latest human-readable output.


---

## Phase 3L — Date-Stamped Flaim Snapshot Assumptions

Date: 2026-06-29

### Current assumptions

1. Flaim-style roster and free-agent snapshots should be archived with dated filenames.
2. Stable latest snapshot files should also be maintained for the reusable waiver workflow.
3. Dated snapshots make it easier to trace which inputs produced each waiver report.
4. The current snapshot builder still uses pasted Flaim response examples.

### Known limitations

1. The snapshot builder does not yet call Flaim directly from Python.
2. The snapshot builder does not yet save raw JSON responses.
3. The workflow does not yet automatically pair a specific dated snapshot with a specific dated report.
4. Projection data is still manually created sample data.

### Project decision

Maintain both dated archive snapshots and stable latest snapshot files in `data/league_snapshots/`.

Future versions should save raw Flaim responses, dated CSV snapshots, and dated reports from the same run.



---

## Phase 3N — Prompt Library Integration Assumptions

Date: 2026-07-01

### Current assumptions

1. Connector prompts should be saved as reusable Markdown files in `prompts/`.
2. Flaim Fantasy remains the primary connector for Yahoo league context.
3. DraftKings remains optional and should only be used if it adds useful schedule or team context.
4. Prompt files are part of the project workflow, not throwaway chat text.
5. Prompt outputs should eventually be saved into `data/outputs/`, `data/raw/`, or `data/league_snapshots/` depending on the output type.

### Prompt files added

- `prompts/flaim_league_audit.md`
- `prompts/flaim_roster_snapshot.md`
- `prompts/flaim_free_agent_snapshot.md`
- `prompts/flaim_waiver_wire.md`
- `prompts/flaim_drop_candidates.md`
- `prompts/flaim_start_sit.md`
- `prompts/flaim_weekly_matchup_audit.md`
- `prompts/flaim_trade_finder.md`
- `prompts/flaim_trade_offer_evaluator.md`
- `prompts/flaim_injury_role_monitor.md`
- `prompts/flaim_draft_assistant.md`
- `prompts/draftkings_schedule_context.md`
- `prompts/flaim_live_data_capture_instructions.md`
- `prompts/flaim_projection_gap_review.md`
- `prompts/project_audit.md`

### Known limitations

1. The prompts are reusable templates, not automated connector calls.
2. The project still needs raw Flaim JSON saving.
3. The project still needs real player projection ingestion.
4. The project still needs live schedule and matchup context.
5. Prompt outputs still need a standard save location and naming convention.

### Project decision

Treat `prompts/` as the project’s reusable connector instruction library.

Future versions should connect prompt outputs to saved raw JSON, CSV snapshots, and dated markdown reports.


---

## Phase 3P — Raw JSON Paths in Waiver Manifest Assumptions

Date: 2026-07-01

### Current assumptions

1. Waiver run manifests should record both raw connector inputs and transformed CSV snapshots.
2. Raw Flaim-style JSON files are saved in `data/raw/`.
3. Transformed Flaim-style CSV snapshots are saved in `data/league_snapshots/`.
4. Projection files remain in `data/interim/` for now.
5. Report files remain in `data/outputs/`.
6. Run manifests remain in `data/run_manifests/`.

### Known limitations

1. Raw JSON files are still sample Flaim-style responses, not direct live API captures.
2. The manifest records file paths but does not yet compute file hashes.
3. The manifest does not yet record Git commit hash.
4. The manifest does not yet record Python or package versions.
5. The manifest does not yet record Flaim connector request metadata.

### Project decision

Use the waiver run manifest as the central reproducibility record connecting raw inputs, transformed inputs, projection inputs, outputs, and model parameters.

Future versions should add file hashes, Git commit hash, environment metadata, and connector request metadata.


---

## Phase 3Q — File Hashes in Waiver Manifest Assumptions

Date: 2026-07-02

### Current assumptions

1. Waiver run manifests should record file metadata for raw inputs, transformed inputs, projection inputs, and outputs.
2. File metadata should include path, existence status, file size, and SHA-256 hash.
3. SHA-256 hashes make it easier to detect whether a file changed after a report was generated.
4. Hashes support reproducibility and debugging.

### Known limitations

1. The manifest still does not record Git commit hash.
2. The manifest still does not record Python version.
3. The manifest still does not record package versions.
4. The manifest still does not record Flaim connector request metadata.
5. The manifest still uses sample raw JSON and sample projection data.

### Project decision

Use SHA-256 file hashes as the first reproducibility check for waiver-analysis inputs and outputs.

Future versions should add Git commit hash and environment metadata.

---

## Phase 3R — Git and Environment Metadata in Waiver Manifest Assumptions

Date: 2026-07-02

### Current assumptions

1. Waiver run manifests should record Git metadata, environment metadata, input files, output files, parameters, file sizes, and SHA-256 hashes.
2. Git metadata should include the current commit hash, branch, and dirty working-tree status.
3. Environment metadata should include the creation timestamp, project root, script name, command, Python version, Python executable, pandas version, and platform/system information.
4. The manifest is now the central reproducibility record for a waiver-analysis run.
5. `git_is_dirty` may be true during active development before files are committed.

### Known limitations

1. The manifest records pandas version but does not yet record the full package environment.
2. The manifest does not yet export `pip freeze`.
3. The manifest does not yet export a conda environment file.
4. The manifest does not yet record live Flaim connector request metadata.
5. The workflow still uses sample raw JSON, sample snapshots, and sample projection data.

### Project decision

Use Git metadata and environment metadata to make waiver reports easier to reproduce, debug, and audit.

Future versions should add full package manifests, real projection ingestion, schedule context, and live Flaim connector capture metadata.

---

## Phase 3S — Package Environment Export Assumptions

Date: 2026-07-02

### Current assumptions

1. Waiver run manifests should record package/environment exports in addition to Git and platform metadata.
2. Each waiver run should save a dated `pip freeze` export.
3. Each waiver run should attempt to save a dated `conda env export --no-builds` export.
4. The manifest should record file metadata and SHA-256 hashes for both environment export files.
5. If a package export command fails, the failure output should still be saved to a file for debugging.

### Known limitations

1. The environment export files may include platform-specific package details.
2. `conda env export` may fail if conda is not available in the active shell.
3. The workflow still uses sample raw JSON, sample snapshots, and sample projection data.
4. The manifest still does not record live Flaim connector request metadata.
5. The workflow still does not include real projection ingestion, schedule context, or matchup context.

### Project decision

Use `pip freeze` and `conda env export --no-builds` as reproducibility artifacts for each waiver-analysis run.

Future versions should add live Flaim connector metadata and real projection ingestion.