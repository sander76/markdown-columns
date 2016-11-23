import markdown

from md_columns import md_columns

input1 = """%% %1 %2 %9
| ---------------- | ---- | ------- |
| test             | test | testing |"""

output1 = """<div class="row instruction">
<div class="col-sm-1">
<p>test</p>
</div>
<div class="col-sm-2">
<p>test</p>
</div>
<div class="col-sm-9">
<p>testing</p>
</div>
</div>"""

input2 = """%% %1 %2 %9 another instruction
| ---------------- | ---- | ------- |
| test             | test | testing |"""

output2 = """<div class="row another instruction">
<div class="col-sm-1">
<p>test</p>
</div>
<div class="col-sm-2">
<p>test</p>
</div>
<div class="col-sm-9">
<p>testing</p>
</div>
</div>"""

input3 = """%% %1 %2 %10
| ---------------- | ---- | ------- |
| cell 1             | test | testing |
| ++ **cell 1 line 2**   | test | testing |
| cell 2 | test | testing |"""

output3 = """<div class="row instruction">
<div class="col-sm-1">
<p>cell 1</p>
<p><strong>cell 1 line 2</strong></p>
</div>
<div class="col-sm-2">
<p>test</p>
<p>test</p>
</div>
<div class="col-sm-10">
<p>testing</p>
<p>testing</p>
</div>
</div>
<div class="row instruction">
<div class="col-sm-1">
<p>cell 2</p>
</div>
<div class="col-sm-2">
<p>test</p>
</div>
<div class="col-sm-10">
<p>testing</p>
</div>
</div>"""

md = markdown.Markdown(extensions=['md_columns.md_columns', 'three_columns', 'markdown.extensions.def_list'])

md1=markdown.Markdown(extensions=['md_columns.md_columns','markdown.extensions.tables','markdown.extensions.attr_list'])

input4="""|   |   |
| ---- | ---- |
| test{: .admonition} | test |

%% %3 %3
| ---- | ---- |
| _test_ | test |
| ++ test{: .admonition} | test |"""

input5="""%% %3 %3
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

doc_output = """<div class="row instruction">
<div class="col-sm-7">
<p>This instruction will make use of the following buttons on the Remote:</p>
</div>
<div class="col-sm-5">
<p><img alt="Adding a remote" src="/imgs/remote_add_to_group.svg" /></p>
</div>
</div>
<div class="row instruction">
<div class="col-sm-1">
<p>1</p>
</div>
<div class="col-sm-6">
<p><strong>Press &amp;icon-pv-stop; <code>stop</code> for 6 seconds.</strong></p>
<p><em>(Keep pressing until the remote lights start blinking.)</em></p>
</div>
</div>
<div class="row instruction">
<div class="col-sm-1">
<p>2</p>
</div>
<div class="col-sm-6">
<p><strong>Press &amp;icon-pv-one; <code>group1</code>.</strong></p>
<p><em>(This will activate the group 1 on the remote.)</em></p>
</div>
</div>
<div class="row instruction">
<div class="col-sm-1">
<p>3</p>
</div>
<div class="col-sm-6">
<p><strong>Press and hold the <code>shade button</code>.</strong></p>
</div>
<div class="col-sm-5">
<p><img alt="programming buttons" src="/imgs/duette.png" /></p>
</div>
</div>
<div class="row instruction">
<div class="col-sm-1">
<p>4</p>
</div>
<div class="col-sm-6">
<p><strong>Press the &amp;icon-pv-open; <code>open</code> button</strong></p>
<p><em>(You will see the shade move up and down shortly.)</em></p>
</div>
</div>
<div class="row instruction">
<div class="col-sm-1">
<p>5</p>
</div>
<div class="col-sm-6">
<p><strong>Release the <code>shade button</code>.</strong></p>
</div>
</div>
<div class="row instruction">
<div class="col-sm-1">
<p>6</p>
</div>
<div class="col-sm-6">
<p>If your remote is still flashing <strong>Press <code>stop</code> for 6 seconds.</strong></p>
<p><em>(Keep pressing until the flashing stops.)</em></p>
</div>
</div>"""

doc1_output="""<blockquote>
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


def test_block4():
    txt = md.convert(get_doc1())
    print(txt)
    assert txt==doc1_output

def test_block5():
    txt=md.convert(get_doc2())
    print(txt)
    assert True

def test_block6():
    txt=md1.convert(input4)
    print(txt)
    assert True

def test_block7():
    txt=md1.convert(input5)
    print(txt)
    assert True