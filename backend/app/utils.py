import os
import shutil
import subprocess
from tempfile import NamedTemporaryFile
from typing import Optional

def _copy_with_limit(src, dst, max_bytes: Optional[int] = None) -> int:
    total = 0
    chunk_size = 1024 * 1024
    while True:
        chunk = src.read(chunk_size)
        if not chunk:
            break
        total += len(chunk)
        if max_bytes is not None and total > max_bytes:
            raise ValueError("Uploaded file exceeds size limit")
        dst.write(chunk)
    try:
        src.seek(0)
    except Exception:
        pass
    return total


def process_file(file, file_type, width, height, quality, max_bytes: Optional[int] = None, content_type: Optional[str] = None):
    print(f"Processing file: {getattr(file, 'filename', 'unknown')}, type: {file_type}, width: {width}, height: {height}, quality: {quality}")

    # Map validated content_type to a safe file extension to prevent spoofing
    ext_map = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "application/pdf": ".pdf"
    }
    # Fallback to .bin to avoid ImageMagick delegate execution from spoofed extensions like .mvg
    safe_suffix = ext_map.get(content_type, ".bin")

    with NamedTemporaryFile(delete=False, suffix=safe_suffix) as temp_input:
        try:
            _copy_with_limit(file.file, temp_input, max_bytes=max_bytes)
        except ValueError:
            return None
        temp_input_path = temp_input.name

    output_dir = os.path.dirname(temp_input_path)
    output_filename = os.path.basename(temp_input_path)

    if file_type == "PDF":
        # Use Ghostscript for proper PDF compression
        output_path = os.path.join(output_dir, "processed_" + output_filename)
        quality_setting = f"/{quality}" if quality else "/ebook"
        cmd = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dSAFER",
            f"-dPDFSETTINGS={quality_setting}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            temp_input_path
        ]
    else:
        # For Images, use convert to create a new file
        output_path = os.path.join(output_dir, "processed_" + output_filename)
        size_param = f"{width}x{height}" if width and height else "50%"
        cmd = [
            "convert",
            "-limit", "memory", "64MiB",
            "-limit", "map", "128MiB",
            "-limit", "disk", "1GiB",
            "-limit", "time", "60",
            temp_input_path,
            "-resize", size_param,
            output_path,
        ]

    print(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during subprocess execution: {e}")
        try:
            os.remove(temp_input_path)
        except Exception:
            pass
        return None

    if not os.path.exists(output_path):
        print(f"Expected output file does not exist: {output_path}")
        try:
            os.remove(temp_input_path)
        except Exception:
            pass
        return None

    print(f"Output file generated at: {output_path}")
    try:
        os.remove(temp_input_path)
    except Exception:
        pass
    return output_path
