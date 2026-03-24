import os
import pytest
from app.utils import process_file
import app.utils

class DummyFile:
    def __init__(self, content):
        self.filename = "dummy.jpg"
        class MockFile:
            def __init__(self, data):
                self.data = data
                self.pos = 0
            def read(self, size):
                chunk = self.data[self.pos:self.pos+size]
                self.pos += size
                return chunk
            def seek(self, pos):
                self.pos = pos
        self.file = MockFile(content)

def test_temp_file_deleted_on_size_limit():
    original_named_temp = app.utils.NamedTemporaryFile
    created_files = []

    def mock_named_temp(*args, **kwargs):
        f = original_named_temp(*args, **kwargs)
        created_files.append(f.name)
        return f

    app.utils.NamedTemporaryFile = mock_named_temp

    try:
        dummy = DummyFile(b"a" * 15)
        result = process_file(dummy, "Image", 100, 100, "ebook", max_bytes=10, content_type="image/jpeg")

        assert result is None, "Should fail due to size limit"

        for f in created_files:
            assert not os.path.exists(f), f"File {f} was not deleted!"
    finally:
        app.utils.NamedTemporaryFile = original_named_temp
