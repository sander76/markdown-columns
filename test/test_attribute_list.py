import markdown
import pytest

from md_columns.md_columns import CssColumnsExtension
from test.output import attribute_output1


@pytest.fixture
def attr_parser():
    return markdown.Markdown(
        extensions=[CssColumnsExtension(), 'markdown.extensions.attr_list']
    )


attribute_list_input1 = """%% %1 %2 %9 another
| ---------------- | ---- | ------- |
| test1{: .test}          | test2 | test3 |"""




def test_attribute_list(attr_parser):
    txt = attr_parser.convert(attribute_list_input1)
    # txt = attr_parser.convert(tst)
    print(txt)
    assert txt == attribute_output1
