import markdown
import pytest

from md_columns.md_columns import CssColumnsExtension

from test.output import output2, output3, output8, doc_output, \
    output6, output7

input2 = """%% %1 %2 %9 another
| ---------------- | ---- | ------- |
| test             | test | testing |"""

input3 = """
%% %1 %2 %10
| ---------------------- | ---- | ------- |
| cell 1                 | test | testing |
| ++ **cell 1 line 2**   | test | testing |
| cell 2                 | test | testing |"""

md = markdown.Markdown(
    extensions=[CssColumnsExtension(), 'markdown.extensions.def_list'])

md1 = markdown.Markdown(
    extensions=['md_columns.md_columns', 'markdown.extensions.tables',
                'markdown.extensions.attr_list'])

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

input7 = """%% %1 %2 %10
| ---------------- | ---- | ------- |
| cell 1             | test | testing |
| ++ **row1**   |  |  |
| += row1 attached |  |  |"""


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

input1 = """
%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |
"""

output1 = """<div class="instruction">
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

from md_columns.md_columns import Columns, get_columns, get_class, \
    CssColumnsExtension

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
    assert len(cols.tables) == 3


def test_block():
    txt = md.convert(input1)
    print(txt)
    assert txt == output1


def test_block1():
    txt = md.convert(input2)
    print(txt)
    assert txt == output2


def test_block2():
    txt = md.convert(input3)
    print(txt)
    assert txt == output3


def test_block3():
    txt = md.convert(get_doc())
    print(txt)
    assert txt == doc_output


# def test_block4():
#     txt = md.convert(get_doc1())
#     print(txt)
#     assert txt == doc1_output


def test_block5():
    txt = md.convert(get_doc2())
    print(txt)
    assert True


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
