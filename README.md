# A lightweight, no dependency HTML parser for text processing

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
parse(html)
```
