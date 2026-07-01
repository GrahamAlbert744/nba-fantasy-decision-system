# Flaim Prompt — Roster Snapshot

Use this before running local waiver, start/sit, or trade analysis.

```text
Pull my current Yahoo fantasy basketball roster.

Use platform="yahoo", sport="basketball", leagueId="466.l.3706", teamId="9", seasonYear=2025.

Return a structured roster snapshot with these fields for each player:
1. playerKey
2. playerId
3. player name
4. NBA team
5. eligible fantasy positions
6. selected roster slot
7. injury/status flag
8. any available ownership or availability metadata

Also include:
- leagueKey
- teamKey
- teamName
- ownerName
- current week or scoring period, if available

Format the output so I can convert it into a local CSV or JSON snapshot for:
data/league_snapshots/
```
