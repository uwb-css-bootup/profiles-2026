"""Check a student's profile card before they commit it.

Usage: python3 .agents/skills/profile-card/scripts/check_card.py YOUR-USERNAME.html

Prints every problem found and exits 1, or prints "OK" and exits 0.
Uses only the Python standard library.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

FIELDS = ["student-name", "role-or-major", "bio", "tech-stack", "fun-fact"]
PROTECTED = {"template.html", "template.md", "index.html", "README.md", "AGENTS.md"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
PLACEHOLDERS = ["Your Name", "A sentence or two about who you are", "something surprising about you"]


class CardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.ids, self.problems = [], [], []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == "id":
                self.ids.append(value)
            if name.startswith("on"):
                self.problems.append(f"<{tag}> has a JavaScript attribute ({name}); remove it")
        if tag == "script":
            self.problems.append("<script> tags are not allowed")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.problems.append(f"unexpected </{tag}> (check for a missing or extra closing tag)")


def check(path):
    problems = []
    if path.name in PROTECTED:
        return [f"{path.name} is a shared file; your card should be YOUR-USERNAME{path.suffix}"]
    if path.parent.resolve() != Path.cwd().resolve():
        problems.append("the card must be in the top folder of the repo")
    text = path.read_text(encoding="utf-8")
    if re.search(r"(https?:)?//[a-z0-9]", text, re.I):
        problems.append("external links/URLs are not allowed (no http://, https://, or //)")
    visible = re.sub(r"<!--.*?-->", "", text, flags=re.S).lower()
    for placeholder in PLACEHOLDERS:
        if placeholder.lower() in visible:
            problems.append(f'still has placeholder text: "{placeholder}"')
    if path.suffix == ".html":
        parser = CardParser()
        parser.feed(text)
        problems += parser.problems
        if parser.stack:
            problems.append(f"unclosed tags: {', '.join(parser.stack)}")
        for field in FIELDS:
            count = parser.ids.count(field)
            if count != 1:
                problems.append(f'id="{field}" should appear exactly once (found {count})')
    elif path.suffix != ".md":
        problems.append("the card must be a .html or .md file")
    return problems


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    if not path.is_file():
        sys.exit(f"{path} not found")
    problems = check(path)
    for problem in problems:
        print(f"✗ {problem}")
    if problems:
        sys.exit(1)
    print(f"OK: {path.name} looks good")


if __name__ == "__main__":
    main()
