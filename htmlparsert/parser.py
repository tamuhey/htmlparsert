from collections import defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import DefaultDict, List, Optional, Tuple, Union


@dataclass
class TextNode:
    start_pos: Tuple[int, int]  # (lineno, column)
    text: str


def convert_pos(
    lineno_cols: List[Tuple[int, int]], text: str, is_sorted: bool = False
) -> List[int]:
    """Convert (lineno, column) position representation to text index."""
    if len(lineno_cols) == 0:
        return []
    if not is_sorted:
        lineno_cols = sorted(lineno_cols)
    ret = []
    curpos = 0
    j = 0
    for i, line in enumerate(text.split("\n"), start=1):
        if i == lineno_cols[j][0]:
            ret.append(lineno_cols[j][1] + curpos)
            j += 1
            if j == len(lineno_cols):
                break
        curpos += len(line) + 1
    return ret


@dataclass
class Node:
    tag: str
    parent: Optional["Node"]
    childlen: List[Union["Node", TextNode]] = field(default_factory=list)
    attrs: DefaultDict[str, List[str]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def extract_text_nodes(self) -> List[TextNode]:
        ret = []
        for node in self.childlen:
            if isinstance(node, Node):
                ret.extend(node.extract_text_nodes())
            elif isinstance(node, TextNode):
                ret.append(node)
        return ret

    def query(self, key: str, value: Optional[str] = None) -> Optional["Node"]:
        if key in self.attrs and (value is not None or value in self.attrs[key]):
            return self
        for node in self.childlen:
            if isinstance(node, Node):
                if ret := node.query(key, value):
                    return ret


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node(tag="", parent=None)
        self.cur = self.root

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        node = Node(tag=tag, parent=self.cur)
        for k, v in attrs:
            l = node.attrs[k]
            if v:
                l.append(v)
        self.cur.childlen.append(node)
        self.cur = node

    def handle_endtag(self, tag: str) -> None:
        assert tag == self.cur.tag
        self.cur = self.cur.parent

    def handle_data(self, data):
        textnode = TextNode(self.getpos(), data)
        self.cur.childlen.append(textnode)


def parse(html: str) -> Node:
    """Parse html string to Node."""
    parser = Parser()
    parser.feed(html)
    return parser.root


if __name__ == "__main__":
    import pprint

    pprint.pprint(parse(input()))
