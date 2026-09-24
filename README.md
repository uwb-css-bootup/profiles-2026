# Profiles Gallery — Fall 2026

Welcome! In this workshop you'll add your own **developer trading card** to this repository using Git and GitHub.

## 1. What you'll do

You'll make your own copy of this repo (a *fork*), create a new branch, add one file with your profile card, and send it back here as a **pull request (PR)**. You're done when your PR is merged and your card is part of the gallery. 🎉

> Throughout this guide, replace `<username>` with **your GitHub username** — no angle brackets.
> Example: if your username is `octocat`, then `profile-<username>` becomes `profile-octocat`.

## 2. Fork the repository

1. At the top right of this repo's page on GitHub, click **Fork**.
2. Keep the default settings and click **Create fork**.

You now have your own copy at `github.com/<username>/profiles-fall-2026`. You'll do all your work there.

## 3. Open a Codespace on your fork

1. Make sure you're on **your fork** (the URL should include your username).
2. Click the green **Code** button → **Codespaces** tab → **Create codespace on main**.
3. Wait for the editor to load in your browser. The terminal is at the bottom.

## 4. Create your branch

In the Codespace terminal, run:

```bash
git checkout -b profile-<username>
```

## 5. Make your card with Copilot Chat

Open **Copilot Chat** (the chat icon in the sidebar) and paste this prompt, filling in your own details:

```text
Copy template.html into a new file named <username>.html. Do not change template.html.
In the new file, fill in my details:
- Name: <your name>
- Role or major: <e.g. Computer Science '27>
- Bio: <1–3 sentences about you>
- Tech stack: <languages and tools you use, one badge each>
- Fun fact: <something fun about you>
Keep the same HTML structure and element IDs. You may change the colors in the :root block to match my style.
```

**No Copilot?** No problem — do it by hand:
1. In the file explorer, right-click `template.html` → **Copy**, then right-click the folder → **Paste**.
2. Rename the copy to `<username>.html`.
3. Edit the text under each `✏️ EDIT HERE` comment.

Prefer plain text? Do the same with `template.md` to make `<username>.md` instead.

## 6. Preview your card

Right-click `<username>.html` in the file explorer → **Open with Live Preview** (or **Show Preview**).

*Fallback:* right-click the file → **Download**, then open it in your web browser.

## 7. Commit and push

In the terminal:

```bash
git add .
git commit -m "Add <username> profile"
git push origin profile-<username>
```

Here `origin` is **your fork** — not the original repo. That's exactly where you want to push.

## 8. Open the pull request

1. Go to your fork on GitHub. You'll see a yellow banner: **Compare & pull request**. Click it.
2. Check the top of the page:
   - **base repository**: the instructor's repo, branch `main`
   - **head repository**: your fork, branch `profile-<username>`
3. Title: `Add <username> profile`
4. Click **Create pull request**. Done!

## 9. Rules

- ✅ Only **add your own file** (`<username>.html` or `<username>.md`).
- ❌ Don't edit `template.html` or `template.md`.
- ❌ Don't edit anyone else's file.

Following these rules means no two PRs ever touch the same file — so no merge conflicts.

## 10. Troubleshooting

| Problem | Fix |
| --- | --- |
| `push` rejected / "permission denied" | You're working in the original repo, not your fork. Go back to step 2, fork, and open the Codespace from **your fork**. |
| I committed on `main` by accident | Run `git checkout -b profile-<username>` — your new branch keeps the commit. Then push that branch (step 7). |
| Copilot edited `template.html` | Run `git restore template.html` to undo the change (before committing). |
| My PR shows changes to other files | Only your own file should be in the PR. Ask an instructor for help. |
