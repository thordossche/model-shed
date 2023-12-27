import os
import zipfile
import tempfile

def zip_directory(directory_path):
    with tempfile.TemporaryFile() as temp_zip:
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, start=directory_path))

        temp_zip.seek(0)
        zip_in_memory = temp_zip.read()

    return zip_in_memory

def unzip_to_directory(zip_in_memory, target_directory):
    with tempfile.TemporaryFile() as temp_zip:
        temp_zip.write(zip_in_memory)
        temp_zip.seek(0)
        zipfile.ZipFile(temp_zip).extractall(target_directory)

