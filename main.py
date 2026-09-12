from parser import parse

def convert_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    body = parse(lines)

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

if __name__ == '__main__':
    convert_file('sample.md', 'output.html')