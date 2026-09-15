import re
import html
import uuid

# --- AST Nodes ---
class ASTNode:
    def render(self):
        raise NotImplementedError

class TextNode(ASTNode):
    def __init__(self, text):
        self.text = text
    def render(self):
        return InlineFormatter.format(self.text)

class Heading(ASTNode):
    def __init__(self, level, text):
        self.level = level
        self.text = text
    def render(self):
        return f"<h{self.level}>{InlineFormatter.format(self.text)}</h{self.level}>"

class Paragraph(ASTNode):
    def __init__(self, text):
        self.text = text
    def render(self):
        return f"<p>{InlineFormatter.format(self.text)}</p>"

class Blockquote(ASTNode):
    def __init__(self, children):
        self.children = children
    def render(self):
        inner = "\n".join(c.render() for c in self.children)
        return f"<blockquote>\n{inner}\n</blockquote>"

class List(ASTNode):
    def __init__(self, items):
        self.items = items
    def render(self):
        inner = "\n".join(item.render() for item in self.items)
        return f"<ul>\n{inner}\n</ul>"

class ListItem(ASTNode):
    def __init__(self, children, is_task=False, checked=False):
        self.children = children
        self.is_task = is_task
        self.checked = checked
    def render(self):
        prefix = ""
        if self.is_task:
            check_attr = " checked" if self.checked else ""
            prefix = f'<input type="checkbox" disabled{check_attr}> '
            
        if len(self.children) == 1 and isinstance(self.children[0], TextNode):
            return f"<li>{prefix}{self.children[0].render()}</li>"
        else:
            inner = "\n".join(c.render() for c in self.children)
            if self.is_task and len(self.children) > 0 and isinstance(self.children[0], TextNode):
                first_rendered = self.children[0].render()
                rest = "\n".join(c.render() for c in self.children[1:])
                return f"<li>\n{prefix}{first_rendered}\n{rest}\n</li>"
            return f"<li>\n{prefix}{inner}\n</li>"

class CodeBlock(ASTNode):
    def __init__(self, text):
        self.text = text
    def render(self):
        return f"<pre><code>{html.escape(self.text)}</code></pre>"

class Table(ASTNode):
    def __init__(self, headers, alignments, rows):
        self.headers = headers
        self.alignments = alignments
        self.rows = rows
    
    def _render_cell(self, text, is_header, align):
        tag = "th" if is_header else "td"
        attr = f' align="{align}"' if align else ""
        return f"<{tag}{attr}>{InlineFormatter.format(text)}</{tag}>"

    def render(self):
        html_out = ["<table>", "<thead>", "<tr>"]
        for i, h in enumerate(self.headers):
            align = self.alignments[i] if i < len(self.alignments) else None
            html_out.append(self._render_cell(h, True, align))
        html_out.extend(["</tr>", "</thead>", "<tbody>"])
        for row in self.rows:
            html_out.append("<tr>")
            for i, cell in enumerate(row):
                align = self.alignments[i] if i < len(self.alignments) else None
                html_out.append(self._render_cell(cell, False, align))
            html_out.append("</tr>")
        html_out.extend(["</tbody>", "</table>"])
        return "\n".join(html_out)


# --- Registry & Rules ---
class ParserRegistry:
    def __init__(self):
        self.block_rules = []
        self.inline_rules = []
    
    def register_block_rule(self, rule):
        self.block_rules.append(rule)
        
    def register_inline_rule(self, rule):
        self.inline_rules.append(rule)

registry = ParserRegistry()

class BlockRule:
    def match(self, lines, i):
        raise NotImplementedError
    def consume(self, lines, i, parse_blocks_fn):
        raise NotImplementedError

class InlineRule:
    def apply(self, text):
        raise NotImplementedError

class RegexInlineRule(InlineRule):
    def __init__(self, pattern, replacement):
        self.pattern = re.compile(pattern)
        self.replacement = replacement
    def apply(self, text):
        return self.pattern.sub(self.replacement, text)

# GFM Strikethrough
class StrikethroughRule(RegexInlineRule):
    def __init__(self):
        super().__init__(r'(?<!\\)~~(.+?)~~', r'<del>\1</del>')

class AutolinkRule(RegexInlineRule):
    def __init__(self):
        super().__init__(r'&lt;((?:https?|ftp)://[^&]+)&gt;', r'<a href="\1">\1</a>')

class EmailAutolinkRule(RegexInlineRule):
    def __init__(self):
        super().__init__(r'&lt;([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})&gt;', r'<a href="mailto:\1">\1</a>')

# Default inline formatter using registry
class InlineFormatter:
    @staticmethod
    def format(text):
        text = html.escape(text)
        
        # 1. Protect inline code
        code_blocks = {}
        def replace_code(match):
            uid = str(uuid.uuid4())
            code_blocks[uid] = f"<code>{match.group(1)}</code>"
            return uid
            
        text = re.sub(r'(?<!\\)`([^`]+)`', replace_code, text)
        
        # 2. Apply dynamic inline rules from registry
        for rule in registry.inline_rules:
            text = rule.apply(text)
            
        # 3. Remove backslash escapes
        text = re.sub(r'\\([\\`*_{}[\]()#+\-.!>~|])', r'\1', text)
        
        # 4. Restore inline code
        for uid, code_html in code_blocks.items():
            text = text.replace(uid, code_html)
            
        return text

