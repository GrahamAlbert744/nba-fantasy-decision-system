# Flaim Prompt — Live Data Capture Instructions

Use this when transitioning from pasted sample snapshots to live connector snapshots.

```text
Use Flaim to retrieve my current Yahoo fantasy basketball league data.

Use platform="yahoo", sport="basketball", leagueId="466.l.3706", teamId="9", seasonYear=2025.

Retrieve and summarize:
1. League settings
2. My roster
3. Free agents
4. Standings
5. Current matchup, if available
6. Recent transactions, if available

For each output, identify which local file it should be saved to:
- data/raw/flaim_league_raw_YYYY_MM_DD.json
- data/raw/flaim_roster_raw_YYYY_MM_DD.json
- data/raw/flaim_free_agents_raw_YYYY_MM_DD.json
- data/league_snapshots/flaim_roster_snapshot_YYYY_MM_DD.csv
- data/league_snapshots/flaim_free_agents_snapshot_YYYY_MM_DD.csv

Also list any fields that are missing, null, or unreliable.
```
