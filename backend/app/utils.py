import os, subprocess, shutil
from tempfile import NamedTemporaryFile


def process_file(file, file_type, width, height, quality):
    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_input:
        shutil.copyfileobj(file.file, temp_input)
        temp_input_path = temp_input.name

    temp_output_path = temp_input_path.replace('.', '_out.')

    if file_type == "PDF":
        quality_setting = f"-dPDFSETTINGS=/{quality}" if quality else "-dPDFSETTINGS=/ebook"
        subprocess.run(["ps2pdf", quality_setting, temp_input_path, temp_output_path], check=True)
    else:
        size_param = f"{width}x{height}" if width and height else "50%"
        subprocess.run(["mogrify", "-path", os.path.dirname(temp_output_path), "-resize", size_param, temp_input_path], check=True)

    print(f"Processed {file.filename} as {file_type} with params {width}x{height or ''} {quality or ''}")
    return temp_output_path