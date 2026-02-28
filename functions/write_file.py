from os import path, makedirs
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes content to a file relative to the working directory, creating parent directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path" : types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory," \
            ),
            "content" : types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
            )
        },
    ),
)

def write_file(working_directory, file_path, content ):
    work_abs = path.abspath(working_directory)
    target = path.normpath(path.join(work_abs, file_path))
    
    if path.commonpath([work_abs, target]) != work_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if path.isdir(target):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    makedirs(path.dirname(target), exist_ok = True)

    with open(target, 'w') as file:
        file.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    