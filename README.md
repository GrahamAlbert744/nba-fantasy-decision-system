# NBA Fantasy Decision System

A Python + connector-assisted decision system for making data-informed decisions in a Yahoo NBA fantasy basketball league.

This project is designed to support a full fantasy basketball season, including draft preparation, weekly lineup decisions, waiver-wire decisions, drop decisions, and trade evaluation.

The project uses Python for repeatable analysis and decision logic, while using fantasy connectors to ground recommendations in actual league context.

---

## Project Purpose

The goal of this project is to build a practical decision-support system for a Yahoo NBA 9-category fantasy basketball league.

The system should help answer questions such as:

1. Which players should I draft?
2. Which available players are the best fit for my roster?
3. Which players should I start or sit each week?
4. Which free agents should I add?
5. Which players should I drop?
6. Which trades should I propose?
7. Which incoming trade offers should I accept, reject, or counter?
8. Which categories is my team strong or weak in?
9. How should injuries, schedule volume, and player role changes affect decisions?

---

## Current League Context

The initial test league is:

- Platform: Yahoo
- Sport: Basketball
- League: Lou Williams Memorial League
- Team: Dame Time Management
- Owner: Graham
- League ID: `466.l.3706`
- Team ID: `9`
- Season: 2025-26
- Number of teams: 10
- Scoring type: Head-to-head

The connected Yahoo season is currently complete, so early development uses this league as a historical test case. Once the next season begins, the same project structure can be reused for live draft and roster management decisions.

---

## Core Fantasy Format

This project assumes a standard Yahoo 9-category fantasy basketball format unless league settings indicate otherwise.

Expected categories:

1. Points
2. Rebounds
3. Assists
4. Steals
5. Blocks
6. Three-pointers
7. Field goal percentage
8. Free throw percentage
9. Turnovers

The scoring model will begin with basic z-score category values, then improve over time by adding volume-weighted percentage impact, punt strategy support, replacement value, injury risk, and schedule effects.

---

## Main Decision Modules

### 1. Draft Assistant

Purpose: Recommend the best available players during the draft.

The draft assistant should:

- Rank players by projected 9-category value
- Account for players already drafted
- Track my current roster construction
- Identify category strengths and weaknesses
- Recommend the best available player
- Provide backup picks
- Support punt strategies
- Flag injury, role, and shutdown risks

---

### 2. Weekly Start/Sit Optimizer

Purpose: Help decide who should start, sit, stream, or be monitored each scoring period.

The weekly optimizer should consider:

- Games played during the scoring period
- Injuries and game-time decisions
- Player role and minutes trends
- Category needs
- Positional eligibility
- Streaming opportunities
- Opponent matchup context

Possible player labels:

- Start
- Sit
- Stream
- Hold
- Monitor
- Injury watch
- Drop candidate

---

### 3. Waiver Wire Analyzer

Purpose: Identify available players who improve the team.

The waiver tool should identify:

- Best long-term adds
- Best short-term streamers
- Best category specialists
- Best injury replacements
- Best upside stashes
- Add/drop pairings

---

### 4. Drop Candidate Detector

Purpose: Identify rostered players who may no longer be worth holding.

Players should be classified as:

- Must hold
- Hold
- Monitor
- Replaceable
- Drop if better option exists
- Drop now

The system should compare weak rostered players against available free agents before recommending a drop.

---

### 5. Trade Analyzer

Purpose: Identify and evaluate trade opportunities.

The trade analyzer should:

- Compare my category strengths and weaknesses against other teams
- Identify sell-high players
- Identify buy-low targets
- Find logical trade partners
- Generate proposed trade offers
- Evaluate incoming trade offers
- Estimate category impact before and after a trade
- Flag overpay, injury, and fit risk

---

## Data Sources

### Primary Source: Flaim Fantasy Connector

Flaim is the primary connector for actual Yahoo league context.

It may be used for:

- League settings
- Team roster
- Standings
- Matchups
- Available players
- Recent transactions
- Player search
- Team and owner context

### Optional Source: DraftKings Connector

DraftKings is optional and should only be used if it adds useful NBA schedule or team-game context.

Potential use cases:

- NBA schedule density
- Back-to-back checks
- Recent team results
- Team-level matchup context

DraftKings should not be treated as the core fantasy ranking source unless player-level fantasy projections become available.

### Python / Local Data

Python will be used to store and process:

- League snapshots
- Player rankings
- Player projections
- Category z-scores
- Draft boards
- Weekly start/sit reports
- Waiver-wire reports
- Trade evaluations
- Injury/status notes
- Prompt outputs

---

## Project Structure

```text
nba-fantasy-decision-system/
│
├── README.md
├── .gitignore
├── requirements.txt
├── .env.example
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── external/
│   ├── league_snapshots/
│   ├── draft_boards/
│   └── outputs/
│
├── notebooks/
│
├── src/
│   └── nba_fantasy/
│       ├── __init__.py
│       ├── config.py
│       ├── scoring.py
│       ├── categories.py
│       ├── draft.py
│       ├── roster.py
│       ├── waiver.py
│       ├── trades.py
│       ├── schedule.py
│       ├── injuries.py
│       ├── data_quality.py
│       └── utils.py
│
├── scripts/
│
├── prompts/
│
├── references/
│   ├── phase_checklist.md
│   └── prompt_library.md
│
├── reports/
│   └── figures/
│
└── tests/