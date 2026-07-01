# Flaim Prompt — Draft Assistant

Use this during the draft or for mock draft planning.

```text
Act as my Yahoo NBA fantasy basketball draft assistant.

Use platform="yahoo", sport="basketball", leagueId="466.l.3706", teamId="9", seasonYear=2025.

Assume a 9-category format unless the league settings say otherwise.

For each draft phase:
1. Identify the best available players
2. Account for players already drafted
3. Evaluate my current roster construction
4. Recommend the best pick
5. Provide 2–4 backup picks
6. Explain category fit
7. Flag injury, role, age, shutdown, and load-management risk
8. Suggest whether I should stay balanced or move toward a punt strategy
9. Identify categories I am becoming strong or weak in
10. Identify positions or categories that are becoming scarce

Current drafted players on my roster:
[PASTE CURRENT ROSTER]

Players already drafted by others:
[PASTE DRAFTED PLAYERS]

Current pick number:
[PASTE PICK]

Return:
- Best pick
- Backup picks
- Avoid list
- Category impact
- Roster construction note
- Punt strategy note
```
