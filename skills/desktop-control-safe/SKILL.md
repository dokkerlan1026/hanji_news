---
name: desktop-control-safe
description: Plan and execute safe desktop control workflows for mouse, keyboard, screenshots, windows, and on-screen inspection. Use when the user wants desktop-level interaction, app/window control, screenshots, coordinate-based actions, or a careful step-by-step computer-use workflow with explicit safety boundaries.
---

# Desktop Control Safe

Use this skill for desktop-level control tasks.

## Goal

Provide a safe workflow for desktop automation and computer-use tasks.

Typical tasks:

- move mouse to a target area
- click specific screen locations
- type into desktop apps
- switch or inspect windows
- take screenshots for verification
- guide step-by-step desktop interaction

## Safety first

Desktop actions are higher risk than read-only browsing.

Rules:

1. Prefer inspection before action.
2. Prefer screenshots or state checks before clicking.
3. Treat destructive actions as sensitive.
4. Do not submit, delete, purchase, or confirm account actions without explicit user intent.
5. Break actions into small visible steps.
6. Report what will happen before major UI actions.

## Recommended workflow

1. Identify the exact target app or window.
2. Establish current desktop state.
3. If needed, capture screenshot or confirm coordinates.
4. Perform one action at a time.
5. Verify after each step.
6. Stop when the task becomes irreversible without user confirmation.

## Common action types

### Mouse

Use for:
- moving to coordinates
- clicking
- dragging
- scrolling

### Keyboard

Use for:
- typing text
- shortcuts
- navigation keys

### Windows

Use for:
- listing windows
- activating the right window
- checking size / position

### Screen inspection

Use for:
- screenshots
- checking visible state
- locating visual targets before action

## Default response pattern

Before action:

```text
我準備這樣做：
- 先確認視窗
- 再移動到目標位置
- 做一次點擊
- 點完再檢查畫面變化
```

After action:

```text
我剛完成：
- ...
- ...

目前狀態：
- ...
```

## Design ideas learned from marketplace skills

This skill borrows safe patterns from desktop-control style skills:

- explicit mouse and keyboard action separation
- screenshot-before-click for uncertain UI state
- window-awareness before input
- emergency-stop mindset and stepwise execution

## References

Read `references/workflows.md` for common desktop workflows.
Read `references/safety.md` for guardrails and confirmation triggers.
