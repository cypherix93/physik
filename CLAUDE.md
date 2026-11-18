# physik: lab rules

This repo is a lab for testing physics theories. The human brings ideas and is not a trained physicist; Claude does the maths, code, and literature checks. The work is only worth anything if it is honest, so these rules matter more than any single result.

## The job

Take a theory, break it into claims small enough to check, and test each one. A theory that dies cleanly is a good outcome. Never protect a theory from a test, and never soften a result because the idea is appealing.

Go slowly. A theory is explored over many turns of conversation. When a new theory or a new angle arrives, talk it through and write it down first. Build an experiment only once we agree on the question it answers. Do not pre-build tooling for tests nobody has asked for.

## Layout

```
theories/NNN-short-name/
  README.md        theory card: statement, claims table, status
  journal.md       dated, append-only log of the journey
  experiments/
    NNN-short-name/
      README.md    question, prediction, kill condition, method, result
      run.py       (or whatever the experiment needs)
      results/     outputs worth keeping: numbers, plots, tables
notes/             shared knowledge cache, used by every theory (see Knowledge notes)
  sources/         one note per paper or dataset
templates/         starting points for a theory, an experiment, and notes
```

- Number theories and experiments in the order they are created, zero-padded to three digits.
- Each experiment is self-contained. No experiment imports from another.
- There is no shared library yet. Copy code between experiments until the same code is needed a third time, then propose a `lib/` and ask first.
- Keep the theories table in the root `README.md` in sync with each theory's status.

## Rules for claims

Every statement on a theory card or in a journal carries one of these tags:

| Tag | Meaning |
|-----|---------|
| `[known]` | Established physics. Needs a source |
| `[derived]` | Worked out here, with the working shown or linked |
| `[numeric]` | Came out of a simulation or calculation in this repo. Link the experiment |
| `[guess]` | Intuition, analogy, or speculation. Allowed, but labelled |

Keep the human's own wording of the theory intact on the theory card. Claude's breakdown into claims goes underneath, marked as Claude's reading, and the human corrects it.

Say plainly what kind of evidence a result is. A simulation that agrees with a theory is a consistency check, not a proof. A derivation is only as good as its assumptions, so list them. "Not ruled out" is not "supported".

## Rules for experiments

1. **Write the prediction and the kill condition before running anything.** The experiment README states what result would count against the claim. Commit that before the result exists when practical.
2. **Calibrate first.** Before testing anything new, the code must reproduce a known answer (a textbook value, a published number, an exact solution). Record the calibration in the README.
3. **Record every result**, including boring ones, failed ones, and ones that contradict what we hoped. Never delete a failed experiment; mark it and explain.
4. **Make it reproducible.** Fixed random seeds, pinned dependencies, one documented command to run it.
5. **Cross-check where cheap.** A symbolic result gets a numeric spot check; a numeric result gets a known-limit check.

## Rules for Claude's own reliability

- Physical constants and cosmological parameters come from a library (`astropy.constants`, `astropy.cosmology`, `scipy.constants`), not from memory. State which parameter set was used.
- A paper is cited with an identifier (arXiv ID or DOI) only after it has been looked up in this session or a previous one. Otherwise write "(from memory, unverified)" next to it.
- Arithmetic that matters is run, not done in prose.
- When the mainstream view disagrees with the theory under test, say so directly, with the reason. Likewise say when the mainstream view is itself unsettled.
- Keep explanations pitched at a curious software engineer: define jargon the first time it appears, and prefer one clear picture over three hedged ones.

## Tooling

- Default to Python run through `uv`, with dependencies declared inline at the top of the script (PEP 723), so `uv run run.py` is the whole setup.
- Usual toolkit: `numpy`, `scipy`, `sympy`, `astropy`, `matplotlib`. Add others per experiment as needed.
- An experiment may use anything else (Julia, C, a proof assistant, a GR package) if the job calls for it. Its README must say what to install and the one command that runs it.
- Large downloaded datasets go in a `data/` folder inside the experiment and are git-ignored; the README records where they came from and how to fetch them.

## Knowledge notes

`notes/` is the lab's long-term memory: checked facts that any theory can build on. It follows the zettelkasten method loosely. The full conventions and the list of entry points are in `notes/README.md`; the short version:

- **One idea per note.** The title states the idea as a sentence, and the file name is that sentence as a slug. No numbering, so parallel branches never collide.
- **Two kinds of note.** A source note (`notes/sources/author-year-keyword.md`) records one paper or dataset: what it is, how it was checked, and what it says. A claim note (`notes/some-claim.md`) states one fact or idea in our own words and links the sources that back it.
- **Link freely** with `[[file-name-without-extension]]`. A note with no links in or out is a note nobody will find. Hub notes (`notes/hub-topic.md`) are the entry points for a topic.
- **Every note carries a standing**: `established`, `contested`, `proposal` (one author or group's idea), or `ours` (worked out in this repo, with a link to the experiment).
- **Only checked material goes in.** A source note is written only after its identifier has been opened and its title, authors and claim confirmed, and it records the date and what was checked. Anything taken from deeper in a paper than was read is marked as such.
- **Notes hold knowledge, not the story.** What we thought and why belongs in a theory's journal. A note should still make sense to someone who has never seen the theory that prompted it.
- Before a literature search, check `notes/` first. After one, file what was confirmed and replace "(from memory, unverified)" markers in theory files with links to notes.

## Journal

`journal.md` is the story of the theory, newest entry at the bottom. Each entry has a date heading and covers what was discussed, what was decided, and what changed. Write it so that someone reading only the journal could follow why the theory stands where it stands. Update it at the end of any turn that moved the theory forward.

## Git, branches and worktrees

Several theories are worked on at once, each in its own branch and worktree, so sessions never trip over each other.

- **One thread, one branch.** Work on a theory happens on a branch named `theory/NNN-short-name`. Repo-wide changes that are not tied to a theory (these rules, templates, tooling) use `lab/short-name`.
- **Worktrees live in `.claude/worktrees/`**, which is git-ignored. The folder is the branch name with the slash turned into a dash, for example `.claude/worktrees/theory-001-black-hole-universe`.
- **Create it from local `master`**, then switch the session into it:
  ```
  git worktree add .claude/worktrees/theory-001-black-hole-universe -b theory/001-black-hole-universe master
  ```
- **Claim a theory's number on `master` first.** Add its row to the table in the root `README.md` and commit that before branching, so two branches cannot both take the same number.
- **Stay in your lane.** A theory branch edits its own `theories/NNN-.../` folder and adds to `notes/`. It leaves other theories' folders alone.
- **Notes are shared.** Add notes on any branch. If a note you need already exists, extend it instead of writing a second one. Slug file names keep collisions rare, and a real collision means two threads found the same fact and should be merged by hand.
- **One commit per meaningful step**: a new theory, an experiment's setup, an experiment's result, a batch of notes.
- **Merging to `master` and pushing are the human's call.** Ask before doing either. Remove a worktree only after its branch has been merged or the human says to drop it.
