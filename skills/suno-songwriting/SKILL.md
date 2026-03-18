---
name: suno-songwriting
description: Write lyrics, song structure, style prompts, and arrangement notes for songs intended for Suno. Use when the user wants to create a song, generate lyrics, shape verse-chorus-bridge structure, prepare Suno-friendly prompts, or turn a theme / mood / story into a ready-to-paste Suno song spec.
---

# Suno Songwriting

Use this skill when the user wants a song made for Suno.

## Goal

Produce outputs that are easy to paste into Suno and easy to revise.

Default deliverables:

1. `Title`
2. `Style Prompt`
3. `Lyrics`
4. `Optional Arrangement Notes`

## Core workflow

1. Identify the song target:
   - theme
   - mood
   - genre
   - language
   - singer perspective
   - tempo / energy if known
2. Choose a simple structure.
3. Write a Suno-friendly style prompt.
4. Write lyrics with clear section headers.
5. Keep lines singable and not too dense.
6. If the user did not provide enough detail, make strong but coherent choices.

## Preferred lyric structure

Default structure:

```text
[Intro]
[Verse 1]
[Pre-Chorus]
[Chorus]
[Verse 2]
[Pre-Chorus]
[Chorus]
[Bridge]
[Final Chorus]
[Outro]
```

Use fewer sections for short / simple songs.
Use no more structure than the idea needs.

## Suno-friendly formatting rules

- Use bracketed section headers like `[Verse 1]`, `[Chorus]`, `[Bridge]`.
- Keep chorus memorable and repeatable.
- Prefer short lines over paragraph-like blocks.
- Avoid overly literary lines that are hard to sing.
- Avoid too many internal commas unless the phrasing really needs them.
- Make the first chorus land fast unless the user wants a slow-burn song.
- Keep the central hook obvious.

## Style prompt rules

A good Suno style prompt should usually include:

- genre or blend of genres
- mood
- vocal character
- production feel
- optional tempo / era / instruments

Good example:

```text
Mandopop, emotional male vocal, warm piano intro, modern pop drums, cinematic build, catchy chorus, bittersweet but uplifting, polished studio production
```

Avoid vague prompts like:

```text
good song, nice melody, awesome vibe
```

## Arrangement note rules

Optional arrangement notes can mention:

- intro feel
- drop / lift points
- whether bridge strips back or explodes
- ending style

Keep them short and practical.

## Output templates

When the user asks for a song, default to this format:

```text
Title: <title>

Style Prompt:
<style prompt>

Lyrics:
[Verse 1]
...

[Chorus]
...

Optional Arrangement Notes:
- ...
```

## Reference files

Read `references/templates.md` for reusable song blueprints.
Read `references/prompt-patterns.md` for style prompt formulas and examples.
