import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)



def get_files_info(working_directory, directory="."):
    work_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(work_abs, directory))
    
    if os.path.commonpath([work_abs, target]) != work_abs:
        return f'Error: Cannot list "{directory}" as it is outside the working directory'
    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'
    results = ""
    with os.scandir(target) as items:
        for item in items:
            print(item.name)
            if item.is_dir() or item.is_file():
                name = item.name
                size = item.stat().st_size
                is_dir = item.is_dir()
                results += f'- {name}: file_size={size} bytes, is_dir={is_dir}  \n'
    return results