---
name: browser-query-operator
description: Query websites, extract page information, navigate browser workflows, take screenshots, and perform lightweight browser interactions. Use when the user wants to browse a site, inspect page content, gather structured info, click through web pages, fill a form, or turn a web lookup task into a step-by-step browser workflow.
---

# Browser Query Operator

Use this skill for browser-based lookup and interaction tasks.

## Goal

Handle common browser tasks in a structured way:

1. open or fetch the target page
2. identify what the user really wants from the page
3. choose the lightest tool that can do the job
4. report the result clearly

## Tool selection

### Prefer lightweight tools first

Use lightweight fetch/search tools when the user mainly wants:

- page summaries
- article content
- documentation lookup
- link discovery
- quick fact extraction

### Use browser automation only when interaction is required

Escalate to browser automation patterns when the user needs:

- clicking through a flow
- filling forms
- logging in manually
- screenshots after interaction
- dynamic pages where static fetch is insufficient

## Browser workflow

1. Clarify the destination or target task.
2. Navigate to the page.
3. Inspect the visible structure.
4. Interact step by step.
5. Re-check after each major action.
6. Summarize findings or save artifacts such as screenshots.

## Safe operating rules

- Prefer read-only browsing unless the user explicitly wants interaction.
- Announce sensitive browser actions before doing them.
- Do not submit forms, purchases, or account changes without clear user intent.
- For authenticated browsing, prefer user-supervised login steps.
- When a page is complex, break the task into: open -> inspect -> act -> verify.

## Default output shape

When reporting a result, prefer:

```text
目標：<你要查什麼>

結果：
- ...
- ...

來源：
- <網址>
```

When reporting an interaction flow, prefer:

```text
目前頁面：<頁面或網站>
已完成：
- ...
- ...
下一步：
- ...
```

## Use patterns inspired by marketplace skills

This skill borrows safe ideas from browser automation skills:

- open / navigate first
- inspect state before clicking
- act in small steps
- verify after each step
- use screenshots when visual confirmation matters

## References

Read `references/workflows.md` for common browser task patterns.
Read `references/patterns.md` for prompt templates and reporting formats.
