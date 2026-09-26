# Design Notes — Profiles Gallery (Fall 2026)

Instructor-facing. Explains **what** is in this repo and **why** each decision was made.
See also: [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md) (running the class) and [REBUILD.md](REBUILD.md) (how the repo was built, step by step).

---

## 1. Context

| | |
| --- | --- |
| Event | Live Git/GitHub workshop, UW Bothell, Fall 2026 |
| Length | 90 minutes |
| Audience | ~30 students, beginners with Git |
| Deliverable per student | One merged pull request adding their own profile card |
| Workflow | **Fork-based** — students have no write access to the instructor's repo |
| Environment | GitHub Codespaces in the browser (nothing installed locally) |
| GitHub repo | `uwb-css-bootup/profiles-2026` (local folder is named `profiles-fall-2026`) |
| AI assist | GitHub Copilot Chat, with a no-Copilot fallback |

### Guiding principle: reliability beats cleverness

With 30 people in a room, every failure mode becomes a queue of raised hands. So:

- **Zero dependencies, no build step, no CI on student PRs.** Nothing to install, nothing to break. The only automation is one post-merge workflow that rebuilds the gallery (§6).
- **Every student adds a unique new file** (`profiles/<their-username>.html`). No two PRs ever touch the same file, so merge conflicts are impossible by construction.
- **Cards in `profiles/`, everything else at the root.** Student cards go in `profiles/` so dozens of merged PRs don't bury the root. The templates, README, and `index.html` stay at the root, so students find the templates easily and the Pages URL doesn't change.
- **Students only ever add one file.** Shared files (templates, README, gallery) are never edited by students.

---

## 2. Repository layout

| Path | Audience | Purpose |
| --- | --- | --- |
| `README.md` | Students | Step-by-step workshop guide (10 numbered sections) |
| `template.html` | Students | The Developer Trading Card; copied to `profiles/YOUR-USERNAME.html` |
| `template.md` | Students | Plain-text fallback card; copied to `profiles/YOUR-USERNAME.md` |
| `.gitignore` | — | Ignores `.DS_Store`, `Thumbs.db`, `.vscode/` |
| `.devcontainer/devcontainer.json` | Codespaces | Codespaces' default image (`universal:linux`) + Live Preview extension + port 8000 preview |
| `.github/pull_request_template.md` | Students (auto) | Checklist pre-filled into every PR description |
| `.github/workflows/build-gallery.yml` | GitHub Actions | Runs `build_index.py` after each merge to `main` and commits `index.html` |
| `.agents/skills/profile-card/SKILL.md` | AI agents | Cross-tool skill: how an AI builds a student's card |
| `.agents/skills/profile-card/scripts/check_card.py` | AI agents, students | Validates a card before commit (stdlib only) |
| `.claude/skills/profile-card` | Claude Code | **Symlink** → `../../.agents/skills/profile-card` |
| `AGENTS.md` | AI agents (always loaded) | Short guardrails + pointer to the skill |
| `build_index.py` | Instructor | Regenerates `index.html` from all student cards in `profiles/` (stdlib only) |
| `profiles/` | Students | One card per student, added via PRs |
| `index.html` | Everyone (via Pages) | Generated gallery page; **never edited by hand** |
| `.nojekyll` | GitHub Pages | Disables Jekyll so files are served as-is |
| `docs/` | Instructor | These notes |

Student files (added via PRs) live in `profiles/`: `profiles/octocat.html`, `profiles/mona.md`, etc. The folder name is the `CARDS_DIR` constant in `build_index.py` and `check_card.py`; the workflow trigger and the docs spell it out.

---

## 3. The card: `template.html`

### Constraints
- Single file. `<!DOCTYPE html>`, `<html lang="en">`, `<meta charset="UTF-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- All CSS in one `<style>` block. **No JavaScript, no web fonts, no external URLs** (the file contains no `http` at all). Renders identically offline, in Live Preview, and on GitHub Pages.
- System font stack: `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.

### Theme — five CSS custom properties in `:root`
Changing this one block restyles the whole card (easy for students or Copilot):

| Variable | Value | Used for |
| --- | --- | --- |
| `--bg` | `#0f172a` | Page background |
| `--card` | `#1e293b` | Card background |
| `--text` | `#f1f5f9` | Main text |
| `--muted` | `#94a3b8` | Dividers, "Tech Stack" label, fun fact |
| `--accent` | `#38bdf8` | Card border, role/major, badges |

