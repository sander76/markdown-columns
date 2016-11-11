import markdown

from md_columns import md_columns


input1 = """%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |
| test             | test | testing |
| dfg dsfg df test | test | testing |"""

output1 = """<div class="mk-container">
<div class="mk-row instruction">
<div class="mk-col-sm-1">test</div>
<div class="mk-col-sm-2">test</div>
<div class="mk-col-sm-9">testing</div>
</div>
<div class="mk-row instruction">
<div class="mk-col-sm-1">test</div>
<div class="mk-col-sm-2">test</div>
<div class="mk-col-sm-9">testing</div>
</div>
<div class="mk-row instruction">
<div class="mk-col-sm-1">dfg dsfg df test</div>
<div class="mk-col-sm-2">test</div>
<div class="mk-col-sm-9">testing</div>
</div>
</div>"""

input2 = """%% %1 %2 %9 another instruction
| ---------------- | ---- | ------- |
| test             | test | testing |"""

output2 = """<div class="mk-container">
<div class="mk-row another instruction">
<div class="mk-col-sm-1">test</div>
<div class="mk-col-sm-2">test</div>
<div class="mk-col-sm-9">testing</div>
</div>
</div>"""

input3="""%% %1 %2 %10
| ---------------- | ---- | ------- |
| cell 1             | test | testing |
| ++ **cell 1 line 2**   | test | testing |
| cell 2 | test | testing |
| **cell 3**             | test | testing |
| ++ cell 3 line 2             | test | testing |"""

output3="""<div class="mk-container">
<div class="mk-row instruction">
<div class="mk-col-sm-1">cell 1<br><strong>cell 1 line 2</strong></div>
<div class="mk-col-sm-2">test<br>test</div>
<div class="mk-col-sm-10">testing<br>testing</div>
</div>
<div class="mk-row instruction">
<div class="mk-col-sm-1">cell 2</div>
<div class="mk-col-sm-2">test</div>
<div class="mk-col-sm-10">testing</div>
</div>
<div class="mk-row instruction">
<div class="mk-col-sm-1"><strong>cell 3</strong><br>cell 3 line 2</div>
<div class="mk-col-sm-2">test<br>test</div>
<div class="mk-col-sm-10">testing<br>testing</div>
</div>
</div>"""

md = markdown.Markdown(extensions=['md_columns.md_columns','three_columns'])

def get_doc():
    with open("test_columns.md",'r') as fl:
        cols = fl.read()
    return cols

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
    assert txt==output3

def test_block3():
    txt = md.convert(get_doc())
    print(txt)
    assert True