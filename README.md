# A lightweight, no dependency HTML parser for text processing

This is useful to extract the character data and their offset from html.
(Other Python html libraries don't provide the offset data.)

## Usage

install: `pip install htmlparsert`

```python
>>> from htmlparsert import parse
>>> node = parse('''<a>foo <b> bar </b></a>''')
>>> node.text_nodes
[TextNode(start_pos=(1, 3), text='foo '), TextNode(start_pos=(1, 10), text=' bar ')]
```

`node` holds html tag nodes (`Node`) and text data (`TextNode`).
`start_pos` of `TextNode` represents its offset in html as "(row number, column number)".
