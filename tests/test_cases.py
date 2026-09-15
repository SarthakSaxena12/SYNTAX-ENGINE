import unittest
import sys
import os

# Add the parent directory to sys.path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import parse

class TestMarkdownEngine(unittest.TestCase):
    def test_heading(self):
        lines = ["# Title", "## Subtitle"]
        expected = "<h1>Title</h1>\n<h2>Subtitle</h2>"
        self.assertEqual(parse(lines), expected)
        
    def test_paragraph_and_inline(self):
        lines = ["This is **bold** and *italic*.", "", "Another paragraph with [link](url)."]
        expected = "<p>This is <strong>bold</strong> and <em>italic</em>.</p>\n<p>Another paragraph with <a href=\"url\">link</a>.</p>"
        self.assertEqual(parse(lines), expected)
        
    def test_list(self):
        lines = ["- item one", "- item two"]
        expected = "<ul>\n<li>item one</li>\n<li>item two</li>\n</ul>"
        self.assertEqual(parse(lines), expected)
        
    def test_blockquote_and_nesting(self):
        lines = [
            "> A quote with a list inside:",
            "> - point one",
            "> - point two"
        ]
        expected = "<blockquote>\n<p>A quote with a list inside:</p>\n<ul>\n<li>point one</li>\n<li>point two</li>\n</ul>\n</blockquote>"
        self.assertEqual(parse(lines), expected)
        
    def test_escaping(self):
        lines = ["This has <script> tags"]
        expected = "<p>This has &lt;script&gt; tags</p>"
        self.assertEqual(parse(lines), expected)

    def test_code_block(self):
        lines = ["```", "**bold** code", "```"]
        expected = "<pre><code>**bold** code</code></pre>"
        self.assertEqual(parse(lines), expected)
        
    def test_complex_inline_styles(self):
        lines = ["Here is **bold and *italic* inside** bold.", "", "And a **[link](http://example.com)**."]
        expected = "<p>Here is <strong>bold and <em>italic</em> inside</strong> bold.</p>\n<p>And a <strong><a href=\"http://example.com\">link</a></strong>.</p>"
        self.assertEqual(parse(lines), expected)
        
    def test_inline_code_protection(self):
        lines = ["This is `some **bold** code` and this is **bold**."]
        expected = "<p>This is <code>some **bold** code</code> and this is <strong>bold</strong>.</p>"
        self.assertEqual(parse(lines), expected)

    def test_complex_block_nesting(self):
        lines = [
            "- List item 1",
            "  > Blockquote in list",
            "  > - Nested list in blockquote",
            "- List item 2"
        ]
        expected = (
            "<ul>\n"
            "<li>\n"
            "List item 1\n"
            "<blockquote>\n"
            "<p>Blockquote in list</p>\n"
            "<ul>\n"
            "<li>Nested list in blockquote</li>\n"
            "</ul>\n"
            "</blockquote>\n"
            "</li>\n"
            "<li>List item 2</li>\n"
            "</ul>"
        )
        self.assertEqual(parse(lines), expected)
        
    def test_multiple_paragraphs(self):
        lines = [
            "Paragraph one.",
            "",
            "Paragraph two."
        ]
        expected = "<p>Paragraph one.</p>\n<p>Paragraph two.</p>"
        self.assertEqual(parse(lines), expected)

if __name__ == '__main__':
    unittest.main()
