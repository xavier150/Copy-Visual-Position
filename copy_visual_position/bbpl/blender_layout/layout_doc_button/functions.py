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

import bpy
from typing import TYPE_CHECKING
from . import types
from . import utils
from ... import __internal__

def add_doc_page_operator(layout: bpy.types.UILayout, url: str="", text: str="", icon: str="HELP"):
    doc_operator = layout.operator(  # type: ignore
        utils.get_open_target_web_page_idname(),
        icon=icon,
        text=text
        )  # type: ignore
    if TYPE_CHECKING:
        doc_operator: types.CustomOpenTargetWebPage_Operator
    
    doc_operator.url = url

    return layout


def add_left_doc_page_operator(layout: bpy.types.UILayout, url: str="", text: str="", icon: str="HELP"):
    new_row = layout.row()
    doc_operator = new_row.operator(  # type: ignore
        utils.get_open_target_web_page_idname(),
        icon=icon,
        text=""
        )  # type: ignore
    
    if TYPE_CHECKING:
        doc_operator: types.CustomOpenTargetWebPage_Operator
    doc_operator.url = url
    new_row.label(text=text)  # type: ignore
    return new_row

def add_right_doc_page_operator(layout: bpy.types.UILayout, url: str="", text: str="", icon: str="HELP"):
    new_row = layout.row()
    new_row.label(text=text)  # type: ignore
    doc_operator = new_row.operator(  # type: ignore
        utils.get_open_target_web_page_idname(),
        icon=icon,
        text=""
        )  # type: ignore
    
    if TYPE_CHECKING:
        doc_operator: types.CustomOpenTargetWebPage_Operator
    doc_operator.url = url
    return new_row

