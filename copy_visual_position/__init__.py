# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Copy Visual Position
#  https://github.com/xavier150/Copy-Visual-Position
# ----------------------------------------------

# ----------------------------------------------
#  with this Addons you will be able to easily copy and paste the visual position of an object in your scene, this works also for Vertices in EditMode and also the chains of Bones in PoseMode
#  xavierloux.com
# ----------------------------------------------

try:
    import bpy
    import importlib
    from . import cvp_panels
    from . import cvp_props
    from . import cvp_ui
    from . import cvp_utils
    from . import single_object
    from . import packed_objs
    from . import packed_bones
    from . import packed_vertices

    import importlib
    if "cvp_panels" in locals():
        importlib.reload(cvp_panels)
    if "cvp_props" in locals():
        importlib.reload(cvp_props)
    if "cvp_ui" in locals():
        importlib.reload(cvp_ui)
    if "cvp_utils" in locals():
        importlib.reload(cvp_utils)
    if "single_object" in locals():
        importlib.reload(single_object)
    if "packed_objs" in locals():
        importlib.reload(packed_objs)
    if "packed_bones" in locals():
        importlib.reload(packed_bones)
    if "packed_vertices" in locals():
        importlib.reload(packed_vertices)


    bl_info = {}


    classes = (
    )


    def register():
        try:
            for cls in classes:
                bpy.utils.register_class(cls)


            cvp_panels.register()
            cvp_props.register()
            cvp_ui.register()

            single_object.register()
            packed_objs.register()
            packed_bones.register()
            packed_vertices.register()
        except Exception as _:
            import traceback
            print("Failed to register addon:")
            print("\033[91m" + "---------------------------------" + "\033[0m")
            traceback.print_exc()
            print("\033[91m" + "---------------------------------" + "\033[0m")



    def unregister():
        try:
            for cls in reversed(classes):
                bpy.utils.unregister_class(cls)

            packed_vertices.unregister()
            packed_bones.unregister()
            packed_objs.unregister()
            single_object.unregister()

            cvp_ui.unregister()
            cvp_props.unregister()
            cvp_panels.unregister()

        except Exception as _:
            import traceback
            print("Failed to unregister addon:")
            print("\033[91m" + "---------------------------------" + "\033[0m")
            traceback.print_exc()
            print("\033[91m" + "---------------------------------" + "\033[0m")


except Exception as _:
    import traceback
    print("Failed to import addon modules:")
    print("\033[91m" + "---------------------------------" + "\033[0m")
    traceback.print_exc()
    print("\033[91m" + "---------------------------------" + "\033[0m")