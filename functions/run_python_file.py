import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if not os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", file_path_abs]
        if args != None:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        
        output: list[str] = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
        return "\n".join(output)

    except Exception as e:
        print(f"Error: executing Python file: {e}")


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python file with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath of the Python file to execute, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": "string",
                    "description": "optional arguments"
                },
            },
            "required" : ["file_path"],
        },
    },
}
