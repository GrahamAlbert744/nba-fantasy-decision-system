# Flaim Prompt — Free-Agent Snapshot

Use this before waiver-wire analysis.

```text
Pull a current free-agent list from my Yahoo fantasy basketball league.

Use platform="yahoo", sport="basketball", leagueId="466.l.3706", teamId="9", seasonYear=2025.

Return at least 25 available players if possible.

For each player include:
1. playerKey
2. playerId
3. player name
4. NBA team
5. eligible positions
6. injury/status flag
7. percent owned, if available
8. availability/free-agent status

Also include the league name and league key.

Format the output so I can convert it into a local CSV or JSON snapshot for:
data/league_snapshots/

Do not rank players unless projection or category data is available. The Python workflow will handle scoring after projections are joined.
```
