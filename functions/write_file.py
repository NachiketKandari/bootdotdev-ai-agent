import os

def write_file(working_directory, file_path, content):
    abs_wd = os.path.abspath(working_directory)
    abs_fp = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_fp.startswith(abs_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_fp):
        f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_fp, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

