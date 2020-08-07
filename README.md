# A lightweight, no dependency HTML parser for text processing

This is useful to extract the character data and their offset from html.
(Other Python html libraries don't provide the offset data.)

## Usage

install: `pip install htmlparsert`

```python
from htmlparsert import parse
html = """
<html>

<body>
    <p>foo</p>
    <div><a>bar</a></div>
</body>

</html>
"""
node = parse(html)
```

`node` holds html tag nodes (`Node`) and text data (`TextNode`).
All text data have its offset in html.
