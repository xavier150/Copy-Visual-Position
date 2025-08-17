# SPDX-FileCopyrightText: 2023-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  BBPL -> BleuRaven Blender Python Library
#  https://github.com/xavier150/BBPL
# ----------------------------------------------

import bpy
from typing import List, Callable, Optional
from . import types

def add_string_selector(
    property_name: str, 
    property_selector_name: str, 
    default: str="", 
    name: str="", 
    description: str="", 
    items: List[str] = [], 
    update: Optional[Callable[..., None]] = None
) -> types.StringSelector:
    my_string_selector = types.StringSelector(property_name, property_selector_name)
    my_string_selector.name = name
    my_string_selector.default = default
    my_string_selector.description = description
    my_string_selector.items = items
    my_string_selector.update = update
    my_string_selector.create_properties()
    return my_string_selector

def draw_string_selector(owner, layout: bpy.types.UILayout, prop_name = "my_prop_id", selector_prop_name = "my_prop_id_selector", icon: str = "PREFERENCES",  text=None):
    row = layout.row(align=True)
    if isinstance(text, str):
        row.prop(owner, prop_name, text=text)
    else:
        row.prop(owner, prop_name)
    row.prop(owner, selector_prop_name, text="", icon=icon, icon_only=True)
    return row