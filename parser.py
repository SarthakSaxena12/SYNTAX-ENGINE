from rules import RULES

def parse_blocks(lines):
    output = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if not line.strip():
            i += 1
            continue
            
        for rule_class in RULES:
            if rule_class.starts(line):
                html_chunk, consumed = rule_class.consume(lines, i)
                output.append(html_chunk)
                i += consumed
                break
                
    return '\n'.join(output)

def parse(lines):
    """Takes a list of markdown lines or a single string, returns complete HTML string."""
    if isinstance(lines, str):
        lines = lines.splitlines()
    return parse_blocks(lines)