

output2 = """<div class="_column_container another">
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

output3 = """<div class="_column_container">
<div class="row">
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
<div class="row">
<div class="col-sm-1">
<p>cell 2</p>
</div>
<div class="col-sm-2">
<p>test</p>
</div>
<div class="col-sm-10">
<p>testing</p>
</div>
</div>
</div>"""

output6 = """<div class="instruction">
<div class="row">
<div class="col-sm-1">
<p>cell 1 <strong>cell 1 line 2</strong></p>
</div>
<div class="col-sm-2">
<p>test</p>
</div>
<div class="col-sm-10">
<p>testing</p>
</div>
</div>
<div class="row">
<div class="col-sm-1">
<p>cell 2</p>
</div>
<div class="col-sm-2">
<p>test</p>
</div>
<div class="col-sm-10">
<p>testing</p>
</div>
</div>
</div>"""

input7 = """%% %1 %2 %10
| ---------------- | ---- | ------- |
| cell 1           | test | testing |
| ++ **row1**      |      |         |
| += row1 attached |      |         |"""


output7 = """<div class="_column_container">
<div class="row">
<div class="col-sm-1">
<p>cell 1</p>
<p><strong>row1</strong> row1 attached</p>
</div>
<div class="col-sm-2">
<p>test</p>
</div>
<div class="col-sm-10">
<p>testing</p>
</div>
</div>
</div>"""


doc_output = """<div class="_column_container">
<div class="row">
<div class="col-sm-7">
<p>This instruction will make use of the following buttons on the Remote:</p>
</div>
<div class="col-sm-5">
<p><img alt="Adding a remote" src="/imgs/remote_add_to_group.svg" /></p>
</div>
</div>
<div class="row">
<div class="col-sm-1">
<p>1</p>
</div>
<div class="col-sm-6">
<p><strong>Press &amp;icon-pv-stop; <code>stop</code> for 6 seconds.</strong></p>
<p><em>(Keep pressing until the remote lights start blinking.)</em></p>
</div>
<div class="col-sm-5"></div>
</div>
<div class="row">
<div class="col-sm-1">
<p>2</p>
</div>
<div class="col-sm-6">
<p><strong>Press &amp;icon-pv-one; <code>group1</code>.</strong></p>
<p><em>(This will activate the group 1 on the remote.)</em></p>
</div>
<div class="col-sm-5"></div>
</div>
<div class="row">
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
<div class="row">
<div class="col-sm-1">
<p>4</p>
</div>
<div class="col-sm-6">
<p><strong>Press the &amp;icon-pv-open; <code>open</code> button</strong></p>
<p><em>(You will see the shade move up and down shortly.)</em></p>
</div>
<div class="col-sm-5"></div>
</div>
<div class="row">
<div class="col-sm-1">
<p>5</p>
</div>
<div class="col-sm-6">
<p><strong>Release the <code>shade button</code>.</strong></p>
</div>
<div class="col-sm-5"></div>
</div>
<div class="row">
<div class="col-sm-1">
<p>6</p>
</div>
<div class="col-sm-6">
<p>If your remote is still flashing <strong>Press <code>stop</code> for 6 seconds.</strong></p>
<p><em>(Keep pressing until the flashing stops.)</em></p>
</div>
<div class="col-sm-5"></div>
</div>
</div>"""

output8 = """<div class="_column_container">
<div class="row2">
<div class="col-1 cell">
<p>test</p>
</div>
<div class="col-2 cell">
<p>test</p>
</div>
<div class="col-9 cell">
<p>testing</p>
</div>
</div>
</div>"""

attribute_output1 = """<div class="_column_container another">
<div class="row">
<div class="col-sm-1">
<p class="test">test1</p>
</div>
<div class="col-sm-2">
<p>test2</p>
</div>
<div class="col-sm-9">
<p>test3</p>
</div>
</div>
</div>"""