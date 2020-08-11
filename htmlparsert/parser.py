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
    lineno, col = lineno_cols[j]
    for i, line in enumerate(text.split("\n"), start=1):
        while i == lineno:
            ret.append(col + curpos)
            j += 1
            if j == len(lineno_cols):
                break
            lineno, col = lineno_cols[j]
        if j == len(lineno_cols):
            break
        curpos += len(line) + 1
    assert len(ret) == len(lineno_cols)
    return ret


@dataclass
class Node:
    tag: str
    parent: Optional["Node"]
    childlen: List[Union["Node", TextNode]] = field(default_factory=list)
    attrs: DefaultDict[str, List[str]] = field(
        default_factory=lambda: defaultdict(list)
    )

    @property
    def text_nodes(self) -> List[TextNode]:
        """Extract TextNode from self
        
        Example:
            >>> from htmlparsert import parse
            >>> node = parse('''<a>foo <b> bar </b></a>''')
            >>> node.text_nodes
            [TextNode(start_pos=(1, 3), text='foo '), TextNode(start_pos=(1, 10), text=' bar ')]
        """
        ret = []
        for node in self.childlen:
            if isinstance(node, Node):
                ret.extend(node.text_nodes)
            elif isinstance(node, TextNode):
                ret.append(node)
        return ret

    def query(self, key: str, value: Optional[str] = None) -> Optional["Node"]:
        if key in self.attrs and (value is None or value in self.attrs[key]):
            return self
        for node in self.childlen:
            if isinstance(node, Node):
                if ret := node.query(key, value):
                    return ret

    def get_element_by_tagname(self, tagname: str) -> Optional["Node"]:
        if tagname == self.tag:
            return self
        for node in self.childlen:
            if isinstance(node, Node):
                if ret := node.get_element_by_tagname(tagname):
                    return ret


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node(tag="", parent=None)
        self.cur = self.root

    def handle_startendtag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        pass

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        node = Node(tag=tag, parent=self.cur)
        for k, v in attrs:
            l = node.attrs[k]
            if v:
                l.extend(v.split())
        self.cur.childlen.append(node)
        self.cur = node

    def handle_endtag(self, tag: str) -> None:
        while tag != self.cur.tag:
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
