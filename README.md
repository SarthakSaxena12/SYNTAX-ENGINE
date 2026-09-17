# Syntax Engine

Syntax Engine is a lightweight, Python-based Markdown-to-HTML parser designed to convert Markdown documents into semantic HTML using a rules-driven parsing system. It is intentionally compact, dependency-free, and easy to extend, making it suitable for learning parser design, prototyping document pipelines, or generating HTML from Markdown files in simple applications.

The project combines:

- A block parser for Markdown structures such as headings, paragraphs, lists, blockquotes, tables, and code blocks
- An inline formatter for emphasis, links, autolinks, inline code, and strikethrough
- A simple command-line interface for converting Markdown files to HTML
- A conformance-style test setup for checking parser behavior against expected HTML output

## Why this project exists

Many Markdown parsers are large, heavy, and difficult to understand. Syntax Engine aims to provide a clear, readable implementation that makes the parsing pipeline easy to inspect and extend. The code is organized around explicit parsing rules, which makes it useful as both a functional project and as a teaching example for parser architecture.

## Features

Syntax Engine supports a wide range of Markdown constructs, including:

- Headings (`#`, `##`, etc.)
- Paragraphs
- Strong and emphasized text (`**bold**`, `*italic*`)
- Inline code with protection from markdown formatting rules
- Links (`[text](url)`)
- Strikethrough (`~~text~~`)
- Autolinks for URLs and email addresses
- Blockquotes
- Unordered lists
- Nested lists and blockquotes inside list items
- Task lists (`- [ ]`, `- [x]`)
- Code fences (```...```)
- Markdown tables
- HTML escaping for safety

## Project structure

- `main.py` — CLI entry point for converting Markdown files to HTML and running conformance checks
- `parser.py` — orchestrates block parsing and returns final HTML
- `rules.py` — contains the AST node definitions, inline rules, and block rules
- `sample.md` — sample Markdown used to demonstrate conversion behavior
- `output.html` — generated example HTML output
- `tests/spec.json` — conformance-style specification data
- `tests/test_cases.py` — unit tests covering common Markdown parsing scenarios
- `setup.py` — package metadata and console entry point configuration

## Installation

Clone the repository:

```bash
git clone https://github.com/SarthakSaxena12/SYNTAX-ENGINE.git
cd SYNTAX-ENGINE
```

Install locally in editable mode:

```bash
pip install -e .
```

This installs the `md-engine` console command:

```bash
md-engine your-file.md -o output.html
```

## Usage

### Convert a Markdown file to HTML

```bash
python main.py sample.md -o output.html
```

This reads the input Markdown file, parses it, wraps the result in a minimal HTML document, and writes it to `output.html`.

### Run the conformance checker

```bash
python main.py tests/spec.json --conformance --verbose
```

This loads a specification file containing expected Markdown-to-HTML examples and prints a report showing how many cases passed.

## Example

### Input (`sample.md`)

```markdown
# Markdown Engine Test

This is a **bold** and *italic* paragraph with `inline code` and a [link](https://google.com).

## Lists and Blockquotes

- This is a list item
- Another list item with a nested blockquote:
  > **Blockquote** inside a list!

```python
def hello_world():
    print("Hello, **Markdown**!")
```
```

### Output

```html
<h1>Markdown Engine Test</h1>
<p>This is a <strong>bold</strong> and <em>italic</em> paragraph with <code>inline code</code> and a <a href="https://google.com">link</a>.</p>
<h2>Lists and Blockquotes</h2>
<ul>
<li>This is a list item</li>
<li>Another list item with a nested blockquote:
<blockquote>
<p><strong>Blockquote</strong> inside a list!</p>
</blockquote>
</li>
</ul>
<pre><code>def hello_world():
    print("Hello, **Markdown**!")
</code></pre>
```

## Architecture overview

The parser follows a simple rule-based design:

1. `parse()` splits input into lines and passes them to the block parser.
2. `parse_blocks()` iterates through the document and applies registered block rules.
3. Each block rule consumes matching Markdown constructs and builds AST nodes.
4. Nodes render themselves to HTML.
5. Inline formatting is handled by `InlineFormatter`, which escapes text, protects inline code, and applies registered inline transformations.

This architecture makes it straightforward to add or customize support for new Markdown features.

## Supported syntax highlights

The parser currently includes support for:

- Markdown headings
- Paragraphs and whitespace separation
- Emphasis and strong formatting
- Inline code
- Links and autolinks
- Lists, including nested items and task lists
- Nested blockquotes and block-level structures
- Tables aligned with `:` markers
- Code blocks fenced with triple backticks
- Strikethrough with `~~text~~`

## Testing

The repository includes tests for the parser's core behaviors. To run the suite:

```bash
python -m unittest discover -s tests
```

The project also includes a conformance-style JSON spec file in `tests/spec.json`, which can be used for broader regression checking.

## Notes

This project is intentionally compact and uses only the Python standard library. It is a good fit for:

- educational use
- small documentation rendering pipelines
- parser experimentation
- custom Markdown preprocessing tasks

## Contributing

Contributions are welcome. If you want to improve the parser:

- add or refine a rule in `rules.py`
- extend parsing logic in `parser.py`
- add tests to `tests/test_cases.py`
- validate behavior with the conformance checks

If you are using the project as a foundation for a more feature-rich Markdown engine, the modular rule-based structure is designed to make incremental extensions straightforward.

## Summary

Syntax Engine is a lightweight, extensible Markdown parser that demonstrates a clear, readable implementation of Markdown-to-HTML conversion in Python. With a modular rule system, CLI usage, and conformance testing, it provides a solid base for both learning and extending Markdown processing capabilities.
