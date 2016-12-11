import markdown

from md_columns import md_columns
from test.output import output1, output2, output3, output8, doc_output

input1 = """%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |"""

input2 = """%% %1 %2 %9 another
| ---------------- | ---- | ------- |
| test             | test | testing |"""

input3 = """%% %1 %2 %10
| ---------------- | ---- | ------- |
| cell 1             | test | testing |
| ++ **cell 1 line 2**   | test | testing |
| cell 2 | test | testing |"""

md = markdown.Markdown(extensions=['md_columns.md_columns', 'three_columns', 'markdown.extensions.def_list'])

md1 = markdown.Markdown(
    extensions=['md_columns.md_columns', 'markdown.extensions.tables', 'markdown.extensions.attr_list'])

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


# def test_block6():
#     txt = md1.convert(input4)
#     print(txt)
#     assert False
#
#
# def test_block7():
#     txt = md1.convert(input5)
#     print(txt)
#     assert False



input8 = """%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |"""
def test_block8():
    ext = md_columns.DefFlexBloxColumnsExtension(row_class='row2',cell_width_class_template='col-sm-{} cell')
    md2 = markdown.Markdown(extensions=[ext])
    txt = md2.convert(input8)
    assert txt == output8