import argparse
import sys
import json
import unittest

from parser import parse

def convert_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    body = parse(content)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Converted Markdown</title>
</head>
<body>
{body}
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_doc)
    print(f"Successfully converted {input_path} to {output_path}")

def run_conformance(spec_path, verbose):
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            specs = json.load(f)
    except Exception as e:
        print(f"Error loading conformance spec: {e}")
        return
        
    passed = 0
    total = len(specs)
    failed_specs = []
    
    for spec in specs:
        md = spec.get("markdown", "")
        expected = spec.get("html", "")
        example_id = spec.get("example", "unknown")
        
        actual = parse(md)
        if actual.strip() == expected.strip():
            passed += 1
        else:
            failed_specs.append((example_id, expected, actual))
            
    print(f"Conformance Report: Passed {passed}/{total} specs.")
    
    if verbose and failed_specs:
        print("\n--- Failed Specs Details ---")
        for ex_id, expected, actual in failed_specs:
            print(f"Example ID: {ex_id}")
            print("Expected:")
            print(repr(expected))
            print("Actual:")
            print(repr(actual))
            print("-" * 30)

def main():
    parser = argparse.ArgumentParser(description="Markdown-to-HTML Syntax Engine")
    parser.add_argument("input_file", help="Input Markdown file (or JSON spec file if --conformance)")
    parser.add_argument("-o", "--output", default="output.html", help="Output HTML file")
    parser.add_argument("--conformance", action="store_true", help="Run conformance tests using the input JSON spec file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output (used with --conformance)")
    
    args = parser.parse_args()
    
    if args.conformance:
        run_conformance(args.input_file, args.verbose)
    else:
        convert_file(args.input_file, args.output)

if __name__ == '__main__':
    main()