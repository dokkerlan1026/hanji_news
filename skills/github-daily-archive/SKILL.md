---
name: github-daily-archive
description: Maintain a GitHub repo as a dated daily archive for Markdown notes, reports, and collected materials. Use when asked to save work into the repo, organize files by day, rename files with time prefixes while keeping Chinese titles, update README.md as an index with tags and summaries, or push daily content to GitHub.
---

# GitHub Daily Archive

## Overview

Use this skill to store daily work in a GitHub repo with a predictable structure:

- one folder per day: `YYYY-MM-DD/`
- Markdown files inside that folder
- file names prefixed with time, while keeping the Chinese title
- `README.md` as the top-level index with links, tags, and short summaries

## Workflow

1. Determine the target date.
2. Create the date folder only if at least one new file will be added.
3. Save each new Markdown file under that folder.
4. Name files as `HHMM_中文標題.md`.
5. Update `README.md` only when that date gains new files.
6. Add a short summary and 1-3 tags per file.
7. Commit and push after changes are ready.

## Naming Rules

- Keep the folder name as `YYYY-MM-DD`.
- Keep Chinese titles in filenames.
- Prefix each filename with 24-hour local time, no colon.
- Use this pattern: `HHMM_標題.md`.
- Prefer concise titles that make sense in GitHub listings.

Examples:

- `2026-03-17/0700_台股早報.md`
- `2026-03-17/1530_任務整理.md`
- `2026-03-17/2145_讀書筆記.md`

## README Rules

Keep `README.md` simple and scannable.

For each active day, include:

- date heading
- folder link
- one bullet per file
- file link
- tags
- one-line summary

Use this structure:

```md
## 2026-03-17

資料夾：[`2026-03-17/`](./2026-03-17/)

- [`0700_台股早報.md`](./2026-03-17/0700_%E5%8F%B0%E8%82%A1%E6%97%A9%E5%A0%B1.md)
  - 標籤：`台股` `新聞整理`
  - 摘要：整理今日 07:00 - 12:00 的台股早盤新聞，聚焦 AI、台積電與記憶體族群。
```

## Tagging Rules

Pick 1-3 tags that help future retrieval.

Good tag examples:

- `台股`
- `筆記`
- `任務整理`
- `新聞整理`
- `AI`
- `市場觀察`
- `工作流`

Do not create too many near-duplicate tags.

## Update Policy

- If no new file is created for a day, skip updates.
- Do not create empty date folders.
- Do not rewrite old summaries unless the file itself changed.
- When reorganizing an older file, update both the path and the README link.

## Push Checklist

Before pushing:

1. Run `git status --short`.
2. Confirm only intended files are staged.
3. Commit with a concrete message.
4. Push to the configured branch.

Prefer commit messages like:

- `Add 2026-03-17 stock morning report`
- `Update README index for 2026-03-17`
- `Organize daily archive structure`

## References

Read `references/templates.md` when you need ready-to-copy filename, README, or summary templates.
