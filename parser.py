from rules import RULES

def parse(line):
    """Takes one line of markdown, returns one line of HTML."""
    for rule in RULES:
        if rule.matches(line):
            return rule.render(line)
    return line  # should never hit this since ParagraphRule catches everything