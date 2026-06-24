import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if not target_file.startswith(working_dir_abs + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e}"
    
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a file's content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to return content from",
            ),
        },
        required=["file_path"],
    ),
)