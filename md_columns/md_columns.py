"""


%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |
| test             | test | testing |
| dfg dsfg df test | test | testing |

"""
from markdown.util import etree

from markdown.blockprocessors import BlockProcessor
import re

from markdown.extensions import Extension


def create_cell_div(parent, content, width):
    cell = etree.SubElement(parent, "div")
    # cell.set('style', "flex:{}".format(width))
    cell.set('class', 'mk-col-sm-{}'.format(width))
    cell.text = content


def create_container(parent):
    container = etree.SubElement(parent, "div")
    container.set('class', 'mk-container')
    return container


class FlexBoxColumns(BlockProcessor):
    """ Process Definition Lists. """

    def __init__(self, parser):
        BlockProcessor.__init__(self, parser)
        self.set_defaults()

    RE = re.compile(r'%%([\s%\d{1,2}]+)(.*)')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def set_defaults(self):
        self.table_class = "instruction"
        self.widths = None

    def _run(self, lines):
        self.rows = []
        row = []
        for ln in lines:
            if ln.startswith("%%"):
                self.get_col_widths(ln)
            elif ln.startswith('| -') or ln.startswith('|-'):
                pass
            elif ln.startswith('| ++') or ln.startswith('|++'):
                row['row'].append(ln)
            else:
                row = {'row': [ln], 'widths': self.widths}
                self.rows.append(row)

    def process_rows(self, parent):
        for row in self.rows:
            fl = etree.SubElement(parent, "div")
            fl.set('class', 'mk-row {}'.format(self.table_class))

            zp = zip(*(self.process_row(rw) for rw in row['row']))
            lst = list(zp)
            for cell, width in zip(lst, row['widths']):
                cell = "<br>".join((cl for cl in cell if cl))
                create_cell_div(fl, cell, width)

    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        # parent = create_container(parent)
        lines = raw_block.split('\n')
        self._run(lines)
        self.process_rows(parent)
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

    def process_row(self, line):
        line = line.strip('| ')
        columns = (ln.strip(' +') for ln in line.split('|'))
        return columns


class DefFlexBloxColumnsExtension(Extension):
    """ Add definition lists to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of DefListProcessor to BlockParser. """
        md.parser.blockprocessors.add('defflexcolumn',
                                      FlexBoxColumns(md.parser),
                                      '>indent')


def makeExtension(*args, **kwargs):
    return DefFlexBloxColumnsExtension(*args, **kwargs)
