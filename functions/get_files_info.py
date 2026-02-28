from os import path, listdir, scandir
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
    work_abs = path.abspath(working_directory)
    target = path.normpath(path.join(work_abs, directory))
    
    if path.commonpath([work_abs, target]) != work_abs:
        return f'Error: Cannot list "{directory}" as it is outside the working directory'
    if not path.isdir(target):
        return f'Error: "{directory}" is not a directory'
    results = ""
    with scandir(target) as items:
        for item in items:
            if path.isdir(item) or item is path.isfile(item):
                name = item.name
                size = path.getsize(item)
                is_dir = path.isdir(item)
                results += f'- {name}: file_size={size} bytes, is_dir={is_dir}  \n'
    return results