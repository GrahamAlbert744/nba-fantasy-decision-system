# NBA Fantasy Decision System — Prompt Library

This folder contains reusable prompts for the NBA Fantasy Decision System.

Use these prompts with the Flaim Fantasy connector first. DraftKings is optional and should only be used if it adds useful NBA schedule or team-game context.

## Default league parameters

Use these values unless the league changes:

```text
platform="yahoo"
sport="basketball"
leagueId="466.l.3706"
teamId="9"
seasonYear=2025
leagueName="Lou Williams Memorial League"
teamName="Dame Time Management"
```

## Recommended use by phase

| File | Phase | Purpose |
|---|---:|---|
| flaim_league_audit.md | 1 | Confirm league settings, roster, standings, and risks |
| flaim_roster_snapshot.md | 3I+ | Pull current roster context for snapshot creation |
| flaim_free_agent_snapshot.md | 3I+ | Pull available players for waiver analysis |
| flaim_waiver_wire.md | 3+ / 5 | Identify add candidates and streamers |
| flaim_drop_candidates.md | 3+ / 5 | Identify weak rostered players and possible drops |
| flaim_start_sit.md | 4 | Weekly lineup decisions |
| flaim_weekly_matchup_audit.md | 4 | Weekly category and opponent context |
| flaim_trade_finder.md | 6 | Find trade partners and proposed offers |
| flaim_trade_offer_evaluator.md | 6 | Evaluate incoming or proposed trades |
| flaim_injury_role_monitor.md | 4/5/6 | Injury, minutes, and role risk review |
| flaim_draft_assistant.md | Draft | Draft-time recommendations |
| draftkings_schedule_context.md | Optional | Schedule density, back-to-backs, team context |
| project_audit.md | QA | Review project completeness and missing pieces |

## Usage note

These prompts are meant to complement the Python workflow, not replace it. Python should remain the source of truth for repeatable scoring, saved snapshots, reports, and run manifests.
