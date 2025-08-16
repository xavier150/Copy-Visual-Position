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
from typing import Optional, Callable, Any
from ... import __internal__



class StringSelector():

    def __init__(self, property_name: str, property_selector_name: str):
        self.property_name: str = property_name
        self.property_selector_name: str = property_selector_name
        self.name: str = ""
        self.default: str = ""
        self.description: str = ""
        self.items = []
        self.update: Optional[Callable[..., None]] = None
        self.string_property: Any = None
        self.enum_selector: Any = None


    def create_properties(self):
        string_selector = self

        def string_update_wrapper(property_self: bpy.types.bpy_struct, context: bpy.types.Context):
            update_selector_from_string(property_self, string_selector)
            if string_selector.update:
                string_selector.update()

        def enum_update_wrapper(property_self: bpy.types.bpy_struct, context: bpy.types.Context):
            update_string_from_enum(property_self, string_selector)
            if string_selector.update:
                string_selector.update()
            

        self.string_property = bpy.props.StringProperty(  # type: ignore
            default=self.default,
            name=self.name,
            description=self.description,
            update=string_update_wrapper
            )

        self.enum_selector = bpy.props.EnumProperty(  # type: ignore
            items=self.items,  # type: ignore
            update=enum_update_wrapper,
            options={"HIDDEN", "SKIP_SAVE"}
            )


def update_string_from_enum(self: Any, string_selector: StringSelector):
    string_name = string_selector.property_name
    selector_name = string_selector.property_selector_name
    if getattr(self, string_name) != getattr(self, selector_name):
        setattr(self, string_name, getattr(self, selector_name))
        #print("Selector update...")

def update_selector_from_string(self: Any, string_selector: StringSelector):
    string_name = string_selector.property_name
    selector_name = string_selector.property_selector_name
    if getattr(self, selector_name) != getattr(self, string_name):
        setattr(self, selector_name, getattr(self, string_name))
        #print("Selector update...")

classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore