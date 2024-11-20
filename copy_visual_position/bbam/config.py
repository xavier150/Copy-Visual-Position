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

# Configuration file names and paths for the addon build process

# JSON file containing addon generation configurations
addon_generate_config = "addon_generate_config.json"

# TOML file containing the Blender manifest details
blender_manifest = "blender_manifest.toml"

# Version of the manifest schema being used
manifest_schema_version = "1.0.0"

# Folder where the generated build files will be stored
build_output_folder = "generated_builds"

show_debug = False