Contrast on the defaults: muted-on-card ≈ 5.7:1, accent-on-card ≈ 7:1 (both pass WCAG AA).

### Layout
- `body`: `display: grid; place-items: center; min-height: 100vh; padding: 1.5rem`.
- `.card`: `width: 100%; max-width: 380px; border: 2px solid var(--accent); border-radius: 16px; padding: 1.75rem`, soft shadow. Responsive with **no media queries**.
- Badges: `ul.tech-stack` is `display: flex; flex-wrap: wrap; gap: 0.5rem`, `list-style: none`; each `li.badge` is a pill (`border-radius: 999px`, accent border and text).
- `* { box-sizing: border-box; }`.

### Semantic structure and the five editable fields
```
<main>
  <article class="card">
    <header>
      <h1 id="student-name" class="student-name">Your Name</h1>
      <p id="role-or-major" class="role-or-major">Computer Science '27</p>
    </header>
    <section>
      <p id="bio" class="bio">…</p>
    </section>
    <section>
      <h2>Tech Stack</h2>
      <ul id="tech-stack" class="tech-stack"><li class="badge">Python</li> …</ul>
    </section>
    <footer>
      <p id="fun-fact" class="fun-fact">Fun fact: …</p>
    </footer>
  </article>
</main>
```
- Each of the five fields (plus `<title>`) has a `<!-- ✏️ EDIT HERE: … -->` comment directly above it.
- A banner comment at the very top says: *Copy this file to profiles/YOUR-USERNAME.html — do not edit template.html directly*, with the `cp` command and an `octocat` example.
- Placeholder content is obviously fake ("Your Name", "Computer Science '27") so an unedited card is easy to spot in review.
- The IDs exist so Copilot (and the verification script) can find fields reliably; the prompt tells Copilot to keep them.

### `template.md`
Same order and headings as the HTML card: `# Your Name`, a bold role/major line, bio paragraph, `## Tech Stack` with inline-code badges (`` `Python` `JavaScript` `Git` ``), `## Fun Fact`. Top HTML comment with copy instructions. For students whose Copilot isn't working or who prefer plain text.

---

## 4. Student README — design choices

The README is written in a beginner voice, numbered 1–10, each step with a one-line italic **"Why:"** so students build a mental model, not just a click sequence.

| # | Section | Key content |
| --- | --- | --- |
| 1 | What you'll do | Goal = a merged PR; `YOUR-USERNAME` convention with `octocat` example |
| 2 | Fork the repository | Fork → Create fork |
| 3 | Open a Codespace on your fork | Check the URL contains your username; Code → Codespaces → Create codespace on main |
| 4 | Create your branch | `git checkout -b profile-YOUR-USERNAME` + example |
| 5 | Make your card | `cp template.html profiles/YOUR-USERNAME.html` first, then Copilot prompt on the open file; Apply/Agent note; "Make my profile card" for AI agents (skill); hand-edit fallback; `.md` alternative |
| 6 | Preview your card | Command Palette → **Live Preview: Show Preview**; fallback `python3 -m http.server 8000` opens a **Card preview** panel automatically |
| 7 | Commit and push | `git status` first; `git add profiles/YOUR-USERNAME.html` (not `git add .`); commit; `git push origin profile-YOUR-USERNAME`; explains `origin` = your fork |
| 8 | Open the pull request | Compare & pull request banner (fallback: Contribute → Open pull request); base = instructor `main`, head = fork branch; title `Add YOUR-USERNAME profile`; gallery note |
| 9 | Rules | Add only your own file; don't edit templates, `index.html`, or others' files |
| 10 | Troubleshooting | 7-row table (below) |

