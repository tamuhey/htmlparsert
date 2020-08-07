import pytest
from htmlparsert.parser import Node, convert_pos, parse


def print_nodes(node: Node, indent=""):
    print(indent + f"node {node.tag} {node.attrs}")
    nextindent = indent + " " * 4
    for c in node.childlen:
        if isinstance(c, Node):
            print_nodes(c, indent=nextindent)
        else:
            print(nextindent + c.text)


@pytest.mark.parametrize(
    "html,attr,expected",
    [
        ("  <foo>bar</foo>", None, "  bar"),
        ("<foo>wow<a href='foo'>111</a></foo>", None, "wow111"),
        ("<a> foo\n\n bar<b>111</b>\nfoooo</a>", None, " foo\n\n bar111\nfoooo"),
        ("<a>woo</a><b id='foo'>wowowo</b>", ("id", "foo"), "wowowo"),
        (
            "<a>woo<b class='foo bar baz'>fff</b></a><b id='foo'>wowowo</b>",
            ("class", "foo"),
            "fff",
        ),
        ("<a></a>", None, ""),
        ("", None, ""),
    ],
)
def test_extract_string(html, expected, attr):
    node = parse(html)
    if attr:
        node = node.query(*attr)
    if node is None:
        print_nodes(parse(html))
        raise ValueError("internall error")
    tnodes = node.extract_text_nodes()
    assert "".join(x.text for x in tnodes) == expected, tnodes
    for pos, t in zip(convert_pos([t.start_pos for t in tnodes], html), tnodes):
        assert html[pos : pos + len(t.text)] == t.text
