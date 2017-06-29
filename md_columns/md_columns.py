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


class FlexBoxColumns(BlockProcessor):
    """ Process Definition Lists. """

    def __init__(self, parser, config):
        BlockProcessor.__init__(self, parser)
        self.set_defaults()

        self.row_class = config['row_class']
        self.cell_width_template = config["cell_width_class_template"]
        # self.instruction_class = config["instruction_class"]

    RE = re.compile(r'%%([\s%\d{1,2}]+)(.*)')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def set_defaults(self):
        self.table_class = "instruction"
        self.widths = None

    def _run(self, lines):
        self.tables = []

        for ln in lines:
            if ln.startswith("%%"):
                self.get_col_widths(ln)
            elif ln.startswith('| -') or ln.startswith('|-'):
                pass

            elif ln.startswith('| ++') or ln.startswith('|++'):
                _col = self.get_columns(ln)
                table['rows'].append(_col)
            elif ln.startswith('| +=') or ln.startswith('|+='):
                _col = self.get_columns(ln)
                FlexBoxColumns._merge_rows(table.get('rows')[-1], _col)
            else:
                _col = self.get_columns(ln)
                table = {'rows': [_col], 'widths': self.widths}
                self.tables.append(table)

    @staticmethod
    def _merge_rows(row1, row2):
        for idx, cols in enumerate(zip(row1, row2)):
            row1[idx] = (' '.join(cols)).strip()

    def process_rows(self, parent):
        for table in self.tables:
            fl = etree.SubElement(parent, "div")
            fl.set('class', self.row_class)
            # for row in table['rows']:
            for cell, width in zip(zip(*table['rows']), table['widths']):
                # cell = [cl for cl in cell if cl]
                self.create_cell_div(fl, list(cell), width)

    def create_cell_div(self, parent, content, width):
        cell = etree.SubElement(parent, "div")
        cell.set('class', self.cell_width_template.format(width))
        self.parser.parseBlocks(cell, content)

    def run(self, parent, blocks):
        parent = etree.SubElement(parent, "div")
        raw_block = blocks.pop(0)
        raw_block = raw_block.lstrip()
        # parent = create_container(parent)
        lines = raw_block.split('\n')
        self._run(lines)
        self.process_rows(parent)
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

    def get_columns(self, line):
        columns = [ln.strip(' +=') for ln in line.split('|')][1:-1]
        return columns


class DefFlexBloxColumnsExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'row_class': ['row',
                          'the class name of the container'],
            'cell_width_class_template': ['col-sm-{}',
                                          'the template to set the cell width']}

        super(DefFlexBloxColumnsExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of DefListProcessor to BlockParser. """
        md.parser.blockprocessors.add('defflexcolumn',
                                      FlexBoxColumns(md.parser,
                                                     self.getConfigs()),
                                      '_begin')


def makeExtension(*args, **kwargs):
    return DefFlexBloxColumnsExtension(*args, **kwargs)
