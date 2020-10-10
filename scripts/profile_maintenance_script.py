#!/usr/bin/env python3

"""
Script to maintain (i.e. bulk edit) profiles of educators/conveners/etc.

Kilian Lieret 2020
"""

# std
from pathlib import Path
import oyaml as yaml  # same as normal yaml, only it keeps order of keys
from typing import List, Callable, Tuple, Dict, Any

this_directory = Path(__file__).resolve().parent
profile_directory = this_directory.parent / "_educators"


def get_content_header(lines: List[str]) -> Tuple[str, Dict[str, Any]]:
    """ Get header of Jekyll file

    Args:
        lines: Lines of profile

    Returns:
        content (everything below header as a string),
        header (parsed yaml, i.e. as dictionary structure)
    """
    header_lines = []
    content_lines = []
    is_content = False
    for i_line, line in enumerate(lines):
        line = line.strip()
        if i_line == 0:
            assert line == "---"
            continue
        if line == "---":
            is_content = True
            continue
        if is_content:
            content_lines.append(line)
        else:
            header_lines.append(line)
    header = "\n".join(header_lines)
    content = "\n".join(content_lines)
    return content, yaml.safe_load(header)


def read_transform_write(
    path: Path, header_transform_fct: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> None:
    """ Opens profile, reads it, transforms the header, writes back

    Args:
        path: Path to open
        header_transform_fct: Function that takes parsed yaml and returns a new
            nested data structure that should be written back

    Returns:
        None
    """
    with Path(path).open("r") as file:
        content, header = get_content_header(file.readlines())
        header = header_transform_fct(header)
    new_file_content = "---\n"
    new_file_content += yaml.dump(header)
    new_file_content += "---\n"
    new_file_content += content
    with Path(path).open("w") as file:
        file.write(new_file_content)


def main():
    """ Loop over all profiles and apply read_transform_write.

    MAKE SURE YOU SET THE RIGHT TRANSFORMATION FUNCTION HERE!

    Returns:
        None
    """
    for file in profile_directory.iterdir():
        read_transform_write(file, lambda x: x)


if __name__ == "__main__":
    main()
