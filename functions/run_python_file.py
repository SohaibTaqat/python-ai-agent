import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if not target_file.startswith(working_dir_abs + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args:
        command.extend(args)

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)
    
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
            
        if not result.stdout and not result.stderr:
            output += "No output produced\n"
        if result.stdout:
            output += f"STDOUT: {result.stdout}\n"
        if result.stderr:
            output += f"STDERR: {result.stderr}\n"
    
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and accepts optional additional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to to run",
            ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                items= types.Schema(type=types.Type.STRING),
                description="optional additional argument to run the file with"
            )
        },
        required=["file_path"],
    ), 
)

    