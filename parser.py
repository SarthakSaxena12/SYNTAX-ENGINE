from rules import registry

def parse_blocks(lines):
    ast_nodes = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if not line.strip():
            i += 1
            continue
            
        matched = False
        for rule in registry.block_rules:
            if rule.match(lines, i):
                node, i = rule.consume(lines, i, parse_blocks)
                ast_nodes.append(node)
                matched = True
                break
                
        # Fallback to prevent infinite loops if no rule matches
        if not matched:
            i += 1
            
    return ast_nodes

def parse(lines):
    """Takes a list of markdown lines or a single string, returns complete HTML string."""
    if isinstance(lines, str):
        lines = lines.splitlines()
    
    ast_nodes = parse_blocks(lines)
    html_chunks = [node.render() for node in ast_nodes]
    return '\n'.join(html_chunks)