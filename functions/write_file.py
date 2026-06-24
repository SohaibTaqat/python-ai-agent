import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if not target_file.startswith(working_dir_abs + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    try:
        with open(target_file, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write to an existing file, or create it necessary ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to to run",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="content to write to file"
            )
        },
        required=["file_path", "content"],
    ), 
)

    