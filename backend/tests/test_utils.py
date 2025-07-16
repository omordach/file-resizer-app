import os
import pytest
from app.utils import process_file

TEST_DIR = os.path.dirname(__file__)

class DummyFile:
    def __init__(self, filepath):
        self.filename = os.path.basename(filepath)
        self.file = open(filepath, "rb")

@pytest.mark.parametrize("file_type,test_file_path,width,height,quality", [
    ("Image", os.path.join(TEST_DIR, "assets/test-image.jpg"), 100, 100, None),
    ("PDF", os.path.join(TEST_DIR, "assets/test-file.pdf"), None, None, "ebook"),
])
def test_process_file_creates_output(file_type, test_file_path, width, height, quality):
    # Validate that the test file exists
    assert os.path.exists(test_file_path), f"Test file not found: {test_file_path}"

    # Prepare the dummy file from the actual file content
    dummy_file = DummyFile(test_file_path)

    # Process the file using your application logic
    output_path = process_file(dummy_file, file_type, width, height, quality)

    # Assert output file was created successfully
    assert output_path is not None
    assert os.path.exists(output_path)

    # Clean up generated file
    os.remove(output_path)
