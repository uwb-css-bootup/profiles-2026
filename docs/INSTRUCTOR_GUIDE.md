# Instructor Guide — Profiles Gallery (Fall 2026)

How to set up, rehearse, run, and wrap up the workshop.
See also: [DESIGN.md](DESIGN.md) (why things are the way they are) and [REBUILD.md](REBUILD.md) (recreate the repo from scratch).

---

## 1. One-time setup (1–2 weeks before class)

### 1.1 Publish the repo
The GitHub repo is **`uwb-css-bootup/profiles-2026`** and is already set as `origin` in this folder. (The local folder is named `profiles-fall-2026`; that's fine.) Create it on github.com as an empty **public** repo if it doesn't exist yet, then:

```bash
git config user.name "Your Name"          # optional: set a real author name for this repo
git push -u origin main
```

The repo must be **public** so students can fork it and so Pages is free. If you ever rename it, update README §2 (`github.com/YOUR-USERNAME/profiles-2026`).

### 1.2 Turn on the gallery
1. Repo → **Settings → Pages** → Source: **Deploy from a branch** → Branch `main`, folder `/ (root)` → Save.
2. If the repo lives in a university organization, confirm the org allows Pages.
3. After ~1 minute, open `https://uwb-css-bootup.github.io/profiles-2026/` — you should see "No cards yet — be the first to open a pull request!"

### 1.3 Recommended repo settings
- **Settings → General → Pull Requests**: allow **Squash merging** (one clean commit per student). Disabling the others is optional.
- **Settings → Actions → General → Workflow permissions**: choose **Read and write permissions** → Save. The "Rebuild gallery" workflow needs this to commit `index.html`; without it its push fails with a 403.
- No branch protection needed — students can't push to your repo anyway. If you add protection that requires PRs on `main`, allow `github-actions[bot]` to bypass it, or the gallery workflow can't push.

### 1.4 Send the pre-class email
Codespace creation and Copilot sign-in are the two biggest time sinks if done live. Suggested text:

> **Before our Git/GitHub workshop, please:**
> 1. Create a GitHub account (or sign in) at github.com and **verify your email address**.
> 2. Get GitHub Copilot: students can get it free via **GitHub Education** (education.github.com); otherwise enable **Copilot Free** in your GitHub settings.
> 3. Test Codespaces: open any repo you own, click **Code → Codespaces → Create codespace**, wait for it to load, then delete it.
> 4. Bring a laptop with Chrome, Edge, or Firefox. Nothing else to install.
> 5. Know your GitHub username — you'll type it a lot.

---

## 2. Rehearsal (do this once, from a second GitHub account)

Walk the student README top to bottom as a student would. Tick each item:

- [ ] Fork works; fork URL is `github.com/SECOND-ACCOUNT/profiles-2026`
- [ ] Codespace on the fork builds quickly with the devcontainer (`universal:linux` image, Live Preview extension installed)
- [ ] Command Palette → **Live Preview: Show Preview** exists and shows the card
- [ ] `python3 -m http.server 8000` fallback: a **Card preview** panel opens in the editor; clicking `YOUR-USERNAME.html` shows the card
- [ ] Copilot Chat with the README prompt edits **only** the open file (note what the Apply button / mode picker are actually called and fix the README if needed)
- [ ] Copilot **Agent mode**: "Make my profile card" triggers the `profile-card` skill (from `.agents/skills/`); it creates only the student's file, runs `check_card.py`, and does **not** commit or push
- [ ] If available, repeat with Gemini CLI or Claude Code in the Codespace terminal
- [ ] `git status` → `git add` → `git commit` → `git push origin profile-…` all succeed
- [ ] Compare & pull request banner appears; base/head are correct
- [ ] PR description is pre-filled with the checklist from `.github/pull_request_template.md`
- [ ] Open a Codespace on **your** (upstream) repo from the second account and try to push: record what actually happens (fork offer? 403?) and update README §10 row 3 to match
- [ ] Merge the PR; within about a minute an "Update gallery" commit from `github-actions[bot]` appears on `main` (Actions tab → "Rebuild gallery"), and the card appears on Pages. Confirm the bot's commit did not start a second run
- [ ] Add a `.md` card too and confirm its gallery tile links to GitHub's rendered view
- [ ] Delete the rehearsal cards before class (the workflow removes them from the gallery)

---

## 3. Suggested 90-minute run of show

| Time | Segment | Notes |
| --- | --- | --- |
| 0:00–0:10 | Why Git/GitHub; the plan (fork → branch → commit → PR) | Draw the fork/PR diagram once; refer back to it |
| 0:10–0:25 | README §2–§4: fork, Codespace, branch | Everyone does it together. Codespaces take a few minutes to boot — talk over it |
| 0:25–0:45 | README §5–§6: make and preview the card | Circulate. Most common issue: editing `template.html` instead of their copy |
| 0:45–0:55 | README §7: `git status`, add, commit, push | Project your own terminal. Stress `git status` |
| 0:55–1:05 | README §8: open PRs | Watch PRs arrive on the projector |
| 1:05–1:20 | Live code review + merge + gallery updates | Review 2–3 PRs on screen (Files changed tab, leave a comment, approve). The gallery rebuilds itself after each merge |
| 1:20–1:30 | Gallery reveal; wrap-up; delete Codespaces | Project the Pages URL |

Leave slack: the timeline above assumes the pre-class email was followed.

---

## 4. Reviewing, merging, and updating the gallery

### What to check on each PR (Files changed tab)
- Exactly **one** added file, named after the student's GitHub username (`.html` or `.md`).
- No changes to `template.*`, `README.md`, `index.html`, or anyone else's file.
- No `<script>` tags or external URLs (the gallery sandboxes scripts, but the standalone card page would run them).
- Content is appropriate for a class page.

### Merging
Use **Squash and merge**. Because every PR adds a unique file, PRs never conflict and can be merged in any order — even if the student's fork is out of date.

### Updating the gallery (automatic)
Every merge to `main` triggers the **Rebuild gallery** workflow (`.github/workflows/build-gallery.yml`). It runs `build_index.py` and, if the card list changed, commits `index.html` as `github-actions[bot]` with the message "Update gallery". Pages then redeploys; after about a minute, refresh the projected page. Back-to-back merges queue up and each run finishes.

Because of those bot commits, run `git pull` before you edit anything in your local clone.

**If a run fails** (Actions tab → Rebuild gallery → red ✗): usually the workflow permission from §1.3 is missing. Fix it, then click **Run workflow** to rerun. Manual fallback, in your local clone:

```bash
git pull
python3 build_index.py          # prints e.g. "Wrote index.html with 12 cards."
git add index.html
git commit -m "Update gallery"
git push
```

`build_index.py` needs Python 3 only (standard library), and must be run from a clone that has an `origin` remote pointing at GitHub so markdown-card links resolve.

---

## 5. Fixing common student problems

| Symptom | What to tell the student |
| --- | --- |
| PR includes a change to `template.html` | In their Codespace: `git restore --source=origin/main template.html`, then `git add template.html`, `git commit -m "Undo template change"`, `git push`. The PR updates automatically. |
| File named wrong (e.g. `template copy.html`, wrong case) | `git mv "template copy.html" octocat.html`, commit, push. |
| Student opened the PR from `main` instead of a branch | Fine for this workshop — review and merge normally. |
| Student worked in a Codespace on the upstream repo and can't push | Fork, open a Codespace on the fork, recreate the file (copy/paste contents), continue from README §7. |
| Two PRs from the same student | Close the older one. |
| PR is an unedited template | Leave a friendly review comment ("Request changes"), which is itself a good teaching moment. |
| Card fails review for script/URL/missing field | Have them run `python3 .agents/skills/profile-card/scripts/check_card.py USERNAME.html` — it lists every problem. |
| Card looks broken in the gallery | Open the card directly (caption link). Usually a missing closing tag from hand-editing; comment on the PR. |

Every fix is a new commit pushed to the same branch — reinforce that PRs update automatically.

---

## 6. After class

- Remind students to **delete their Codespace** (github.com/codespaces) — idle Codespaces consume their free monthly hours and storage.
- Merge any stragglers; check the last "Rebuild gallery" run succeeded.
- Optionally archive the repo (Settings → Archive) to freeze it.
- For a future term: copy the repo (see [REBUILD.md](REBUILD.md)), rename it (e.g. `profiles-winter-2027`) and update the name in `README.md` §2 and the headings in `README.md` and `build_index.py`.
