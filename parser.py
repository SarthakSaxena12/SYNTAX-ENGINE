import re
from rules import Heading, Paragraph, Blockquote, List, ListItem, CodeBlock, TextNode

def parse_blocks(lines):
    ast_nodes = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Blank line
        if not line.strip():
            i += 1
            continue
            
        # Code Block
        if line.startswith('```'):
            i += 1
            code_lines = []
            while i < len(lines):
                if lines[i].startswith('```'):
                    i += 1
                    break
                code_lines.append(lines[i])
                i += 1
            ast_nodes.append(CodeBlock('\n'.join(code_lines)))
            continue
            
        # Heading
        heading_match = re.match(r'^(#{1,6})\s+(.*)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            ast_nodes.append(Heading(level, text))
            i += 1
            continue
            
        # Blockquote
        if line.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].strip():
                if lines[i].startswith('> '):
                    quote_lines.append(lines[i][2:])
                    i += 1
                elif lines[i].startswith('>'):
                    quote_lines.append(lines[i][1:])
                    i += 1
                else:
                    break
            # Recursively parse inner content
            inner_nodes = parse_blocks(quote_lines)
            ast_nodes.append(Blockquote(inner_nodes))
            continue
            
        # List
        if line.startswith('- '):
            list_items = []
            while i < len(lines) and lines[i].strip():
                if lines[i].startswith('- '):
                    item_text = lines[i][2:].strip()
                    i += 1
                    
                    # Collect nested lines (must be indented by at least 2 spaces)
                    nested_lines = []
                    while i < len(lines) and lines[i].strip():
                        if lines[i].startswith('  '):
                            # Strip 2 spaces of indentation
                            nested_lines.append(lines[i][2:])
                            i += 1
                        elif lines[i].startswith('\t'):
                            # Strip 1 tab of indentation
                            nested_lines.append(lines[i][1:])
                            i += 1
                        else:
                            break
                            
                    if nested_lines:
                        item_children = [TextNode(item_text)]
                        item_children.extend(parse_blocks(nested_lines))
                        list_items.append(ListItem(item_children))
                    else:
                        list_items.append(ListItem([TextNode(item_text)]))
                else:
                    break
            ast_nodes.append(List(list_items))
            continue
            
        # Paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip():
            if len(para_lines) > 0:
                l = lines[i]
                if (l.startswith('```') or 
                    re.match(r'^(#{1,6})\s+', l) or
                    l.startswith('> ') or 
                    l.startswith('- ')):
                    break
                    
            para_lines.append(lines[i].strip())
            i += 1
            
        ast_nodes.append(Paragraph(' '.join(para_lines)))

    return ast_nodes

def parse(lines):
    """Takes a list of markdown lines or a single string, returns complete HTML string."""
    if isinstance(lines, str):
        lines = lines.splitlines()
    
    ast_nodes = parse_blocks(lines)
    html_chunks = [node.render() for node in ast_nodes]
    return '\n'.join(html_chunks)