# SPDX-FileCopyrightText: 2024-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  BBAM -> BleuRaven Blender Addon Manager
#  https://github.com/xavier150/BBAM
# ----------------------------------------------

import re
import subprocess
from typing import Optional

def build_extension(
    src: str,
    dst: str,
    blender_executable_path: str
):
    """
    Builds an extension using Blender's executable with specified source and destination paths.

    Parameters:
        src (str): Path to the source directory of the extension.
        dst (str): Destination path for the built extension.
        blender_executable_path (str): Path to the Blender executable.

    Returns:
        subprocess.CompletedProcess: The result of the subprocess command execution.
    """
    command = [
        blender_executable_path,
        '--background',
        '--factory-startup',
        '--command', 'extension', 'build',
        '--source-dir', src,
        '--output-filepath', dst,
    ]


    result = subprocess.run(command, capture_output=True, text=True)
    return result

def get_build_file(
    build_result
) -> Optional[str]:
    """
    Extracts the path of the created build file from the build result output.

    Parameters:
        build_result (subprocess.CompletedProcess): The result of the build command.

    Returns:
        str: The path of the created build file, if found; otherwise, None.
    """
    match = re.search(r'created: "([^"]+)"', build_result.stdout)
    if match:
        return match.group(1)
    return None

def validate_extension(
    path: str, 
    blender_executable_path: str
):
    """
    Validates the built extension using Blender's executable.

    Parameters:
        path (str): Path to the extension file to validate.
        blender_executable_path (str): Path to the Blender executable.
    """
    validate_command = [
        blender_executable_path,
        '--background',
        '--factory-startup',
        '--command', 'extension', 'validate', 
        path,
    ]

    result = subprocess.run(validate_command, capture_output=True, text=True)
    return result