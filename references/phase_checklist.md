# NBA Fantasy Decision System — Phase Checklist

## Phase 0 — Project setup

Goal: Create the GitHub repo, conda environment, folder structure, checklist, and prompt library.

Checklist:
- [ ] Create local project folder
- [ ] Create conda environment named `nba-fantasy`
- [ ] Install core Python packages
- [ ] Create project folder structure
- [ ] Create `.gitignore`
- [ ] Create `README.md`
- [ ] Create `requirements.txt`
- [ ] Create `references/phase_checklist.md`
- [ ] Create `references/prompt_library.md`
- [ ] Create individual prompt files in `prompts/`
- [ ] Initialize git
- [ ] Create GitHub repo
- [ ] Push first commit

Primary outputs:
- `README.md`
- `requirements.txt`
- `.gitignore`
- `references/phase_checklist.md`
- `references/prompt_library.md`

---

## Phase 1 — League audit

Goal: Confirm the actual Yahoo league settings and team context.

Checklist:
- [ ] Use Flaim to confirm league settings
- [ ] Confirm scoring format
- [ ] Confirm roster positions
- [ ] Confirm team roster
- [ ] Confirm standings
- [ ] Confirm available player pool access
- [ ] Save league audit notes
- [ ] Save league snapshot manually or through connector output

Primary outputs:
- `data/league_snapshots/league_audit_YYYY_MM_DD.json`
- `data/outputs/league_audit_summary.md`

Prompt used:
- `prompts/01_flaim_league_audit.md`

---

## Phase 2 — Baseline player value model

Goal: Build the first Python scoring model for 9-category fantasy value.

Checklist:
- [ ] Define standard 9 categories
- [ ] Create sample player data
- [ ] Create z-score function
- [ ] Score counting stats
- [ ] Score turnovers as negative
- [ ] Add simple FG% and FT% scoring
- [ ] Later improve FG% and FT% using volume impact
- [ ] Export baseline player rankings

Primary outputs:
- `src/nba_fantasy/scoring.py`
- `notebooks/02_player_value_model.ipynb`
- `data/processed/player_rankings.csv`

Prompt used:
- `prompts/02_player_value_model_review.md`

---

## Phase 3 — Draft assistant

Goal: Recommend best available players during the draft.

Checklist:
- [ ] Load rankings
- [ ] Track drafted players
- [ ] Track user roster
- [ ] Remove unavailable players
- [ ] Recommend best available players
- [ ] Add roster-fit logic
- [ ] Add category-need logic
- [ ] Add punt-strategy logic
- [ ] Export draft board

Primary outputs:
- `data/draft_boards/current_draft_board.csv`
- `scripts/run_draft_recommendation.py`

Prompt used:
- `prompts/03_flaim_draft_assistant.md`

---

## Phase 4 — Weekly start/sit optimizer

Goal: Recommend starts, sits, streams, and monitor players for each scoring period.

Checklist:
- [ ] Pull current roster context
- [ ] Check injuries
- [ ] Check games played this week
- [ ] Estimate weekly category output
- [ ] Recommend starts
- [ ] Recommend sits
- [ ] Identify streamers
- [ ] Save weekly report

Primary outputs:
- `data/outputs/weekly_start_sit_report.md`

Prompt used:
- `prompts/04_flaim_start_sit.md`

---

## Phase 5 — Waiver wire and drop decisions

Goal: Compare free agents against the weakest rostered players.

Checklist:
- [ ] Pull available players
- [ ] Identify best long-term adds
- [ ] Identify short-term streamers
- [ ] Identify category specialists
- [ ] Identify drop candidates
- [ ] Create add/drop pairings
- [ ] Save waiver report

Primary outputs:
- `data/outputs/waiver_wire_report.md`
- `data/outputs/drop_candidate_report.md`

Prompts used:
- `prompts/05_flaim_waiver_wire.md`
- `prompts/06_flaim_drop_candidates.md`

---

## Phase 6 — Trade analyzer

Goal: Identify and evaluate trades based on value and category fit.

Checklist:
- [ ] Analyze my team strengths and weaknesses
- [ ] Analyze opponent team needs
- [ ] Identify trade partners
- [ ] Identify buy-low players
- [ ] Identify sell-high players
- [ ] Generate proposed offers
- [ ] Evaluate incoming offers
- [ ] Save trade report

Primary outputs:
- `data/outputs/trade_recommendations.md`

Prompt used:
- `prompts/07_flaim_trade_finder.md`

---

## Phase 7 — DraftKings optional schedule context

Goal: Decide whether DraftKings adds useful schedule or game context.

Checklist:
- [ ] Test DraftKings NBA schedule output
- [ ] Compare usefulness against Flaim
- [ ] Keep only if it improves decisions
- [ ] Remove from core workflow if redundant

Primary output:
- `data/outputs/draftkings_context_test.md`

Prompt used:
- `prompts/08_draftkings_schedule_context.md`

---

## Phase 8 — Documentation and QA

Goal: Make the project reliable, understandable, and easy to resume.

Checklist:
- [ ] Update README
- [ ] Add data dictionary
- [ ] Add assumptions log
- [ ] Add known limitations
- [ ] Add tests for scoring functions
- [ ] Confirm no private data or credentials are committed
- [ ] Push final version to GitHub

Primary outputs:
- `references/data_dictionary.md`
- `references/assumptions_log.md`
- `tests/test_scoring.py`
