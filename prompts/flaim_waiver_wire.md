# Flaim Prompt — Waiver Wire

Use this for human review alongside the Python waiver report.

```text
Analyze available players in my Yahoo fantasy basketball league.

Use platform="yahoo", sport="basketball", leagueId="466.l.3706", teamId="9", seasonYear=2025.

Identify:
1. Best long-term adds
2. Best short-term streamers
3. Best category specialists
4. Best injury replacements
5. Best upside stashes
6. Players who are only useful in specific punt builds
7. Players who are risky because of injury, uncertain role, low minutes, or poor schedule
8. Rostered players I should compare them against before making a move

For each recommendation, explain:
- Category fit
- Expected role/minutes logic
- Injury/status risk
- Short-term vs long-term value
- Whether the player is a streamer, hold, or speculative add

Do not make final add/drop recommendations unless you compare the free agent against my rostered drop candidates.
```
