"""Python markdown extension for adding css column layout.
"""
import logging
import re
from itertools import zip_longest
from typing import Sequence, List

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.util import etree

RE = re.compile(r'%%([\s%\d{1,2}]+)(.*)')

RE_ATTR = re.compile(r'{:\s[^}]*}')

ATTR_ROW_CONTENT = 'row_content'
ATTR_ROW_CLASS = 'css'

CLASS_NO_FLOW = 'noflow'

CONFIG_CELL_WIDTH_CLASS_TEMPLATE = 'cell_width_class_template'
CONFIG_CELL_NOFLOW_WIDTH_CLASS_TEMPLATE = 'cell_noflow_width_class_template'
DEFAULT_CELL_WIDTH_CLASS_TEMPLATE = 'col-sm-{}'
NOFLOW_CELL_WIDTH_CLASS_TEMPLATE = 'col-xs-{}'

LOGGER = logging.getLogger(__name__)


# todo: add the option to add attribute list: {: .testclass}

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


class Row:
    def __init__(self, cell_data: Sequence, cell_widths: Sequence):
        self.rows = []
        self.add_data(cell_data)
        self.merged_rows = None
        self.widths = cell_widths
        self.css = ''

    def merge_rows(self):
        LOGGER.debug("merging a total of {} rows".format(len(self.rows)))
        self.merged_rows = zip_longest(*self.rows, fillvalue='')

    def add_data(self, data):
        self.rows.append(data)


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

    cell_width_template = None
    noflow_cell_width_template = None

    def __init__(self, raw_block):
        self.rows = []
        self._lines = raw_block.lstrip().split('\n')
        # temporary storage of column widths which are processed during the
        # lines interpretation.
        self.widths = None
        self._table_class = 'instruction'
        self._table_rows = []
        # self.cell_width_template = CONFIG_CELL_WIDTH_CLASS_TEMPLATE
        # self.cell_width_template = cell_width_template
        # self.no_flow_cell_width_template = no_flow_cell_width_template

    @property
    def table_class(self):
        return self._table_class

    @property
    def table_rows(self) -> List[Row]:
        return self._table_rows

    def run(self):
        """Processes the lines list line by line."""
        row = None
        for ln in self._lines:
            ln = ln.strip()
            if ln.startswith("%%"):
                self._get_col_widths_and_table_class(ln)
            elif ln.startswith('| --') or ln.startswith('|--'):
                pass
            elif ln.startswith('| ++') or ln.startswith('|++'):
                # append to a current row
                LOGGER.debug("found ++")
                _col, _ccs_class = get_columns(ln)
                LOGGER.debug(f"found {_col}")
                row.add_data(_col)
                row.css = get_class(_ccs_class)
            elif ln == '':
                pass
            else:
                # Create a new row.
                try:
                    LOGGER.debug(
                        "Merging the previous row before creating a new one.")
                    self._table_rows[-1].merge_rows()
                except IndexError:
                    LOGGER.debug("No previous row found.")
                _col, _css_class = get_columns(ln)
                row = Row(_col, self.widths)
                row.css = get_class(_css_class)
                self._table_rows.append(row)
        if row:
            LOGGER.debug("merging the last row in the list.")
            row.merge_rows()
        LOGGER.debug("found {} number of rows".format(len(self._table_rows)))

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
            self._get_cell_width_template()

    def _get_cell_width_template(self):
        if CLASS_NO_FLOW in self._table_class:
            # overrides the default cell width template.
            self.cell_width_template = self.noflow_cell_width_template


class CssColumns(BlockProcessor):
    """ Process Definition Lists. """

    def __init__(self, parser, config):
        BlockProcessor.__init__(self, parser)
        self.row_class = config['row_class']
        Columns.noflow_cell_width_template = config[
            CONFIG_CELL_NOFLOW_WIDTH_CLASS_TEMPLATE]
        Columns.cell_width_template = config[
            CONFIG_CELL_WIDTH_CLASS_TEMPLATE]

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
        for _row in columns.table_rows:
            fl = etree.SubElement(parent, "div")
            _css_class = self.row_class
            if _row.css is not None:
                _css_class = ' '.join((_css_class, _row.css))
            fl.set('class', _css_class)
            for cell, width in zip(_row.merged_rows,
                                   _row.widths):
                self.create_cell_div(
                    fl, list(cell), width, columns.cell_width_template)

    def create_cell_div(self, parent, content, width, width_template):
        cell = etree.SubElement(parent, "div")
        cell.set('class', width_template.format(width))
        self.parser.parseBlocks(cell, content)


class CssColumnsExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'row_class':
                ['row', 'the class name of the container'],
            CONFIG_CELL_WIDTH_CLASS_TEMPLATE:
                [DEFAULT_CELL_WIDTH_CLASS_TEMPLATE,
                 'the template to set the cell width'],
            CONFIG_CELL_NOFLOW_WIDTH_CLASS_TEMPLATE:
                [NOFLOW_CELL_WIDTH_CLASS_TEMPLATE,
                 'Cell width when "noflow" class is added to the table class.']
        }

        super(CssColumnsExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of DefListProcessor to BlockParser. """
        md.parser.blockprocessors.add('defflexcolumn',
                                      CssColumns(md.parser,
                                                 self.getConfigs()),
                                      '_begin')


def makeExtension(*args, **kwargs):
    return CssColumnsExtension(*args, **kwargs)
