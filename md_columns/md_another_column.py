"""


** %1 %2 %9
*************************
- row 1
- this is column 2
  Line two on column 2
- This is column3
  Including a second line.
**************************
* test
* this is column 2
  Line two on column 2
* This is column3
  Including a second line.
**************************

"""
from markdown.util import etree

from markdown.blockprocessors import BlockProcessor
import re

from markdown.extensions import Extension

COL_CHAR1 = '* '
COL_CHAR2 = '- '


def create_container(parent):
    container = etree.SubElement(parent, "div")
    container.set('class', 'container')
    return container


class Row:
    def __init__(self, widths, parser):
        self.parser = parser
        self.widths = widths
        self.columns = []

    def create_row(self, parent):
        if self.columns:
            fl = etree.SubElement(parent, "div")
            fl.set('class', 'row')
            for column, width in zip(self.columns, self.widths):
                cell = etree.SubElement(fl, "div")
                cell.set('class', 'col-sm-{}'.format(width))
                self.parser.parseBlocks(cell, column.content)


class Column:
    @staticmethod
    def _remove_indent(line):
        if line.startswith('  '):
            line = line.lstrip('  ')
        return line

    def __init__(self, line):
        self._content = [self._checkline(line)]

    @property
    def content(self):
        return self._content

    def __iter__(self):
        for itm in self._content:
            yield itm

    def _checkline(self, line):
        line = line.lstrip(COL_CHAR1)
        line = line.lstrip(COL_CHAR2)
        return line

    def append(self, line):
        self._content.append(Column._remove_indent(line))


class ColumnsParserAlternative(BlockProcessor):
    """ Process Definition Lists. """

    def __init__(self, parser):
        BlockProcessor.__init__(self, parser)
        self.set_defaults()

    RE = re.compile(r'\*\*([\s%\d{1,2}]+)(.*)')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def set_defaults(self):
        self.table_class = "instruction"
        self.widths = None

    def _parse_lines(self, lines):
        rows = []
        for ln in lines:
            if ln.startswith("***"):
                rows.append(Row(self.widths,self.parser))
            elif ln.startswith("**"):
                self.get_col_widths(ln)
            elif ln.startswith(COL_CHAR1) or ln.startswith(COL_CHAR2):
                rows[-1].columns.append(Column(ln))
            else:
                rows[-1].columns[-1].append(ln)
        return rows

    def run(self, parent, blocks):
        parent = etree.SubElement(parent, "div")
        raw_block = blocks.pop(0)
        raw_block = raw_block.lstrip()
        # parent = create_container(parent)
        lines = raw_block.split('\n')
        rows = self._parse_lines(lines)
        for row in rows:
            row.create_row(parent)
        parent.set('class', self.table_class)
        self.set_defaults()

    def get_col_widths(self, line):
        m = self.RE.match(line)
        line = m.group(1)
        line = line.replace('%', '')
        self.widths = line.split()
        _cls = (m.group(2)).strip()
        if _cls == "":
            pass
        else:
            self.table_class = m.group(2)


class DefColumnsParserAlternativeExtension(Extension):
    """ Add definition lists to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of DefListProcessor to BlockParser. """
        md.parser.blockprocessors.add('def_columns_parser_alt',
                                      ColumnsParserAlternative(md.parser),
                                      '_begin')


def makeExtension(*args, **kwargs):
    return DefColumnsParserAlternativeExtension(*args, **kwargs)
