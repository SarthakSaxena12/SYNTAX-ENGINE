import re
import html

def apply_inline_formatting(text):
    # Step 4: Escaping HTML
    text = html.escape(text)
    
    # Step 5: Inline formatting (regex)
    # Bold text
    text = re.sub(r'(?<!\\)\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic text
    text = re.sub(r'(?<!\\)\*([^*]+)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'(?<!\\)`([^`]+)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'(?<!\\)\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Remove backslash escapes
    text = re.sub(r'\\([\\`*_{}[\]()#+\-.!>])', r'\1', text)
    
    return text

class HeadingRule:
    pattern = re.compile(r'^(#{1,6})\s+(.*)$')
    
    @classmethod
    def starts(cls, line):
        return cls.pattern.match(line) is not None
        
    @classmethod
    def consume(cls, lines, index):
        line = lines[index]
        match = cls.pattern.match(line)
        level = len(match.group(1))
        content = apply_inline_formatting(match.group(2).strip())
        return f"<h{level}>{content}</h{level}>", 1

class ListRule:
    @classmethod
    def starts(cls, line):
        return line.startswith('- ')
        
    @classmethod
    def consume(cls, lines, index):
        from parser import parse_blocks
        i = index
        items_html = []
        
        while i < len(lines) and lines[i].strip():
            if lines[i].startswith('- '):
                item_text = apply_inline_formatting(lines[i][2:].strip())
                i += 1
                nested_lines = []
                while i < len(lines) and lines[i].strip() and lines[i].startswith('  '):
                    nested_lines.append(lines[i][2:])
                    i += 1
                
                if nested_lines:
                    nested_html = parse_blocks(nested_lines)
                    items_html.append(f"<li>{item_text}\n{nested_html}</li>")
                else:
                    items_html.append(f"<li>{item_text}</li>")
            else:
                break
                
        html_out = "<ul>\n" + "\n".join(items_html) + "\n</ul>"
        return html_out, (i - index)

class BlockquoteRule:
    @classmethod
    def starts(cls, line):
        return line.startswith('> ')
        
    @classmethod
    def consume(cls, lines, index):
        from parser import parse_blocks
        i = index
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
        
        inner_html = parse_blocks(quote_lines)
        return f"<blockquote>\n{inner_html}\n</blockquote>", (i - index)

class CodeBlockRule:
    @classmethod
    def starts(cls, line):
        return line.startswith('```')
        
    @classmethod
    def consume(cls, lines, index):
        i = index + 1
        code_lines = []
        while i < len(lines):
            if lines[i].startswith('```'):
                i += 1
                break
            code_lines.append(html.escape(lines[i]))
            i += 1
        
        content = '\n'.join(code_lines)
        return f"<pre><code>{content}</code></pre>", (i - index)

class ParagraphRule:
    @classmethod
    def starts(cls, line):
        return True
        
    @classmethod
    def consume(cls, lines, index):
        i = index
        para_lines = []
        while i < len(lines) and lines[i].strip():
            if i > index:
                if HeadingRule.starts(lines[i]) or ListRule.starts(lines[i]) or BlockquoteRule.starts(lines[i]) or CodeBlockRule.starts(lines[i]):
                    break
            para_lines.append(lines[i].strip())
            i += 1
            
        content = ' '.join(para_lines)
        content = apply_inline_formatting(content)
        return f"<p>{content}</p>", (i - index)

RULES = [
    HeadingRule,
    ListRule,
    BlockquoteRule,
    CodeBlockRule,
    ParagraphRule,
]