### Why `YOUR-USERNAME` instead of `<username>`
The first draft used `<username>`. Students copy-paste commands, and in bash `<` is input redirection. Verified in bash:
```
$ git checkout -b profile-<username>
bash: syntax error near unexpected token `newline'
$ cp template.html <username>.html
bash: username: No such file or directory
```
Neither error hints at the fix. `YOUR-USERNAME` is shell-safe, and each command is followed by a concrete `octocat` example. A troubleshooting row still covers the bracket error in case old habits leak in.

### Why `cp` before Copilot
The first draft asked Copilot to "copy template.html into a new file". That only works in Copilot's Agent/Edit modes; in the default Ask mode Copilot just prints code. It was also the main way `template.html` got modified by accident. Now the file copy is a deterministic terminal step, and Copilot is asked to edit **only the file that is open**.

The Copilot prompt (verbatim in the README):
```text
Fill in my details in the file I have open. Only change this file.
- Name: (your name)
- Role or major: (e.g. Computer Science '27)
- Bio: (1–3 sentences about you)
- Tech stack: (languages and tools you use, one badge each)
- Fun fact: (something fun about you)
Keep the same HTML structure and element IDs. You may change the colors in the :root block to match my style.
```
Note: the original workshop spec contained its own prompt text that was not available when this was written. Replace the prompt above if you have the canonical one.

### Why `git status` + `git add profiles/YOUR-USERNAME.html` instead of `git add .`
`git add .` silently stages an accidental edit to `template.html`, after which the plain `git restore template.html` fix no longer works (the change is staged). Explicit staging enforces the "only your file" rule and teaches what the staging area is for. `git status` before committing is the single most valuable habit this workshop can teach.

### Why a devcontainer
The Live Preview extension (`ms-vscode.live-server`) is not guaranteed in a default Codespace, and "Show Preview" alone only exists for Markdown. `.devcontainer/devcontainer.json` adds the extension. This is configuration, not a dependency, so the zero-setup promise holds.

| Setting | Value | Why |
| --- | --- | --- |
| `image` | `mcr.microsoft.com/devcontainers/universal:linux` | This is the tag Codespaces uses as its default image (Sept 2026: same digest as `latest`, `6`, `6.1.7`). Tracking the default keeps it **cached** on Codespaces hosts (fast creation for 30 students at once) and **free of storage charges** (see below), even after a new major version ships. A major bump is low-risk here: the workshop needs only `python3` and `git`. Includes Python 3.14, git, node, `gh`, and the Copilot CLI. |
| `portsAttributes."8000"` | `label: "Card preview"`, `onAutoForward: "openPreview"` | When a student runs the `python3 -m http.server 8000` fallback, the port is labeled and a preview panel opens **inside the editor** automatically — no pop-up to miss, no URL to edit. |
| `customizations.vscode.extensions` | `["ms-vscode.live-server"]` | Live Preview for README §6. |

**History:** the first version pinned `universal:2`. By Sept 2026 that was four major versions old and a different digest from the default, so Codespaces would have pulled a separate, large, uncached image. It was briefly `universal:6`, then changed to `universal:linux` so it can't drift from the default again.

**Why not the smaller `mcr.microsoft.com/devcontainers/python` image?** Checked Sept 2026:

| | `universal:linux` | `python:3` |
| --- | --- | --- |
| Compressed size (amd64) | 4.01 GB, but already cached on Codespaces hosts | 0.65 GB, pulled for every codespace |
| Storage billed to students | None: "storage of base dev containers built from the default dev container image is free of charge" (identified by `Definition ID: universal`; the image's `dev.containers.id` label is `universal`) | "If you use an alternative base image, then the resulting container and all of the files in the codespace will be counted as used storage" |
| Tools | python3, git, node, `gh`, Copilot CLI | python3, git, node; no `gh` or Copilot CLI |
| Extensions it adds | GitHub Pull Requests | Python, Pylance, autopep8, ESLint (irrelevant to an HTML workshop) |

Python is only used for `http.server` and `check_card.py`, which `universal` covers. A Python-specific image would only make sense if the workshop wrote Python.

**Deliberately not added:**
- Copilot extensions — Codespaces provides Copilot to users who have access; `GitHub.copilot` has not been updated since Oct 2025, so pinning extension IDs risks installing a superseded one.
- `forwardPorts` — `portsAttributes` applies when the port is auto-detected, so nothing is forwarded until the student actually starts the server.
- `postCreateCommand`, features, `hostRequirements` — nothing to install; the default 2-core machine is plenty and conserves students' free Codespaces hours.

**Re-check before each term:** run [REBUILD.md §5.6](REBUILD.md#56-devcontainer-image-check) to see which version `universal:linux` currently is, and rehearse in a real Codespace.

### Troubleshooting table (README §10)
| Problem | Fix |
| --- | --- |
| `syntax error near unexpected token` / `No such file or directory: username` | Brackets typed; use the real username |
| `git status` shows `template.html` modified | `git restore template.html`; if already staged, `git restore --staged --worktree template.html` |
| push rejected / permission denied / 403 | Codespace is on the original repo; accept a fork offer if shown, else fork, new Codespace on the fork, copy file over |
| No Compare & pull request banner | Contribute → Open pull request |
| Committed on `main` by accident | `git checkout -b profile-YOUR-USERNAME` keeps the commit; push the branch |
| Live Preview command not found | `python3 -m http.server 8000` fallback |
| PR shows changes to other files | Ask an instructor |

---

## 5. Pull request template

`.github/pull_request_template.md` pre-fills every PR description with a four-item checklist:
- only one file added (`profiles/YOUR-USERNAME.html` or `.md`)
- filename matches GitHub username
- card previewed
- title is `Add YOUR-USERNAME profile`

It is a **nudge at the moment of submission**, not enforcement. PR templates are read from the base repo's default branch.

**Rejected:** a GitHub Action that fails PRs touching files other than one new card. It would work, but violates "no CI on student PRs", and the PR's *Files changed* tab already exposes the problem during review.

---

## 6. Gallery

### Goal
The payoff moment: everyone sees their card on one shared page, projected at the end of class.

### Design
- **GitHub Pages** serves the repo root from `main`.
- **`build_index.py`** (Python 3 standard library only; tested on 3.9) regenerates `index.html`. A workflow runs it after merging (see below); students never touch `index.html`, so it can't cause conflicts.
- Card discovery: every `*.html` / `*.md` file in `profiles/` (the `CARDS_DIR` constant). No skip list is needed because shared files never live there. A missing folder means zero cards. Sorted case-insensitively.
- **HTML cards** are embedded as `<iframe sandbox src="profiles/NAME.html" loading="lazy">` in a centered responsive grid (`repeat(auto-fit, minmax(min(100%, 380px), 440px))`, no max-width, so zooming the browser out adds columns for the end-of-class reveal). Each sits in a 480px-tall rounded "stage" with a caption link (initial avatar, username, "Open card"). Until there are 4 cards (`GHOST_TILE_BELOW`), a dashed "Your card goes here" tile is appended.
- **Markdown cards** are shown as a document tile linking to GitHub's rendered view (`https://github.com/OWNER/REPO/blob/main/profiles/NAME.md`). The repo URL is derived from `git remote get-url origin` (SSH or HTTPS form); if there is no remote, the link falls back to the relative `.md` path.
- Filenames are HTML-escaped and URL-quoted.
- Empty state: "No cards yet — be the first to open a pull request!" and a "0 cards" count.
- Gallery uses the same five-color palette as the card, plus a `--line` border tone, with one accent for every tile. It never reads student CSS. Text meant for the room is 16px or larger; fonts are system fonts only (no network); the only motion is a hover lift, disabled under `prefers-reduced-motion`.
- Output header comment: `<!-- Generated by build_index.py — do not edit by hand. -->`.

### Why a post-merge workflow
`.github/workflows/build-gallery.yml` runs on every push to `main` that touches `profiles/**` or `build_index.py`, plus a manual **Run workflow** button. It runs `build_index.py` and, only if `index.html` changed, commits it as `github-actions[bot]` ("Update gallery") and pushes; Pages then redeploys.
- It never runs on PRs, so it can't block or confuse students — the "no CI on student PRs" principle holds.
- It only ever writes `index.html` on `main`.
- No loop: pushes made with `GITHUB_TOKEN` don't trigger workflows, and the bot's commit only touches `index.html`, which isn't in the trigger paths anyway.
- `on.paths` can't use expressions or variables, so `profiles/**` is written out, with a comment to keep it in sync with `CARDS_DIR`.
- `concurrency` (no cancel) plus `git pull --rebase` before pushing handles back-to-back merges during class.
- Needs **Read and write** workflow permissions ([INSTRUCTOR_GUIDE.md §1.3](INSTRUCTOR_GUIDE.md#13-recommended-repo-settings)). Running `build_index.py` by hand still works as a fallback.

### Why `sandbox` on the iframes
Cards are served from the instructor's Pages origin. Without `sandbox`, a student's `<script>` could reach `window.top` and rewrite the gallery. `sandbox` with **no** `allow-*` flags blocks all scripts and gives the frame an opaque origin. Verified with a test card whose script rewrites both itself and `top`:
- inside the gallery → card and gallery unchanged;
- opened directly → the script ran ("GALLERY PWNED").

So the sandbox is what protects the gallery. The caption link opens the raw card, where scripts *can* run, affecting only that card's own page — review PRs for `<script>` before merging.

### Why `.nojekyll`
Without it, GitHub Pages' Jekyll build converts `NAME.md` to `NAME.html` (via optional-front-matter), which could collide with or shadow files. With `.nojekyll`, files are served exactly as committed.

### Rejected: client-side index using the GitHub API
An `index.html` that lists files via the GitHub REST API needs no regeneration step, but unauthenticated API calls are limited to **60 requests/hour per IP**. Thirty students on campus Wi-Fi likely share one NAT IP, so the gallery would fail exactly when it's being shown.

### Known trade-off
Iframes are a fixed 480px tall (cards are ~410px). A very long bio scrolls inside its frame instead of growing it — chosen to keep the grid tidy. Increase `height: 480px` on `.stage` in `build_index.py` if needed.

---

## 7. AI assistant skill (`profile-card`)

### Goal
Let a student say *"Make my profile card"* in **any** AI tool and get the same safe, correct result, while still typing the Git commands themselves.

### Format and discovery
The skill follows the open **Agent Skills** format: a folder whose `SKILL.md` has YAML frontmatter (`name` must equal the folder name, plus a `description` that tells the tool when to use it) and a Markdown body of instructions. Bundled files (here, `scripts/check_card.py`) sit alongside it.

| Tool | Where it looks (repo-level) | How this repo covers it |
| --- | --- | --- |
| GitHub Copilot (VS Code agent mode, Copilot CLI) | `.github/skills/`, `.claude/skills/`, `.agents/skills/` | `.agents/skills/profile-card/` |
| Gemini CLI | `.gemini/skills/` or the `.agents/skills/` alias | `.agents/skills/profile-card/` |
| OpenAI Codex and other Agent Skills tools | `.agents/skills/` | `.agents/skills/profile-card/` |
| Claude Code | `.claude/skills/` | Symlink `.claude/skills/profile-card` → `../../.agents/skills/profile-card` |
| Tools that don't support skills but read `AGENTS.md` | `AGENTS.md` | Root `AGENTS.md` points at the skill and restates the hard rules |
| Chat-only assistants (no repo access) | — | Student pastes the README §5 prompt; the skill's last section covers this case |

One canonical copy plus a symlink avoids two copies drifting apart. Codespaces (Linux) and macOS handle git symlinks natively.

**Why `AGENTS.md` but no `CLAUDE.md` / `GEMINI.md`:** those files are always loaded, including when the *instructor* uses an agent in this repo. `AGENTS.md` is scoped ("when a student asks…") and short; the full procedure only loads when the skill triggers.

### What the skill makes the agent do
1. **Rules:** edit only `profiles/USERNAME.html`/`.md`; never touch shared files; **never run `git add/commit/push/checkout/switch/branch`** (the student is here to learn Git); no JavaScript or external URLs; keep the five ids; never invent facts about the student.
2. **Username:** `$GITHUB_USER` (set by Codespaces) → owner of `git remote get-url origin` → ask; always confirm. If `origin` is the instructor's repo, stop and send the student to fork first.
3. **Branch:** if on `main`, ask the student to run `git checkout -b profile-USERNAME`.
4. **Details:** ask once for any missing name / role / bio / tech stack / fun fact / optional theme.
5. **Create:** `cp template.html profiles/USERNAME.html` (never retype the template).
6. **Fill:** text only, field table, HTML-escape `& < >`, one `<li class="badge">` per item, title `Name — Developer Trading Card`.
7. **Restyle (optional):** only the five `:root` values; ≥ 4.5:1 contrast against `--card`.
8. **Check:** run `check_card.py` until it prints `OK`.
9. **Hand off:** preview instructions + the exact `git status / add / commit / push` commands with the username filled in.
10. **Fallback** for chat-only tools: student pastes the file, the AI returns the complete file.

### `check_card.py`
Stdlib-only validator; exits 0 with `OK: NAME looks good`, or prints each problem with `✗` and exits 1. It flags:
- the file is a shared file (`template.*`, `index.html`, `README.md`, `AGENTS.md`)
- the card isn't in `profiles/` (compared with `profiles/` under the current directory, so run it from the repo root)
- any `http://`, `https://`, or `//host` URL
- leftover placeholder text (`Your Name`, `A sentence or two about who you are`, `something surprising about you`), case-insensitive, **ignoring HTML comments** (the `✏️ EDIT HERE: your name` comment caused a false positive before this)
- HTML only: `<script>`, any `on…=` attribute, unbalanced tags, and each of the five ids not appearing exactly once
- extensions other than `.html` / `.md`

### Tested
| Test | Result |
| --- | --- |
| Checker on `template.html` | Rejected as a shared file |
| Checker on unedited copy (`.html` and `.md`) | Three placeholder errors each |
| Checker on filled cards (`.html` and `.md`) | `OK` |
| Checker on card with `<script>`, `https://` image, `onerror`, missing `id="bio"` | All four reported |
| Checker on card in a subfolder | Rejected |
| `claude -p` in a copy of the repo: "is there a project skill named profile-card?" | Yes — discovered through the symlink |
| `claude -p` as a student, with `origin` = instructor repo | Refused and sent the student to fork first |
| `claude -p` as student `octocat` with details and "green theme", `origin` = fork | Created only `octocat.html`; no commits; `&` escaped; green `:root`; checker `OK`; printed the git commands for the student |

**Not tested:** Copilot, Gemini CLI, and Codex discovering the skill (their docs list `.agents/skills/`); whether Copilot in Codespaces uses skills outside Agent mode.

## 8. Verification that was performed

| Check | Method | Result |
| --- | --- | --- |
| Template well-formedness | stdlib `html.parser`: five IDs each exactly once, every tag closed, no `http` | Pass |
| Desktop render | Headless Chrome, 1280×900 | Card centered, badges wrap |
| Mobile render | Headless Chrome window of 390px is clamped to a minimum width (screenshot looked cropped); re-tested inside a 390px `<iframe>` | Card fits, text wraps |
| Student flow | In a scratch clone under bash: branch, `cp`, simulated Copilot edit to template, `git add` of both, `git restore --staged --worktree template.html`, commit | Commit contained only `octocat.html` |
| Gallery render | Sample cards (default, recolored, malicious script, markdown) served by `python3 -m http.server`, screenshots at 1400px and 500px | Grid renders; responsive |
| Sandbox | Malicious card in gallery vs. opened directly | Blocked in gallery; runs standalone |
| Generated HTML | Tag-balance check on empty and populated `index.html` | Pass |

### Not yet verified (needs a real Codespace + second GitHub account)
- devcontainer build and Live Preview command name in Codespaces
- Copilot Chat's **Apply** button / Agent mode wording
- Whether GitHub offers to fork on a 403 push from a Codespace on the upstream repo
- GitHub Pages deployment and the rendered-markdown links
- PR template appearing on a fork PR
- The `build-gallery.yml` workflow end to end (bot commit, Pages redeploy, no second run)

---

## 9. History

1. **Initial commit** `d73a3b2` — "Initial commit: Set up profiles gallery repository": `.gitignore`, `template.html`, `template.md`, `README.md`. Author identity was auto-derived by git (`GK <773293+gautamk@users.noreply.github.com>`) since no global `user.name` is set.
2. **Review pass** (TA / principal-engineer lens). Findings, in priority order:
   1. `<username>` placeholders break when pasted into bash → `YOUR-USERNAME` + examples.
   2. Live Preview likely missing in Codespaces → devcontainer + `http.server` fallback.
   3. Copilot prompt depends on chat mode → `cp` first, Copilot edits the open file only.
   4. `git add .` lets rule violations through → `git status` + explicit `git add`.
   5. Missing troubleshooting rows → banner fallback, 403 path, bracket errors, Live Preview missing.
   6. No submission-time guardrail → PR template.
   7. No actual gallery → Pages + generated `index.html`.
   - Also: "Why:" line per step, `<title>` edit marker.
3. **Applied** 1–5, then built 6 and 7, then wrote these docs (commit `1d51382`).
4. **Cross-tool AI skill** (§7): `.agents/skills/profile-card/` + Claude symlink + `AGENTS.md`; `AGENTS.md` added to `build_index.py`'s skip list so it never appears as a gallery card.
5. **Repo name fix:** the GitHub repo is `uwb-css-bootup/profiles-2026`, but README §2 said forks would be at `…/profiles-fall-2026`. The student-facing text now says `profiles-2026`; the skill no longer hardcodes a repo name.
6. **Devcontainer update:** `universal:2` → `universal:6` → `universal:linux` (tracks Codespaces' cached, storage-free default; `python` image evaluated and rejected); added port 8000 `Card preview` auto-preview; README §6 fallback text updated to match. Validated with `@devcontainers/cli read-configuration` and the spec schema.
7. **Auto-rebuilt gallery:** `.github/workflows/build-gallery.yml` runs `build_index.py` after each merge and commits `index.html`, replacing the manual rebuild step (§6). `build_index.py`'s docstring updated; its code is unchanged.
