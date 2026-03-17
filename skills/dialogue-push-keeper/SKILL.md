---
name: dialogue-push-keeper
description: Maintain a conversational assistant workflow that periodically checks whether the repo has new committed content and pushes it upstream on a 30-minute cadence. Use when the user wants the assistant to keep chatting naturally while also managing timed repo pushes, idle check-ins, short task breaks such as “I’ll go handle this for 10 minutes”, or concise push summaries after new content is uploaded.
---

# Dialogue Push Keeper

Use this skill to keep conversation behavior and repo push behavior aligned.

## Core rules

1. Keep conversation natural and concise.
2. If the user gives a short task break such as “go do this first” or “come back later”, acknowledge briefly and return when there is something meaningful to report.
3. Do not spam status updates during idle time.
4. Push only when there is new content worth pushing.
5. If the user explicitly asks to push now, push immediately and ignore the half-hour cadence.

## Push cadence

Default timed push windows:

- `09:00`
- `09:30`
- `10:00`
- and every 30 minutes after that

Interpretation:

- If there are new local commits not yet on `origin/main`, push at the next half-hour boundary.
- If there are no new commits, do nothing.
- If the session is idle and no content changed, do not send a message just to say nothing happened.
- After a successful timed push, send a short summary message.

## Short task-break behavior

When the user implies a short pause, use this pattern:

- “好，我先去處理，等有結果或有問題我再回來。”

Do not keep sending timer chatter every few minutes. Only come back when:

- the task is finished
- a blocker appears
- a timed push happened and there is something worth summarizing

## What counts as push-worthy

Push-worthy examples:

- new daily Markdown note
- updated README index
- new generated audio summary
- new skill or workflow improvement
- bug fix to scripts already in use

Not push-worthy by itself:

- no file change
- unstaged exploratory work with no meaningful result
- idle waiting

## Recommended workflow

1. Work normally in conversation.
2. Commit meaningful changes when ready.
3. Use `scripts/push_check.py` to decide whether a timed push is due.
4. If due and there are unpushed commits, push.
5. Report in one short sentence what was pushed.

## Scripts

- `scripts/push_check.py`
  - Determine whether a half-hour push is due
  - Detect whether local branch is ahead of upstream
  - Optionally update the recorded last-check state
- `scripts/push_now_if_needed.py`
  - Push immediately if local branch is ahead
  - Print a short summary for user-facing follow-up

## References

Read `references/behavior.md` for example wording and timing rules.
