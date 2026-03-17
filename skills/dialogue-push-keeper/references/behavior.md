# Behavior patterns

## Timed push wording

If a timed push happened:

- `我剛幫你把新的內容推上去了，這次主要是更新了 README 和今天的資料。`
- `剛剛照半小時節點幫你推了一次，有新內容才推，沒有白吵你。`

## Idle wording

If nothing changed:

- say nothing
- do not announce an empty push check

## Short break wording

Good:
- `好，我先去處理，等有結果我再回來。`
- `我先去弄，卡住我再叫你。`

Important timing rule:
- the 10-minute idle timer starts only after the assistant has already replied
- any new user message cancels the idle transition and gets a normal timely reply first
- only after post-reply silence longer than 10 minutes should background-mode behavior begin

Avoid:
- repetitive countdowns
- needless “still working” chatter
- pushing with no changes

## Timing rule

A timed push is due only when:

- the current minute is `00` or `30`
- and this boundary has not already been processed
- and local branch is ahead of upstream

## Practical note

If you want this behavior to run automatically outside active conversation, pair this skill with a scheduler such as an OpenClaw cron job or heartbeat-driven check. The skill itself defines the rules and scripts; scheduling is the deployment layer.

For B-mode, prefer the script-first approach:
- record the assistant reply timestamp that starts the idle timer
- schedule a one-shot job
- let the script inspect the transcript directly
- if no newer user message exists, send one fixed Chinese update via `openclaw message send`
