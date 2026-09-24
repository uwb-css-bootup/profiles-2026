# Profiles Gallery — Fall 2026

Welcome! In this workshop you'll add your own **developer trading card** to this repository using Git and GitHub.

## 1. What you'll do

You'll make your own copy of this repo (a *fork*), create a new branch, add one file with your profile card, and send it back here as a **pull request (PR)**. You're done when your PR is merged and your card is part of the gallery. 🎉

> **Replace `YOUR-USERNAME` with your GitHub username** everywhere in this guide.
> Example: if your username is `octocat`, then `profile-YOUR-USERNAME` becomes `profile-octocat`.

## 2. Fork the repository

*Why: you can't change the instructor's repo directly, so you work in your own copy.*

1. At the top right of this repo's page on GitHub, click **Fork**.
2. Keep the default settings and click **Create fork**.

You now have your own copy at `github.com/YOUR-USERNAME/profiles-2026`. You'll do all your work there.

## 3. Open a Codespace on your fork

*Why: a Codespace is a ready-to-use editor and terminal in your browser — nothing to install.*

1. Make sure you're on **your fork** — the URL should include your username.
2. Click the green **Code** button → **Codespaces** tab → **Create codespace on main**.
3. Wait for the editor to load in your browser. The terminal is at the bottom.

## 4. Create your branch

*Why: a branch keeps your work separate from `main` until it's reviewed.*

In the Codespace terminal, run:

```bash
git checkout -b profile-YOUR-USERNAME
```

Example: `git checkout -b profile-octocat`

## 5. Make your card

First, copy the template to a new file named after you:

```bash
cp template.html YOUR-USERNAME.html
```

Example: `cp template.html octocat.html`

Then open **your** file (`YOUR-USERNAME.html`, not `template.html`) from the file explorer.

**With Copilot Chat:** open Copilot Chat (the chat icon in the sidebar) and paste this prompt, filling in your details:

```text
Fill in my details in the file I have open. Only change this file.
- Name: (your name)
- Role or major: (e.g. Computer Science '27)
- Bio: (1–3 sentences about you)
- Tech stack: (languages and tools you use, one badge each)
- Fun fact: (something fun about you)
Keep the same HTML structure and element IDs. You may change the colors in the :root block to match my style.
```

If Copilot replies with code instead of changing your file, click **Apply** on its code block (or switch the chat mode to **Agent** and ask again).

**Using an AI agent** (Copilot Agent mode, Claude Code, Gemini CLI, Codex…)? This repo includes a **profile-card skill** that tells it exactly how to build your card. Just say *"Make my profile card"* and answer its questions. It will make the card and then tell you the Git commands to run yourself.

**No Copilot?** No problem — edit the text under each `✏️ EDIT HERE` comment by hand.

Prefer plain text? Use `cp template.md YOUR-USERNAME.md` instead and edit that file.

## 6. Preview your card

1. Open `YOUR-USERNAME.html`.
2. Open the Command Palette (`Ctrl+Shift+P`, or `Cmd+Shift+P` on Mac) and run **Live Preview: Show Preview**.

Your card appears in a panel next to the code and updates as you save.

*Fallback:* in the terminal, run `python3 -m http.server 8000`. A **Card preview** panel opens inside the editor with a list of files — click `YOUR-USERNAME.html`. (No panel? Open the **Ports** tab at the bottom and click the globe icon next to port 8000.) Press `Ctrl+C` in the terminal to stop the server.

## 7. Commit and push

*Why: a commit saves a snapshot of your work; pushing uploads it to your fork on GitHub.*

In the terminal, first check what changed:

```bash
git status
```

You should see **only** `YOUR-USERNAME.html` (or `.md`) listed. If anything else shows up, see [Troubleshooting](#10-troubleshooting).

Then add **just your file**, commit, and push:

```bash
git add YOUR-USERNAME.html
git commit -m "Add YOUR-USERNAME profile"
git push origin profile-YOUR-USERNAME
```

Example:

```bash
git add octocat.html
git commit -m "Add octocat profile"
git push origin profile-octocat
```

Here `origin` is **your fork** — not the original repo. That's exactly where you want to push.

## 8. Open the pull request

*Why: a pull request asks the instructor to review your change and merge it into the real repo.*

1. Go to your fork on GitHub. You'll see a yellow banner: **Compare & pull request**. Click it.
   (No banner? Click **Contribute** → **Open pull request** instead.)
2. Check the top of the page:
   - **base repository**: the instructor's repo, branch `main`
   - **head repository**: your fork, branch `profile-YOUR-USERNAME`
3. Title: `Add YOUR-USERNAME profile`
4. Click **Create pull request**. Done!

Once your PR is merged, your card will appear on the class gallery page — your instructor will share the link.

## 9. Rules

- ✅ Only **add your own file** (`YOUR-USERNAME.html` or `YOUR-USERNAME.md`).
- ❌ Don't edit `template.html`, `template.md`, or `index.html` (the gallery page — your instructor updates it).
- ❌ Don't edit anyone else's file.

Following these rules means no two PRs ever touch the same file — so no merge conflicts.

## 10. Troubleshooting

| Problem | Fix |
| --- | --- |
| `syntax error near unexpected token` or `No such file or directory: username` | You typed `<` or `>` in a command. Use your actual username with no brackets, e.g. `profile-octocat`. |
| `git status` shows `template.html` as modified | Copilot (or you) changed the template. Undo it with `git restore template.html`. If you already ran `git add` on it, use `git restore --staged --worktree template.html`. |
| `push` rejected / "permission denied" / 403 | Your Codespace is on the **original repo**, not your fork. If the Codespace offers to create a fork for you, accept it. Otherwise: fork (step 2), open a new Codespace from **your fork**, and copy your file over. Ask an instructor if you're stuck. |
| No **Compare & pull request** banner | The banner disappears after a while. On your fork, click **Contribute** → **Open pull request**. |
| I committed on `main` by accident | Run `git checkout -b profile-YOUR-USERNAME` — your new branch keeps the commit. Then push that branch (step 7). |
| Live Preview command not found | Use the `python3 -m http.server 8000` fallback in step 6. |
| My PR shows changes to other files | Only your own file should be in the PR. Ask an instructor for help. |
