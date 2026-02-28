from os import path
import subprocess
from google.genai import types
schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Executes a Python file relative to the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path" : types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to execute, relative to the working directory",
            ),
            "args" : types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python script"
            )
        },

    ),
)

def run_python_file(working_directory, file_path, args=None):

    work_abs = path.abspath(working_directory)
    target = path.normpath(path.join(work_abs, file_path))
    print(target)
    if path.commonpath([work_abs, target]) != work_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not path.isfile(target):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if target[-2:] != "py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python3", target ]

    result = subprocess.run(command, 
                            capture_output=True, 
                            text=True, 
                            timeout=30
                              )
    
    if result.returncode != 0:
        return f"Process exited with code {result.returncode}"
    
    out = ""
    err = ""
    
    if result.stdout: 
        out +=  f"STDOUT: {result.stdout}"
    if result.stderr:
        err += f"\nSTDERR: {result.stderr}"
    output = out + err

    if output:
        return output
    else:
        return "No output produced" 
    


