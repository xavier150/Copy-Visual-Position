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
#  BBPL -> BleuRaven Blender Python Library
#  BleuRaven.fr
#  XavierLoux.com
# ----------------------------------------------

from ... import __internal__

def get_template_button_idname(name: str) -> str:
    return __internal__.utils.get_data_operator_idname("tpl_btn_" + name)  # type: ignore

def get_template_button_class_name(name: str) -> str:
    return __internal__.utils.get_operator_class_name("tpl_btn_" + name)  # type: ignore

def get_operator_class_name(name: str) -> str:
    return __internal__.utils.get_operator_class_name(name)  # type: ignore