# Register default inline rules
registry.register_inline_rule(RegexInlineRule(r'(?<!\\)\*\*(.+?)\*\*', r'<strong>\1</strong>'))
registry.register_inline_rule(RegexInlineRule(r'(?<!\\)\*(.+?)\*', r'<em>\1</em>'))
registry.register_inline_rule(RegexInlineRule(r'(?<!\\)\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>'))
registry.register_inline_rule(StrikethroughRule())
registry.register_inline_rule(AutolinkRule())
registry.register_inline_rule(EmailAutolinkRule())

# Default Block Rules
class HeadingRule(BlockRule):
    def match(self, lines, i):
        return bool(re.match(r'^(#{1,6})\s+(.*)$', lines[i]))
    def consume(self, lines, i, parse_blocks_fn):
        m = re.match(r'^(#{1,6})\s+(.*)$', lines[i])
        return Heading(len(m.group(1)), m.group(2).strip()), i + 1

class CodeBlockRule(BlockRule):
    def match(self, lines, i):
        return lines[i].startswith('```')
    def consume(self, lines, i, parse_blocks_fn):
        i += 1
        code_lines = []
        while i < len(lines):
            if lines[i].startswith('```'):
                i += 1
                break
            code_lines.append(lines[i])
            i += 1
        return CodeBlock('\n'.join(code_lines)), i

class BlockquoteRule(BlockRule):
    def match(self, lines, i):
        return lines[i].startswith('> ') or lines[i].startswith('>')
    def consume(self, lines, i, parse_blocks_fn):
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
        return Blockquote(parse_blocks_fn(quote_lines)), i

class ListRule(BlockRule):
    def match(self, lines, i):
        return lines[i].startswith('- ')
    def consume(self, lines, i, parse_blocks_fn):
        list_items = []
        while i < len(lines) and lines[i].strip():
            if lines[i].startswith('- '):
                item_text = lines[i][2:].strip()
                i += 1
                
                # Check for Task List
                is_task = False
                checked = False
                if item_text.startswith('[ ] '):
                    is_task = True
                    item_text = item_text[4:]
                elif item_text.startswith('[x] ') or item_text.startswith('[X] '):
                    is_task = True
                    checked = True
                    item_text = item_text[4:]
                
                nested_lines = []
                while i < len(lines) and lines[i].strip():
                    if lines[i].startswith('  '):
                        nested_lines.append(lines[i][2:])
                        i += 1
                    elif lines[i].startswith('\t'):
                        nested_lines.append(lines[i][1:])
                        i += 1
                    else:
                        break
                        
                item_children = [TextNode(item_text)] if item_text else []
                if nested_lines:
                    item_children.extend(parse_blocks_fn(nested_lines))
                
                list_items.append(ListItem(item_children, is_task, checked))
            else:
                break
        return List(list_items), i

class TableRule(BlockRule):
    def match(self, lines, i):
        if i + 1 >= len(lines):
            return False
        if '|' not in lines[i]: return False
        if '|' not in lines[i+1]: return False
        
        sep = lines[i+1].strip()
        if not re.match(r'^\|?(\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?$', sep) and not re.match(r'^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?$', sep):
            return False
        return True
        
    def _parse_row(self, line):
        line = line.strip()
        if line.startswith('|'): line = line[1:]
        if line.endswith('|'): line = line[:-1]
        return [c.strip() for c in line.split('|')]
        
    def consume(self, lines, i, parse_blocks_fn):
        headers = self._parse_row(lines[i])
        sep_cols = self._parse_row(lines[i+1])
        alignments = []
        for col in sep_cols:
            col = col.strip()
            if col.startswith(':') and col.endswith(':'):
                alignments.append("center")
            elif col.endswith(':'):
                alignments.append("right")
            elif col.startswith(':'):
                alignments.append("left")
            else:
                alignments.append(None)
                
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip() and '|' in lines[i]:
            rows.append(self._parse_row(lines[i]))
            i += 1
            
        return Table(headers, alignments, rows), i

class ParagraphRule(BlockRule):
    def match(self, lines, i):
        return True
    def consume(self, lines, i, parse_blocks_fn):
        para_lines = []
        while i < len(lines) and lines[i].strip():
            if len(para_lines) > 0:
                interrupted = False
                for rule in registry.block_rules:
                    if rule is not self and rule.match(lines, i):
                        interrupted = True
                        break
                if interrupted:
                    break
                    
            para_lines.append(lines[i].strip())
            i += 1
        return Paragraph(' '.join(para_lines)), i

registry.register_block_rule(CodeBlockRule())
registry.register_block_rule(TableRule())
registry.register_block_rule(HeadingRule())
registry.register_block_rule(BlockquoteRule())
registry.register_block_rule(ListRule())
registry.register_block_rule(ParagraphRule())