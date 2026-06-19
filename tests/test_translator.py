from unittest.mock import Mock, patch
from translator import translation_to_english


@patch("translator.OpenAI")
def test_translation_saved(mock_openai, tmp_path):

    mock_response = Mock()
    mock_response.output_text = "Namaste"

    mock_client = Mock()
    mock_client.responses.create.return_value = mock_response

    mock_openai.return_value = mock_client

    output_file = tmp_path / "translated.md"

    result = translation_to_english(
        markdown_text="नमस्ते",
        output_file=str(output_file)
    )

    assert result == "Namaste"
    assert output_file.exists()