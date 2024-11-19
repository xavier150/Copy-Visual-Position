# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

# ----------------------------------------------
#  BBAM -> BleuRaven Blender Addon Manager
#  https://github.com/xavier150/BBAM
#  BleuRaven.fr
#  XavierLoux.com
# ----------------------------------------------

import sys
import re
import subprocess

def build_extension(src, dst, blender_executable_path):
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
        '--command', 'extension', 'build',
        '--source-dir', src,
        '--output-filepath', dst,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result

def get_build_file(build_result):
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

def validate_extension(path, blender_executable_path):
    """
    Validates the built extension using Blender's executable.

    Parameters:
        path (str): Path to the extension file to validate.
        blender_executable_path (str): Path to the Blender executable.
    """
    validate_command = [
        blender_executable_path,
        '--command', 'extension', 'validate', 
        path,
    ]
    result = subprocess.run(validate_command, capture_output=True, text=True)

    # Output results for debugging purposes
    if result.returncode == 0:
        print("Validation successful.")
    else:
        print(f"Validation failed. Error: {result.stderr}", file=sys.stderr)