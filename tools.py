from pathlib import Path


def list_project_files() -> str:
    """
    List files and directories in the current project directory.

    Returns:
        A newline-separated list of files and directories.
    """
    items = []

    for path in Path(".").iterdir():
        if path.name in {".venv", ".git"}:
            continue

        items.append(path.name)

    return "\n".join(sorted(items))


def read_text_file(filename: str) -> str:
    """
    Read a text file from the current project directory.

    Args:
        filename: Relative path to a file inside the project directory.

    Returns:
        The contents of the file.
    """
    project_root = Path(".").resolve()
    requested_path = (project_root / filename).resolve()

    if project_root not in requested_path.parents:
        return "Error: access outside the project directory is not allowed."

    if not requested_path.exists():
        return f"Error: {filename} does not exist."

    if not requested_path.is_file():
        return f"Error: {filename} is not a file."

    try:
        return requested_path.read_text()
    except UnicodeDecodeError:
        return f"Error: {filename} is not a readable text file."


def create_text_file(filename: str, content: str) -> str:
    """
    Create a new text file inside the current project directory.

    Args:
        filename: Relative path to a file inside the project directory.
        content: Text content to write.

    Returns:
        A status message describing the result.
    """
    project_root = Path(".").resolve()
    requested_path = (project_root / filename).resolve()

    if project_root not in requested_path.parents:
        return "Error: writing outside the project directory is not allowed."

    protected_files = {
        "agent.py",
        ".gitignore",
        "requirements.txt",
    }

    if requested_path.name in protected_files:
        return f"Error: {filename} is protected and cannot be modified."

    if requested_path.exists():
        return f"Error: {filename} already exists. Refusing to overwrite it."

    requested_path.write_text(content)

    return f"Successfully created {filename}."


def calculate(operation: str, a: float, b: float) -> str:
    """
    Perform a basic arithmetic calculation.

    Args:
        operation: The operation to perform. Must be one of:
            add, subtract, multiply, divide.
        a: The first number.
        b: The second number.

    Returns:
        The result of the calculation.
    """
    if not isinstance(operation, str):
        return "Error: operation must be a string."

    if not isinstance(a, (int, float)):
        return "Error: a must be a number."

    if not isinstance(b, (int, float)):
        return "Error: b must be a number."

    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":
        if b == 0:
            return "Error: division by zero is not allowed."

        result = a / b

    else:
        return f"Error: unknown operation '{operation}'."

    return str(result)

TOOLS = [
    list_project_files,
    read_text_file,
    create_text_file,
    calculate,
]


TOOL_REGISTRY = {
    "list_project_files": list_project_files,
    "read_text_file": read_text_file,
    "create_text_file": create_text_file,
    "calculate": calculate,
}


APPROVAL_REQUIRED = {
    "create_text_file",
}