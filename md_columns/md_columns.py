"""Python markdown extension for adding css column layout.
"""
import re

from markdown.util import etree
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension

RE = re.compile(r'%%([\s%\d{1,2}]+)(.*)')

ATTR_ROW_CONTENT = 'row_content'
ATTR_ROW_CLASS = 'css'


def get_class(css_string: str):
    if css_string is None:
        return None
    else:
        css_string = css_string.strip('{: }').replace('.', '')
        return css_string


def get_columns(line: str):
    """Splits the line into columns and checks whether there is a class
    added."""
    _css_class = None
    if line.endswith('}'):
        _start = line.rfind('{')
        _css_class = line[_start:]
        line = line[0:_start]
    columns = [ln.lstrip('+ ').rstrip() for ln in line.split('|')][1:-1]
    return columns, _css_class


class Columns:
    """Columns class which populates a dict which in the end forms a table

    table_rows =
    [
        {'row_content' : [['text col1','text col2','text col3'],
                   ['text col1','text col2','text col3']
                ]
        'widths' : [3,4,5],
        'css' : 'css class'
        },

        {'row_content' : [['text col1','text col2','text col3'],
                   ['text col1','text col2','text col3']
                ]
        'widths' : [3,4,5],
        'css' : 'css class'
        }
    ]

    All col1 text is put in column1, All col2 text is put in column2
    """

    def __init__(self, raw_block):
        self.rows = []
        self._lines = raw_block.lstrip().split('\n')
        # temporary storage of column widths which are processed during the
        # lines interpretation.
        self.widths = None
        self._table_class = 'instruction'
        self.table_rows = []

    @property
    def table_class(self):
        return self._table_class

    def run(self):
        """Processes the lines list line for line."""

        for ln in self._lines:
            ln = ln.strip()
            if ln.startswith("%%"):
                self._get_col_widths_and_table_class(ln)
            elif ln.startswith('| -') or ln.startswith('|-'):
                pass
            elif ln.startswith('| ++') or ln.startswith('|++'):
                _col, _ccs_class = get_columns(ln)
                row[ATTR_ROW_CONTENT].append(_col)
            elif ln == '':
                pass
            else:
                _col, _css_class = get_columns(ln)
                row = {ATTR_ROW_CONTENT: [_col],
                         'widths': self.widths,
                       ATTR_ROW_CLASS: get_class(_css_class)}
                self.table_rows.append(row)

    def _get_col_widths_and_table_class(self, line):
        m = RE.match(line)
        line = m.group(1)
        line = line.replace('%', '')
        self.widths = line.split()
        _cls = (m.group(2)).strip()
        if _cls == "":
            pass
        else:
            self._table_class = m.group(2)


class CssColumns(BlockProcessor):
    """ Process Definition Lists. """

    def __init__(self, parser, config):
        BlockProcessor.__init__(self, parser)
        self.row_class = config['row_class']
        self.cell_width_template = config["cell_width_class_template"]

    def test(self, parent, block):
        """Checks whether a block is found which fits the regex expression"""
        return bool(RE.search(block))

    def run(self, parent, blocks):
        """main entry point for processing the block of markdown text."""
        parent = etree.SubElement(parent, "div")
        # Get the raw data block
        raw_block = blocks.pop(0)
        columns = Columns(raw_block)
        columns.run()
        self.process_rows(parent, columns)
        parent.set('class', columns.table_class)

    def process_rows(self, parent, columns: Columns):
        for table in columns.table_rows:
            fl = etree.SubElement(parent, "div")
            _css_class = self.row_class
            if table[ATTR_ROW_CLASS] is not None:
                _css_class = ' '.join((_css_class, table[ATTR_ROW_CLASS]))
            fl.set('class', _css_class)
            for cell, width in zip(zip(*table[ATTR_ROW_CONTENT]), table['widths']):
                self.create_cell_div(fl, list(cell), width)

    def create_cell_div(self, parent, content, width):
        cell = etree.SubElement(parent, "div")
        cell.set('class', self.cell_width_template.format(width))
        self.parser.parseBlocks(cell, content)


class CssColumnsExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'row_class':
                ['row', 'the class name of the container'],
            'cell_width_class_template':
                ['col-sm-{}', 'the template to set the cell width']}

        super(CssColumnsExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of DefListProcessor to BlockParser. """
        md.parser.blockprocessors.add('defflexcolumn',
                                      CssColumns(md.parser,
                                                 self.getConfigs()),
                                      '_begin')


def makeExtension(*args, **kwargs):
    return CssColumnsExtension(*args, **kwargs)
