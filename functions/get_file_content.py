from os import path

def get_file_content(working_directory, file_path):
    work_abs = path.abspath(working_directory)
    target = path.normpath(path.join(work_abs, file_path))
    print(target)
    if path.commonpath([work_abs, target]) != work_abs:
        return f'Error: Cannot read"{file_path}" as it is outside the working directory'
    if not path.isfile(target):
        return f'Error: "{file_path}" is not a file'

    MAX_CHARS = 10000

    with open(target, "r") as f:
        content = f.read(MAX_CHARS)

         # After reading the first MAX_CHARS...
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    print(content)
