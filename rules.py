import re

class HeadingRule:
    """Matches ATX-style headings: # through ######"""

    pattern = re.compile(r'^(#{1,6})\s+(.*)$')

    @classmethod
    def matches(cls, line):
        return cls.pattern.match(line) is not None

    @classmethod
    def render(cls, line):
        match = cls.pattern.match(line)
        level = len(match.group(1))      # number of #'s = heading level
        content = match.group(2).strip()
        return f"<h{level}>{content}</h{level}>"


class ParagraphRule:
    """Fallback rule: anything that matches nothing else becomes a paragraph"""

    @classmethod
    def matches(cls, line):
        return True  # always matches — must be checked LAST

    @classmethod
    def render(cls, line):
        return f"<p>{line}</p>"


# The registry — order matters. ParagraphRule is the catch-all, so it's last.
RULES = [
    HeadingRule,
    ParagraphRule,
]