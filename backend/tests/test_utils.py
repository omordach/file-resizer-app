import os
import pytest
from app.utils import process_file
from io import BytesIO

class DummyFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.file = BytesIO(content)

@pytest.mark.parametrize("file_type,width,height,quality", [
    ("Image", 100, 100, None),
    ("PDF", None, None, "ebook"),
])
def test_process_file_creates_output(file_type, width, height, quality):
    # Prepare dummy file content
    dummy_content = b"Test content for file"
    dummy_filename = "testfile.jpg" if file_type == "Image" else "testfile.pdf"
    dummy_file = DummyFile(dummy_filename, dummy_content)

    # Process the file
    output_path = process_file(dummy_file, file_type, width, height, quality)

    # Assert output path is not None and file exists
    assert output_path is not None
    assert os.path.exists(output_path)

    # Clean up the generated file
    os.remove(output_path)
