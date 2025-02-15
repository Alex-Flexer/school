"""Module provides functionality from communicating with os """
import os


def get_script_from_file(filename: str) -> str:
    """
    Function return sql-request from file
    """
    with open(os.path.join("./db", "scripts", filename), "r", encoding="utf-8") as f:
        return f.read()
