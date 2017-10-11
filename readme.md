# Markdown columns

Python markdown plugin to create a column layout inspired by bootstrap.


input:

```markdown
%% %1 %2 %9
| ---------------------- | ----------------- | ------- |
| cell 1                 | cell 2            | cell 3  |
| ++ **cell 1 line 2**   | cell 2 line 2     | c3l2    |
| cell 4                 | cell 5            | cell 6  |{: .extra_row_class}
```

output:

```html
<div class="instruction">
    <div class="row">
        <div class="col-sm-1">
            <p>cell 1</p>
            <p><strong>cell 1 line 2</strong></p>
        </div>
        <div class="col-sm-2">
            <p>cell 2</p>
            <p>cell 2 line 2</p>
        </div>
        <div class="col-sm-9">
            <p>cell 3</p>
            <p>c3l2</p>
        </div>
    </div>
    <div class="row extra_row_class">
        <div class="col-sm-1">
            <p>cell 4</p>
        </div>
        <div class="col-sm-2">
            <p>cell 5</p>
        </div>
        <div class="col-sm-9">
            <p>cell 6</p>
        </div>
    </div>
</div>
```

- First line should start with `%%` column widths are defined by following it with `%<width>`.
    So `%% %1 %2 %9` will create columns with a width of 1, 2 and 9.
- By default the table class is `instruction`. `%% %1 %2 %9 table` will replaces it
    with `table` class.
- The second line `| --- | --- |` is ignored.
- `++` adds this line to the previous row definition as a new block.
- `extra_row_class` adds an extra class to the row definition.


## configuration

Adding the extension.

```python
from md_columns import CssColumnsExtension

markdown.Markdown(extensions=[CssColumnsExtension()])
```

Optional arguments to configure the output:

- **row_class**: Default is ```row```
- **cell_width_class_template**: Default is ```col-sm-{}```

