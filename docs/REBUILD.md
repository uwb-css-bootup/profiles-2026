# Rebuild Guide — Profiles Gallery (Fall 2026)

How this repository was built, in order, and how to check the result. Use it when you set up a new term or make a fresh copy.
The files in the repo are the source of truth. This guide points to them and doesn't copy them.
For the full reasoning behind each choice, see [DESIGN.md](DESIGN.md). To run the class, see [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md).

---

## 1. Requirements

- `git`
- Python 3 (standard library only; tested with 3.9)
- Optional, for visual checks: Google Chrome (headless screenshots)

## 2. File tree

```
profiles-fall-2026/              (GitHub repo: uwb-css-bootup/profiles-2026)
├── .agents/skills/profile-card/
│   ├── SKILL.md                (AI assistant instructions for making a card)
│   └── scripts/check_card.py   (card validator the skill runs)
├── .claude/skills/profile-card → ../../.agents/skills/profile-card   (symlink)
├── .devcontainer/devcontainer.json   (Codespace image + Live Preview)
├── .github/
│   ├── pull_request_template.md     (student PR checklist)
│   └── workflows/build-gallery.yml  (rebuilds index.html after each merge)
├── docs/
│   ├── DESIGN.md               (why things are the way they are)
│   ├── INSTRUCTOR_GUIDE.md     (running the class)
│   └── REBUILD.md              (this file)
├── .gitignore                  (OS/editor junk)
├── .nojekyll                   (empty; turns off Jekyll on Pages)
├── AGENTS.md                   (short rules for AI tools, points to the skill)
├── README.md                   (student walkthrough)
├── build_index.py              (generates index.html)
├── index.html                  (generated; never edited by hand)
├── profiles/                   (student cards, added by PR; absent until the first one)
├── template.html               (the card students copy)
└── template.md                 (plain-text alternative)
```

## 3. Build steps

Each step lists what to create, the key choices, and where to look. Build in this order: each step relies on the ones before it.

