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

import os
import json
from typing import Optional
from .bbam_addon_config_type import BBAM_AddonConfig
from .. import config

def load_addon_config_from_json(
    addon_path: str
) -> Optional[BBAM_AddonConfig]:

    # Get the path of the current addon's configuration file from `config`
    addon_manifest_name = config.addon_generate_config
    addon_manifest_path = os.path.abspath(os.path.join(addon_path, addon_manifest_name))

    # Load the manifest file data if it exists
    if os.path.isfile(addon_manifest_path):
        with open(addon_manifest_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            addon_config = BBAM_AddonConfig()
            addon_config.set_config_from_dict(data)
        return addon_config
    else:
        print(f"Error: '{addon_manifest_name}' was not found in '{addon_manifest_path}'.")
        return None

    