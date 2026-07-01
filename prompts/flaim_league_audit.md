# Flaim Prompt — League Audit

Use this prompt during the league-audit phase or when reconnecting to a new season.

```text
Review my Yahoo fantasy basketball league.

Use platform="yahoo", sport="basketball", leagueId="466.l.3706", teamId="9", seasonYear=2025.

Summarize:
1. League format and scoring settings
2. My roster
3. Roster slots and positional requirements
4. Standings and final/current team rank
5. Category strengths and weaknesses, if available
6. Biggest roster risks
7. Injury/status concerns
8. Most important decision priorities
9. Initial free-agent or trade opportunities

Focus on 9-category fantasy basketball strategy.

Return the answer in a structure I can save as:
data/outputs/league_audit_summary.md
```
