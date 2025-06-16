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

from pathlib import Path
import argparse
import sys
import importlib.util

# ---------------------------------------------------------------
#  This script is used to install the BBAM addon from Blender.
#  See 'exemple_file.py' for running this script from Blender
# ----------------------------------------------------------------

parser = argparse.ArgumentParser(description="Installer BBAM depuis Blender")
parser.add_argument("--current_only", type=str, help="Build only addon for the current Blender version", default="False")
args = parser.parse_args()
current_only: bool = args.current_only.lower() == 'true'

# get bbam __init__.py file avec pathlib
bbam_path = (Path(__file__).parent.parent / "__init__.py").resolve()
module_name = "bbam"

# Load and run bbam
spec = importlib.util.spec_from_file_location(module_name, str(bbam_path))
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load spec or loader for {module_name} from {bbam_path}")
module = importlib.util.module_from_spec(spec)  # type: ignore
sys.modules[module_name] = module
spec.loader.exec_module(module)

# VS Code Type Checking
import typing
if typing.TYPE_CHECKING:
    import bbam
    module: bbam  # type: ignore

module.install_from_blender(current_only=current_only)

