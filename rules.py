import re
import html
import uuid

class InlineFormatter:
    @staticmethod
    def format(text):
        # 1. Escape HTML first!
        text = html.escape(text)
        
        # 2. Extract inline code to protect it
        code_blocks = {}
        def replace_code(match):
            uid = str(uuid.uuid4())
            # Content of inline code shouldn't be formatted, but it is HTML escaped
            code_blocks[uid] = f"<code>{match.group(1)}</code>"
            return uid
            
        # Match `...`
        text = re.sub(r'(?<!\\)`([^`]+)`', replace_code, text)
        
        # 3. Apply other formatting
        # Bold: **text**
        text = re.sub(r'(?<!\\)\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        
        # Italic: *text* (that are not bold)
        text = re.sub(r'(?<!\\)\*(.+?)\*', r'<em>\1</em>', text)
        
        # Links: [text](url)
        text = re.sub(r'(?<!\\)\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        # 4. Remove backslash escapes
        text = re.sub(r'\\([\\`*_{}[\]()#+\-.!>])', r'\1', text)
        
        # 5. Restore inline code
        for uid, code_html in code_blocks.items():
            text = text.replace(uid, code_html)
            
        return text

class ASTNode:
    def render(self):
        raise NotImplementedError

class Heading(ASTNode):
    def __init__(self, level, text):
        self.level = level
        self.text = text
        
    def render(self):
        content = InlineFormatter.format(self.text)
        return f"<h{self.level}>{content}</h{self.level}>"

class Paragraph(ASTNode):
    def __init__(self, text):
        self.text = text
        
    def render(self):
        content = InlineFormatter.format(self.text)
        return f"<p>{content}</p>"

class Blockquote(ASTNode):
    def __init__(self, children):
        self.children = children
        
    def render(self):
        inner_html = "\n".join(child.render() for child in self.children)
        return f"<blockquote>\n{inner_html}\n</blockquote>"

class TextNode(ASTNode):
    def __init__(self, text):
        self.text = text
        
    def render(self):
        return InlineFormatter.format(self.text)

class ListItem(ASTNode):
    def __init__(self, children):
        self.children = children
        
    def render(self):
        if len(self.children) == 1 and isinstance(self.children[0], TextNode):
            return f"<li>{self.children[0].render()}</li>"
        else:
            inner_html = "\n".join(child.render() for child in self.children)
            return f"<li>\n{inner_html}\n</li>"

class List(ASTNode):
    def __init__(self, items):
        self.items = items
        
    def render(self):
        inner_html = "\n".join(item.render() for item in self.items)
        return f"<ul>\n{inner_html}\n</ul>"

class CodeBlock(ASTNode):
    def __init__(self, text):
        self.text = text
        
    def render(self):
        # Code block contents are HTML escaped, but inline formatting is NOT applied.
        content = html.escape(self.text)
        return f"<pre><code>{content}</code></pre>"