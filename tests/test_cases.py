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

if __name__ == '__main__':
    unittest.main()
