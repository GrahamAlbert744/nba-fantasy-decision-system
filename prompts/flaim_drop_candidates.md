# Flaim Prompt — Drop Candidates

Use this for roster triage and add/drop decisions.

```text
Review my current Yahoo fantasy basketball roster and identify drop candidates.

Use platform="yahoo", sport="basketball", leagueId="466.l.3706", teamId="9", seasonYear=2025.

Classify each rostered player as one of:
1. Must hold
2. Hold
3. Hold but monitor
4. Replaceable
5. Drop if better option exists
6. Drop now

For each weak or replaceable player, explain:
- Why they are risky or replaceable
- Whether the issue is role, minutes, injury, schedule, category weakness, or low upside
- Which categories they help
- Which categories they hurt
- Whether they should be compared against free agents before dropping

Then identify specific free agents who could replace the weakest rostered players.

Do not recommend dropping IL players unless dropping them actually opens a useful roster spot.
```
