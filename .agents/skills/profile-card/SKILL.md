---
name: profile-card
description: Create, fill in, or restyle a student's Developer Trading Card (YOUR-USERNAME.html or YOUR-USERNAME.md) in the profiles gallery Git/GitHub workshop repo. Use when a student asks to make, fill in, update, fix, or change the colors of their profile card.
---

# Profile Card

You are helping a student in a live Git/GitHub workshop add their own profile card to this repository. The student is learning Git, so **you make the card and they run the Git commands themselves.**

## Rules (never break these)

1. Only create or edit **one** file: the student's own card at the repo root, `USERNAME.html` (or `USERNAME.md`), where `USERNAME` is their GitHub username.
2. Never modify `template.html`, `template.md`, `index.html`, `README.md`, `AGENTS.md`, `build_index.py`, anything in `.github/`, `.agents/`, `.claude/`, `docs/`, or another student's card.
3. Never run `git add`, `git commit`, `git push`, `git checkout`, `git switch`, or `git branch`. Tell the student the exact command instead.
4. No JavaScript: no `<script>` tags and no `on…=` attributes.
5. No external resources: no `http://`, `https://`, or `//` URLs — no web fonts, remote images, or links.
6. Keep the HTML structure from `template.html`. The ids `student-name`, `role-or-major`, `bio`, `tech-stack`, and `fun-fact` must each appear exactly once.
7. Never invent facts about the student. If a detail is missing, ask for it. You may polish wording they give you.

## Steps

### 1. Find the student's GitHub username
Try in order, then **confirm it with the student** before creating any file:
- `echo "$GITHUB_USER"` (set automatically in GitHub Codespaces)
- the owner in `git remote get-url origin` (their fork looks like `github.com/USERNAME/REPO-NAME`)
- ask the student

If `origin` does not belong to the student (it's the instructor's repo), stop and tell them to fork first (README step 2) and open a Codespace on their fork.

### 2. Check their branch
Run `git branch --show-current`. If it prints `main`, ask the student to run this themselves, then continue:

```bash
git checkout -b profile-USERNAME
```

### 3. Collect their details
Ask in **one** message for anything they haven't given you:
- **Name**
- **Role or major** (e.g. `Computer Science '27`)
- **Bio** — 1–3 sentences
- **Tech stack** — languages and tools, 3–8 items
- **Fun fact**
- *(optional)* a color theme

### 4. Create the file
If `USERNAME.html` doesn't exist yet, copy the template exactly — don't retype it:

```bash
cp template.html USERNAME.html
```

If the file already exists, edit it in place. For a plain-text card, use `template.md` → `USERNAME.md` instead.

### 5. Fill in the fields (HTML)
Replace **only the text content**, keeping every tag, id, and class:

| Field | Element | What to put there |
| --- | --- | --- |
| Tab title | `<title>` | `Name — Developer Trading Card` |
| Name | `<h1 id="student-name">` | Their name |
| Role or major | `<p id="role-or-major">` | e.g. `Computer Science '27` |
| Bio | `<p id="bio">` | 1–3 sentences |
| Tech stack | `<ul id="tech-stack">` | One `<li class="badge">Item</li>` per item; replace the three example badges |
| Fun fact | `<p id="fun-fact">` | Keep the `Fun fact: ` prefix |

- Escape special characters in text: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;` (e.g. `C++ &amp; Java`).
- You may leave or remove the `✏️ EDIT HERE` comments.

For a `.md` card: replace the `# Your Name` heading, the bold role line, the bio paragraph, the inline-code badges under `## Tech Stack`, and the text under `## Fun Fact`.

### 6. Optional: restyle
Change **only** the five values in the `:root` block (`--bg`, `--card`, `--text`, `--muted`, `--accent`). Keep text readable: `--text`, `--muted`, and `--accent` should each have at least 4.5:1 contrast against `--card`.

### 7. Check the card
Run:

```bash
python3 .agents/skills/profile-card/scripts/check_card.py USERNAME.html
```

Fix every problem it reports and run it again until it prints `OK`.

### 8. Hand off to the student
Tell the student, with their real username filled in:

1. Preview: Command Palette → **Live Preview: Show Preview** (or `python3 -m http.server 8000` and open `/USERNAME.html`).
2. Then run these themselves:
   ```bash
   git status
   git add USERNAME.html
   git commit -m "Add USERNAME profile"
   git push origin profile-USERNAME
   ```
3. Open the pull request (README step 8).

Do not run these commands for them.

## If you can't edit files or run commands
(For example, a chat-only assistant.) Ask the student to run `cp template.html USERNAME.html` and paste the file contents to you. Reply with the **complete** updated file for them to paste back, following every rule above, and tell them to run the check in step 7.
