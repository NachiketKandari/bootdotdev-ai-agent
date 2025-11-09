import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try: 
        with open(target_file, "r") as f:
            all_content = f.read()
            if len(all_content) > MAX_CHARS:
                file_content_string = all_content[:MAX_CHARS]
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
            else:
                file_content_string = all_content
        return file_content_string
    except Exception as e:
        return f"Error: {e}"