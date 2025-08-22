import os
import shutil
import subprocess
from tempfile import NamedTemporaryFile
from PIL import Image

def process_file(file, file_type, width, height, quality):
    print(f"Processing file: {file.filename}, type: {file_type}, width: {width}, height: {height}, quality: {quality}")

    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_input:
        shutil.copyfileobj(file.file, temp_input)
        temp_input_path = temp_input.name

    output_dir = os.path.dirname(temp_input_path)
    output_filename = os.path.basename(temp_input_path)

    if file_type == "PDF":
        output_path = os.path.join(output_dir, "processed_" + output_filename)
        quality_setting = f"/{quality}" if quality else "/ebook"
        if shutil.which("gs"):
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
            print(f"Running command: {' '.join(cmd)}")
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error during subprocess execution: {e}")
                return None
        else:
            # Fallback: simply copy the file if Ghostscript is unavailable
            shutil.copy(temp_input_path, output_path)
    else:
        output_path = os.path.join(output_dir, "processed_" + output_filename)
        if shutil.which("convert"):
            size_param = f"{width}x{height}" if width and height else "50%"
            cmd = ["convert", temp_input_path, "-resize", size_param, output_path]
            print(f"Running command: {' '.join(cmd)}")
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error during subprocess execution: {e}")
                return None
        else:
            # Fallback: use Pillow for image resizing if ImageMagick is unavailable
            try:
                with Image.open(temp_input_path) as img:
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    if width and height:
                        img = img.resize((width, height))
                    else:
                        img = img.resize((img.width // 2, img.height // 2))
                    img.save(output_path)
            except Exception as e:
                print(f"Error during image processing: {e}")
                return None

    if not os.path.exists(output_path):
        print(f"Expected output file does not exist: {output_path}")
        return None

    print(f"Output file generated at: {output_path}")
    return output_path
