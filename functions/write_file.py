from os import path, makedirs

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


    