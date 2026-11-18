# Notes

The lab's long-term memory. Each note holds one checked fact or idea, written so that any theory can reuse it without redoing the reading. Loosely a zettelkasten: small notes, one idea each, joined by links instead of folders.

## Finding things

Start from a hub. A hub is a note that lists and orders the other notes on a topic.

| Hub | Covers |
|-----|--------|
| | |

Or search: every note's file name is its idea as a sentence, so `ls notes` and a text search go a long way.

## The two kinds of note

**Source notes** live in `notes/sources/`, one per paper, book or dataset, named `author-year-keyword.md`. A source note says what the work is, how we confirmed it exists and says what we think it says, and what it claims. It makes no judgement beyond the paper's own standing in the field.

**Claim notes** live directly in `notes/`. Each states one fact or idea in our own words, named as a sentence: `ordinary-matter-can-only-slow-an-expansion.md`. A claim note links the source notes that back it and the neighbouring claims it depends on or contradicts.

**Hub notes** are claim-level notes named `hub-topic.md` that exist to organise others.

## Rules

1. **One idea per note.** If a note needs "and also", split it.
2. **Name it as a sentence.** The title should be something that can be true or false. "Holographic dark energy" is a topic; "Using the Hubble radius as the holographic length gives no acceleration" is a note.
3. **Link with `[[file-name-without-extension]]`.** Link whenever a note leans on another. Add new notes to a hub.
4. **State the standing** in the header:
   - `established`: textbook or broadly accepted, with a source.
   - `contested`: published and disputed; the note names both sides.
   - `proposal`: one author or group's idea, not broadly adopted.
   - `ours`: worked out in this repo. Link the experiment. Our own results never get `established`.
5. **Only checked material.** Record the date and what was opened. "Checked: abstract" means the identifier resolves and the abstract supports the claim. "Checked: paper" means the relevant section was read. Details taken from memory or from a secondary summary are labelled where they appear.
6. **Write for a stranger.** No "as we found yesterday". Plain words, jargon defined once. A note should make sense without the theory that prompted it.
7. **Correct in place, visibly.** If a note turns out wrong, fix it and add a dated line under "Changes" saying what changed and why. Notes are current knowledge, not history; the theory journals are the history.
8. **No numbering.** Slugs only, so parallel branches cannot collide on an ID.

## Header format

Every note starts with:

```
---
type: source | claim | hub
standing: established | contested | proposal | ours
checked: YYYY-MM-DD, what was opened
tags: [a, few, lowercase, tags]
---
```

Templates for both kinds are in `templates/notes/`.
