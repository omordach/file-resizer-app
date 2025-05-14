import os
import shutil
import subprocess
from tempfile import NamedTemporaryFile

def process_file(file, file_type, width, height, quality):
    print(f"Processing file: {file.filename}, type: {file_type}, width: {width}, height: {height}, quality: {quality}")

    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_input:
        shutil.copyfileobj(file.file, temp_input)
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
        cmd = ["convert", temp_input_path, "-resize", size_param, output_path]

    print(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during subprocess execution: {e}")
        return None

    if not os.path.exists(output_path):
        print(f"Expected output file does not exist: {output_path}")
        return None

    print(f"Output file generated at: {output_path}")
    return output_path
