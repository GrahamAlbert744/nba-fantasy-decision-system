# Flaim Prompt — Projection Gap Review

Use this to identify which Flaim players are missing projections in the Python workflow.

```text
Review the current free-agent and roster snapshots from my Yahoo fantasy basketball league.

Use platform="yahoo", sport="basketball", leagueId="466.l.3706", teamId="9", seasonYear=2025.

I am joining Flaim player snapshots to local projection files. Help identify which players are likely to need projection rows.

Return:
1. Rostered players that need projection data
2. Free agents that need projection data
3. Players with name formatting risks, such as punctuation, apostrophes, suffixes, or initials
4. Players where Yahoo/Flaim player IDs should be preferred over name matching
5. Any rookies or low-ownership players likely missing from public projection files

Do not rank players. This is a data-quality and join-readiness review.
```
