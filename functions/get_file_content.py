import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.join(working_dir_abs, file_path)

            
        if not os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs, "r") as f:
            content: str = f.read(MAX_CHARS)
            if f.read(1):
                return content + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content
    
    except Exception as e:
        print(f"Error: {e}")
