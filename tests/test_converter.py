from converter import clean_markdown


def test_remove_image_references():
    text = """
    Hello

    ![](image.jpg)

    World
    """

    result = clean_markdown(text)

    assert "![]" not in result
    assert "Hello" in result
    assert "World" in result


def test_collapse_blank_lines():
    text = "A\n\n\n\nB"

    result = clean_markdown(text)

    assert result == "A\n\nB"


def test_multiple_images():
    text = """
    ![](a.jpg)

    Text

    ![](b.png)
    """

    result = clean_markdown(text)

    assert "a.jpg" not in result
    assert "b.png" not in result


