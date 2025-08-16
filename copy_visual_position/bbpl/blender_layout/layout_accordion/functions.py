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
import typing
from typing import Optional, Tuple
from . import types


def add_ui_accordion(name: str=""):
    return bpy.props.PointerProperty(type=types.get_layout_accordion_class(), name=name)

def get_accordion(data: typing.Any, property: str) -> Optional[types.CustomAccordionUI_PropertyGroup]:
    prop = getattr(data, property, None)
    if isinstance(prop, types.CustomAccordionUI_PropertyGroup):
        return prop
    else:
        print(f"The property '{property}' was not found.")
        return None

def draw_accordion(layout: bpy.types.UILayout, data: typing.Any, property: str) -> Tuple[Optional[bpy.types.UILayout], Optional[bpy.types.UILayout]]:
    prop = getattr(data, property, None)
    if isinstance(prop, types.CustomAccordionUI_PropertyGroup):
        return prop.draw(layout)
        
    else:
        print(f"The property '{property}' was not found.")
        return None, None
