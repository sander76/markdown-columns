import markdown

from test.output import output1, output2, output3, doc_output

input19 = '''** %1 %2 %9
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
**************************'''

input1 = """** %1 %2 %9
****
- test
- test
- testing"""

input2 = """** %1 %2 %9 another
****
- test
- test
- testing
****"""

input3 = """** %1 %2 %10
*************************
- cell 1
  **cell 1 line 2**
- test
  test
- testing
  testing
*************************
- cell 2
- test
- testing"""

md = markdown.Markdown(extensions=['md_columns.md_another_column'])


def test_block():
    txt = md.convert(input1)
    print(txt)
    assert txt == output1
    # assert txt == output1


def test_block2():
    txt = md.convert(input2)
    assert txt == output2


def test_block3():
    txt = md.convert(input3)
    print(txt)
    assert txt == output3


def get_doc():
    with open("test_columns_alt.md", 'r') as fl:
        cols = fl.read()
    return cols


def test_block4():
    txt = md.convert(get_doc())
    print(txt)
    assert txt == doc_output