### 3.1 Repo skeleton
```bash
mkdir profiles-fall-2026 && cd profiles-fall-2026
git init -b main
touch .nojekyll
```
- `.gitignore` covers only OS/editor clutter (`.DS_Store`, `Thumbs.db`, `.vscode/`). Students commit one file, so nothing else needs ignoring.
- `.nojekyll` makes GitHub Pages serve files exactly as committed. Without it, Jekyll turns `NAME.md` cards into HTML. See [DESIGN §6](DESIGN.md#why-nojekyll).

### 3.2 The card: `template.html` and `template.md`
- One self-contained HTML file: all CSS in a single `<style>` block, **no JavaScript, no web fonts, no external URLs**. It looks the same offline, in Live Preview, and on Pages.
- The theme is five CSS variables in `:root` (`--bg`, `--card`, `--text`, `--muted`, `--accent`), so students or Copilot can restyle the card by changing one block.
- The five editable fields have stable ids (`student-name`, `role-or-major`, `bio`, `tech-stack`, `fun-fact`), each with an `✏️ EDIT HERE` comment. The ids let Copilot, the skill, and `check_card.py` find fields reliably.
- The placeholder text is obviously fake ("Your Name"), so an unedited card stands out in review.
- `template.md` has the same fields in the same order, for students who prefer plain text or can't use Copilot.

See `template.html`, `template.md`, and [DESIGN §3](DESIGN.md#3-the-card-templatehtml).

### 3.3 Student walkthrough: `README.md`
Ten numbered steps: fork → Codespace on the fork → `git checkout -b profile-YOUR-USERNAME` → `cp template.html profiles/YOUR-USERNAME.html` → fill in (Copilot, the AI skill, or by hand) → preview → `git status` / `git add` / commit / push → PR. Each step has a one-line "Why:".
- **`YOUR-USERNAME`, not `<username>`:** students paste commands, and in bash `<` is input redirection, which gives errors that don't hint at the fix.
- **`cp` before Copilot:** copying is a deterministic terminal step. Copilot is then asked to edit only the open file, which works in Ask mode and keeps `template.html` untouched.
- **`git add profiles/YOUR-USERNAME.html`, not `git add .`:** staging just the one file enforces the "only your file" rule and teaches what the staging area is for.

See `README.md` and [DESIGN §4](DESIGN.md#4-student-readme--design-choices).

### 3.4 Codespace: `.devcontainer/devcontainer.json`
- The image is `mcr.microsoft.com/devcontainers/universal:linux`, the tag Codespaces uses as its default. It stays cached on Codespaces hosts, so 30 students can start at once, and the storage isn't billed to them. A pinned major version or the smaller `python` image would lose both.
- It adds the Live Preview extension and labels port 8000 "Card preview", which opens automatically for the `python3 -m http.server 8000` fallback.
- There's no `postCreateCommand` or extra features, because there's nothing to install.

See `.devcontainer/devcontainer.json`, [DESIGN "Why a devcontainer"](DESIGN.md#why-a-devcontainer), and the check in [§5.6](#56-devcontainer-image-check).

### 3.5 PR template: `.github/pull_request_template.md`
- A four-item checklist (one file, filename = username, previewed, title `Add YOUR-USERNAME profile`) that reminds students when they submit.
- It deliberately has no enforcement Action: nothing runs CI on student PRs, and the *Files changed* tab already shows any extra files.

See [DESIGN §5](DESIGN.md#5-pull-request-template).

### 3.6 Gallery: `build_index.py` → `index.html`
- Python standard library only, so there's nothing to install locally or in CI.
- `CARDS_DIR = "profiles"` is the single place the cards folder is named. Every `.html`/`.md` file there is a card, and shared files never live there, so no skip list is needed.
- HTML cards are embedded as `<iframe sandbox>` with no `allow-*` flags, so a student's script can't reach or rewrite the gallery.
- `.md` cards become tiles that link to GitHub's rendered view. The repo URL comes from `git remote get-url origin`.
- A dashed "Your card goes here" ghost tile shows until there are `GHOST_TILE_BELOW` (4) cards.
- `index.html` is a generated file. Create it by running the script, never by hand:
  ```bash
  python3 build_index.py        # → "Wrote index.html with 0 cards from profiles/."
  ```

See `build_index.py` and [DESIGN §6](DESIGN.md#6-gallery).

### 3.7 Auto-rebuild: `.github/workflows/build-gallery.yml`
- The workflow runs after a merge to `main` (plus a manual **Run workflow** button), never on PRs, so it can't block or confuse students. It commits `index.html` only when it changed.
- `concurrency` with no cancel, plus `git pull --rebase` before pushing, handles back-to-back merges during class.
- The `paths:` filter (`profiles/**`, `build_index.py`) can't read variables. **Keep it in sync with `CARDS_DIR`** if you rename the folder.
- It needs **Read and write** workflow permissions ([INSTRUCTOR_GUIDE §1.3](INSTRUCTOR_GUIDE.md#13-recommended-repo-settings)).

See [DESIGN "Why a post-merge workflow"](DESIGN.md#why-a-post-merge-workflow).

### 3.8 AI assistant skill
- `.agents/skills/profile-card/SKILL.md` follows the Agent Skills format. Copilot, Gemini CLI, Codex, and others find it in `.agents/skills/`. The skill makes the card but tells the student which Git commands to run, so they still learn Git.
- `scripts/check_card.py` is a stdlib validator. It checks for placeholders left in, URLs, scripts, a missing or duplicated id, a card outside `profiles/`, or a shared file edited by mistake.
- Claude Code looks only in `.claude/skills/`, so link to the one real copy instead of keeping a second one:
  ```bash
  mkdir -p .claude/skills
  ln -s ../../.agents/skills/profile-card .claude/skills/profile-card
  ```
- `AGENTS.md` is short and scoped to students: it points to the skill and restates the hard rules. There's no `CLAUDE.md`/`GEMINI.md`, because those would load for the instructor too.

See [DESIGN §7](DESIGN.md#7-ai-assistant-skill-profile-card).

### 3.9 Instructor docs
- `docs/INSTRUCTOR_GUIDE.md`: setup, rehearsal, run of show, merging, and fixes.
- `docs/DESIGN.md`: the reasoning behind every choice above.
- `docs/REBUILD.md`: this file.

Then run the checks in [§5](#5-verification) and commit:
```bash
git add -A
git commit -m "Initial commit: Set up profiles gallery repository"
```

## 4. Original history

The first commit (`d73a3b2`, same message as above) had only `.gitignore`, `template.html`, `template.md`, and `README.md`, in their pre-review form. Everything else came from the review pass described in [DESIGN.md §9](DESIGN.md#9-history). Building the final state in one commit is fine.

---

## 5. Verification

These checks test how the repo behaves, not exact file contents, so they still work after you change a file on purpose.

### 5.1 Template well-formedness (stdlib only)
```python
from html.parser import HTMLParser

VOID = {"meta", "br", "img", "hr", "link", "input"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.ids, self.errors = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(tag)
        else:
            self.stack.pop()


src = open("template.html", encoding="utf-8").read()
checker = Checker()
checker.feed(src)
assert "http" not in src, "external URL found"
assert not checker.stack and not checker.errors, (checker.stack, checker.errors)
for field in ["student-name", "role-or-major", "bio", "tech-stack", "fun-fact"]:
    assert checker.ids.count(field) == 1, field
print("template.html OK")
```

### 5.2 Student flow (run in a throwaway copy, under bash)
```bash
git checkout -b profile-octocat
mkdir -p profiles
cp template.html profiles/octocat.html
echo "<!-- oops -->" >> template.html          # simulate an accidental template edit
git add profiles/octocat.html template.html
git restore --staged --worktree template.html
git status --short                             # expect only: A  profiles/octocat.html
```

### 5.3 Card checker
```bash
mkdir -p profiles
cp template.html profiles/octocat.html
python3 .agents/skills/profile-card/scripts/check_card.py profiles/octocat.html   # 3 placeholder errors, exit 1
python3 .agents/skills/profile-card/scripts/check_card.py template.html           # "shared file", exit 1
cp template.html octocat.html
python3 .agents/skills/profile-card/scripts/check_card.py octocat.html            # also "must be in the profiles/ folder", exit 1
rm profiles/octocat.html octocat.html
```

### 5.4 Gallery and sandbox (throwaway copy)
```bash
git remote add origin git@github.com:instructor/profiles-fall-2026.git
mkdir -p profiles
sed 's/Your Name/Octo Cat/' template.html > profiles/octocat.html
sed -e 's/Your Name/Evil Student/' \
    -e 's#</body>#<script>try{top.document.body.innerHTML="<h1>GALLERY PWNED</h1>"}catch(e){}</script></body>#' \
    template.html > profiles/evil.html
cp template.md profiles/mona.md
python3 build_index.py                         # → "Wrote index.html with 3 cards from profiles/."
python3 -m http.server 8765
```
Open `http://localhost:8765/`: three tiles, the Evil Student card renders normally and the gallery is intact. Open `http://localhost:8765/profiles/evil.html` directly: the page shows "GALLERY PWNED" (proves the sandbox is what protects the gallery). The `mona` tile links to `https://github.com/instructor/profiles-fall-2026/blob/main/profiles/mona.md`.

### 5.5 Visual check (optional, macOS)
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --hide-scrollbars --screenshot=/tmp/card-desktop.png \
  --window-size=1280,900 "file://$PWD/template.html"
```
Expected: a dark navy page with one centered 380px card, sky-blue border, "Your Name", "Computer Science '27" in blue, bio, "TECH STACK" label with three pill badges (Python, JavaScript, Git), and an italic grey fun fact. Headless Chrome clamps very narrow windows, so for a true 390px mobile check load the card inside a 390px-wide `<iframe>` instead.

### 5.6 Devcontainer image check
`devcontainer.json` uses `universal:linux`, the tag Codespaces uses as its default, so it stays cached and storage-free. To see which version that currently is:
```bash
for tag in linux latest; do
  printf "%-6s " "$tag"
  curl -sI -H "Accept: application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json" \
    "https://mcr.microsoft.com/v2/devcontainers/universal/manifests/$tag" | grep -i "^docker-content-digest"
done
npx -y @devcontainers/cli read-configuration --workspace-folder .   # config parses
```
As of Sept 2026 both print `sha256:584e41561451c910dcd96221634be07545803aed9cd437a60288f06ddeaf5880` (version 6.1.7). If the major version has changed, rehearse in a real Codespace before class.
