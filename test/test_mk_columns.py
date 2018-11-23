import logging

import markdown
import pytest

from md_columns.md_columns import CssColumnsExtension, Columns, get_columns, \
    get_class
from test.output import output2, output3, output8, doc_output, \
    attribute_output1, input7, output7

logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def parser():
    return markdown.Markdown(
        extensions=[CssColumnsExtension(), 'markdown.extensions.def_list'])


input2 = """%% %1 %2 %9 another
| ---------------- | ---- | ------- |
| test             | test | testing |"""

input3 = """
%% %1 %2 %10
| ---------------------- | ---- | ------- |
| cell 1                 | test | testing |
| ++ **cell 1 line 2**   | test | testing |
| cell 2                 | test | testing |"""

input4 = """|   |   |
| ---- | ---- |
| test{: .admonition} | test |

%% %3 %3
| ---- | ---- |
| _test_ | test |
| ++ test{: .admonition} | test |"""

input5 = """%% %3 %3
| ---- | ---- |
| a test{: .admonition} a | test |"""



def get_doc():
    with open("test_columns.md", 'r') as fl:
        cols = fl.read()
    return cols


def get_doc1():
    with open("test1_columns.md", 'r')as fl:
        cols = fl.read()
    return cols


def get_doc2():
    with open("test2_columns.md", 'r')as fl:
        cols = fl.read()
    return cols


doc1_output = """<blockquote>
<p>first block test</p>
</blockquote>
<div class="row instruction">
<div class="col-sm-1">
<p>1</p>
</div>
<div class="col-sm-6">
<p><strong>Press &amp;icon-pv-stop; <code>stop</code> for 6 seconds.</strong></p>
<blockquote>
<p>block test</p>
</blockquote>
</div>
</div>"""

output1 = """<div class="_column_container instruction">
<div class="row">
<div class="col-sm-1">
<p>test</p>
</div>
<div class="col-sm-2">
<p>test</p>
</div>
<div class="col-sm-9">
<p>testing</p>
</div>
</div>
</div>"""

input1 = """
%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |
"""

single_line_tests = """
%% %1 %2 %9
| -------------------- | ---- | ------- |
| testing              | adsf | asdf    |{: .test}
| ++ adding extra line | 123  | 123     |
"""


def test_get_column():
    cols = Columns(single_line_tests)
    assert cols._lines[0].startswith('%%')
    _cols, _css_class = get_columns(cols._lines[2])
    assert len(_cols) == 3
    assert get_class(_css_class) == 'test'
    _cols, _css_class = get_columns(cols._lines[3])
    assert len(_cols) == 3
    assert _cols[0] == 'adding extra line'
    assert get_class(_css_class) is None


bucket_tests = """
%% %1 %2 %9
| -------------------- | ---- | ------- |
| testing              | adsf | asdf    |
| ++ adding extra line | 123  | 123     |
| testing              | adsf | asdf    |

| testing              | adsf | asdf    |

"""


def test_buckets():
    cols = Columns(bucket_tests)
    cols.run()
    assert len(cols.table_rows) == 3


def test_block(parser):
    txt = parser.convert(input1)
    print(txt)
    assert txt == output1


def test_block1(parser):
    txt = parser.convert(input2)
    print(txt)
    assert txt == output2


def test_block2(parser):
    txt = parser.convert(input3)
    print(txt)
    assert txt == output3


def test_block3(parser):
    txt = parser.convert(get_doc())
    print(txt)
    assert txt == doc_output


def test_block5(parser):
    txt = parser.convert(get_doc2())
    print(txt)
    assert True

def test_input7(parser):
    txt = parser.convert(input7)
    assert txt == output7

input8 = """%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |"""


def test_class_names():
    ext = CssColumnsExtension(
        row_class='row2',
        cell_width_class_template='col-{} cell')
    md2 = markdown.Markdown(extensions=[ext])
    txt = md2.convert(input8)
    assert txt == output8


input_no_flow1 = """
%% %1 %2 %9 noflow
| ---------------- | ---- | ------- |
| test             | test | testing |
"""

output_no_flow1 = """<div class="_column_container instruction noflow">
<div class="row">
<div class="col-xs-1">
<p>test</p>
</div>
<div class="col-xs-2">
<p>test</p>
</div>
<div class="col-xs-9">
<p>testing</p>
</div>
</div>
</div>"""


def test_no_flow(parser):
    txt = parser.convert(input_no_flow1)
    assert txt == output_no_flow1



wrong_output1 = """<p>abc
%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |</p>"""

wrong_input1 = """
abc
%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |
"""


def test_error(parser):
    txt = parser.convert(wrong_input1)
    assert txt == wrong_output1


wrong_output2 = """<div>
<div>
    <div><strong>PROBLEM PARSING COLUMN LAYOUT</strong></div>
    %%
| ---------------- | ---- | ------- |
| test             | test | testing |
    <div><strong>END PROBLEM PARSING COLUMN LAYOUT</strong></div>
</div>
</div>"""

wrong_input2 = """
%%
| ---------------- | ---- | ------- |
| test             | test | testing |
"""


def test_error1(parser):
    txt = parser.convert(wrong_input2)
    assert txt == wrong_output2
