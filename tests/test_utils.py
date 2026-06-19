from unittest.mock import patch
from utils import save_translation_docx


@patch("utils.pypandoc.convert_text")
def test_docx_conversion(mock_convert):

    save_translation_docx(
        "# Heading",
        "test.docx"
    )

    mock_convert.assert_called_once()

