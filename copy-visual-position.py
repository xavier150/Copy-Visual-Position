#====================== BEGIN GPL LICENSE BLOCK ============================
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
#======================= END GPL LICENSE BLOCK =============================

# ----------------------------------------------
#  with this Addons you will be able to easily copy and paste the visual position of an object in your scene, this works also for Vertices in EditMode and also the chains of Bones in PoseMode
#  xavierloux.com
# ----------------------------------------------

bl_info = {
	'name': 'Copy Visual Position',
	'description': "This addons Copy Visual Position allows to easily copy / paste the visual position of several elements in the scene like Objects, Bones or Vertex and other element in EditMod.",
	'author': 'Loux Xavier (BleuRaven)',
	'version': (0, 1, 1),
	'blender': (2, 79, 0),
	'location': 'View3D > Tool > Copy Visual Position',
	'warning': '',
	"wiki_url": "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Copy_Visual_Position",
	'tracker_url': '',
	'support': 'COMMUNITY',
	'category': '3D_interaction'}

import bpy
import bmesh
import mathutils
import math
import copy
from math import radians
from mathutils import *


########################### [UI (One by one)] ###########################

class VisualPoseOneByOne(bpy.types.Panel): #Is Export panel
	bpy.types.Scene.LastVisualLocation = bpy.props.FloatVectorProperty(
		name = "VisualLocation",
		description	 = "",
		default = (0,0,0),
		precision = 40,
		size=3
		)

	bpy.types.Scene.LastVisualRotation = bpy.props.FloatVectorProperty(
		name = "VisualRotation",
		description	 = "",
		default = (0,0,0),
		precision = 40,
		size=3
		)
		
	bpy.types.Scene.LastVisualScale = bpy.props.FloatVectorProperty(
		name = "VisualScale:",
		description	 = "",
		default = (1,1,1),
		precision = 40,
		size=3
		)
	
	bl_idname = "panel.visualposeonebyone"
	bl_label = "One by one"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Copy visual position"
	
	def draw(self, context):
		scn = context.scene
		prop = bpy.types.Scene
		layout = self.layout
		value = layout
		value.prop(scn, 'LastVisualLocation')
		value.prop(scn, 'LastVisualRotation')
		value.prop(scn, 'LastVisualScale')

		text = layout.row()
		text.label("Copy visual position from active", icon='COPYDOWN')
		text.label("Paste visual position to active", icon='PASTEDOWN')
		Buttons = layout.row(align=True).column()
		Button_loc = Buttons.row()
		Button_rot = Buttons.row()
		Button_scale = Buttons.row()
		Button_all = Buttons.row()
		
		Button_loc.operator("object.copy_visual_location", icon='MAN_TRANS')
		Button_rot.operator("object.copy_visual_rotation", icon='MAN_ROT')
		Button_scale.operator("object.copy_scale", icon='MAN_SCALE')
		Button_all.operator("object.copy_visual_all", icon='MANIPUL')
		
		
		Button_loc.operator("object.paste_visual_location", icon='MAN_TRANS')
		Button_rot.operator("object.paste_visual_rotation", icon='MAN_ROT')
		Button_scale.operator("object.paste_scale", icon='MAN_SCALE')
		Button_all.operator("object.paste_visual_all", icon='MANIPUL')
		
		if bpy.context.active_object is None:
			Buttons.enabled = False
		if bpy.context.object is not None:
			if bpy.context.object.mode == "EDIT" :
				Button_rot.enabled = False
				Button_scale.enabled = False
				Button_all.enabled = False
		else:
			Button_rot.enabled = False
			Button_scale.enabled = False
			Button_all.enabled = False

########################### [Buttons (One by one) ] ###########################

class CopyVisualObjLocButton(bpy.types.Operator):
	bl_label = "Copy loc"
	bl_idname = "object.copy_visual_location"
	bl_description = "Contpy the visual location of the active object"

	def execute(self, context):	
		Scene = bpy.context.scene
		obj = bpy.context.active_object
		if bpy.context.object.mode == "OBJECT":
			Scene.LastVisualLocation = obj.matrix_world * (obj.location * 0)
		if bpy.context.object.mode == "POSE":
			Scene.LastVisualLocation = GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[0]
		if bpy.context.object.mode == "EDIT":
			Scene.LastVisualLocation = GetVisualVertLoc(bpy.context.active_object)
		return {'FINISHED'}
		
		
class CopyVisualObjRotButton(bpy.types.Operator):
	bl_label = "Copy rot"
	bl_idname = "object.copy_visual_rotation"
	bl_description = "Copy the visual rotation of the active object"

	def execute(self, context):		
		Scene = bpy.context.scene
		obj = bpy.context.active_object
		if bpy.context.object.mode == "OBJECT":
			Scene.LastVisualRotation = obj.matrix_world.to_euler()
		if bpy.context.object.mode == "POSE":
			Scene.LastVisualRotation = GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[1]
		return {'FINISHED'}
		
		
class CopyObjScaleButton(bpy.types.Operator):
	bl_label = "Copy scale"
	bl_idname = "object.copy_scale"
	bl_description = "Copy the scale of the active object"

	def execute(self, context):		
		Scene = bpy.context.scene
		obj = bpy.context.active_object
		if bpy.context.object.mode == "OBJECT":
			Scene.LastVisualScale = obj.scale
		if bpy.context.object.mode == "POSE":
			Scene.LastVisualScale = GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[2]
		return {'FINISHED'}

		
class CopyVisualObjPosButton(bpy.types.Operator):
	bl_label = "Copy all"
	bl_idname = "object.copy_visual_all"
	bl_description = "Copy the visual position of the active object"

	def execute(self, context):	
		Scene = bpy.context.scene
		obj = bpy.context.active_object
		if bpy.context.object.mode == "OBJECT":
			Scene.LastVisualLocation = obj.matrix_world * (obj.location * 0)
			Scene.LastVisualRotation = obj.matrix_world.to_euler()
			Scene.LastVisualScale =  obj.scale
		if bpy.context.object.mode == "POSE":
			Trans = GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)
			Scene.LastVisualLocation = Trans[0]
			Scene.LastVisualRotation = Trans[1] 
			Scene.LastVisualScale =  Trans[2]
		return {'FINISHED'}

		
class PasteVisualObjLocButton(bpy.types.Operator):
	bl_label = "Paste loc"
	bl_idname = "object.paste_visual_location"
	bl_description = "Paste the visual location to active object"

	def execute(self, context):		
		Scene = bpy.context.scene
		loc = Vector(Scene.LastVisualLocation)
		rot = Euler(Scene.LastVisualRotation, 'XYZ')
		scale = Vector(Scene.LastVisualScale)
		if bpy.context.object.mode == "OBJECT":
			SetVisualObjPos(bpy.context.active_object, loc, rot, scale, True, False, False)
		if bpy.context.object.mode == "POSE":
			SetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone, loc, rot, scale, True, False, False)
		if bpy.context.object.mode == "EDIT":
			SetVisualVertLoc(bpy.context.active_object, loc)
		return {'FINISHED'}
		
		
class PasteVisualObjRotButton(bpy.types.Operator):
	bl_label = "Paste rot"
	bl_idname = "object.paste_visual_rotation"
	bl_description = "Paste the visual rotation to active object"

	def execute(self, context):		
		Scene = bpy.context.scene
		loc = Vector(Scene.LastVisualLocation)
		rot = Euler(Scene.LastVisualRotation, 'XYZ')
		scale = Vector(Scene.LastVisualScale)
		obj = bpy.context.active_object
		if bpy.context.object.mode == "OBJECT":
			SetVisualObjPos(obj, loc, rot, scale, False, True, False)
		if bpy.context.object.mode == "POSE":
			bone = bpy.context.active_pose_bone
			SetVisualBonePos(obj, bone, loc, rot, scale, False, True, False)
		return {'FINISHED'}
		
		
class PasteObjScaleButton(bpy.types.Operator):
	bl_label = "Paste scale"
	bl_idname = "object.paste_scale"
	bl_description = "Paste the scale to active object"

	def execute(self, context):		
		Scene = bpy.context.scene
		loc = Vector(Scene.LastVisualLocation)
		rot = Euler(Scene.LastVisualRotation, 'XYZ')
		scale = Vector(Scene.LastVisualScale)
		obj = bpy.context.active_object
		if bpy.context.object.mode == "OBJECT":
			SetVisualObjPos(obj, loc, rot, scale, False, False, True)
		if bpy.context.object.mode == "POSE":
			bone = bpy.context.active_pose_bone
			SetVisualBonePos(obj, bone, loc, rot, scale, False, False, True)
		return {'FINISHED'}
		
		
class PasteVisualObjPosButton(bpy.types.Operator):
	bl_label = "Paste all"
	bl_idname = "object.paste_visual_all"
	bl_description = "Paste the visual position to active object"

	def execute(self, context):	
		Scene = bpy.context.scene
		loc = Vector(Scene.LastVisualLocation)
		rot = Euler(Scene.LastVisualRotation, 'XYZ')
		scale = Vector(Scene.LastVisualScale)
		obj = bpy.context.active_object
		if bpy.context.object.mode == "OBJECT":
			SetVisualObjPos(obj, loc, rot, scale, True, True, True)
		if bpy.context.object.mode == "POSE":
			bone = bpy.context.active_pose_bone
			SetVisualBonePos(obj, bone, loc, rot, scale, True, True, True)
		return {'FINISHED'}

########################### [UI (Packed)] ###########################

class VisualPosePacked(bpy.types.Panel): #Is Export panel

	class SaveCopyPosition(bpy.types.PropertyGroup):
		name = bpy.props.StringProperty(name="RefName", default="Unknown")
		location = bpy.props.FloatVectorProperty(name="location")
		rotation = bpy.props.FloatVectorProperty(name="rotation")
		scale = bpy.props.FloatVectorProperty(name="scale")
	bpy.utils.register_class(SaveCopyPosition)
	
	class SaveCopyVertLoc(bpy.types.PropertyGroup):
		id = bpy.props.IntProperty(name="Index")
		location = bpy.props.FloatVectorProperty(name="location")
	bpy.utils.register_class(SaveCopyVertLoc)
	
	bpy.types.Scene.CopiedObjects = bpy.props.CollectionProperty(
		type=SaveCopyPosition
		)
		
	bpy.types.Scene.CopiedBones = bpy.props.CollectionProperty(
		type=SaveCopyPosition
		)
		
	bpy.types.Scene.CopiedVertex = bpy.props.CollectionProperty(
		type=SaveCopyVertLoc
		)
	
	bl_idname = "panel.visualposepacked"
	bl_label = "Packed"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Copy visual position"
	
	def draw(self, context):
		scn = context.scene
		layout = self.layout		

		text = layout.row()
		text.label("Copy visual positions from select", icon='COPYDOWN')
		text.label("Paste visual positions to select", icon='PASTEDOWN')
		Buttons = layout.row(align=True).column()
		Button_objs = Buttons.row()
		Button_bones = Buttons.row()
		Button_vertex = Buttons.row()
				
		Button_objs.operator("object.copy_pack_visual_objs", icon='OBJECT_DATAMODE')
		Button_objs.operator("object.paste_pack_visual_objs", icon='OBJECT_DATAMODE')

		Button_bones.operator("object.copy_pack_visual_bones", icon='POSE_HLT')
		Button_bones.operator("object.paste_pack_visual_bones", icon='POSE_HLT')
		
		Button_vertex.operator("object.copy_pack_visual_vertex", icon='EDITMODE_HLT')
		Button_vertex.operator("object.paste_pack_visual_vertex", icon='EDITMODE_HLT')
		
		if bpy.context.object is not None:
			if bpy.context.object.mode != "OBJECT":
				Button_objs.enabled = False
			if bpy.context.object.mode != "POSE":
				Button_bones.enabled = False
			if bpy.context.object.mode != "EDIT":
				Button_vertex.enabled = False
			if bpy.context.active_object.type != "MESH":
				Button_vertex.enabled = False
		else:
			Button_objs.enabled = False
			Button_bones.enabled = False
			Button_vertex.enabled = False
		
########################### [Buttons (Packed) ] ###########################

class CopyVisualObjPosButton(bpy.types.Operator):
	bl_label = "Copy objs"
	bl_idname = "object.copy_pack_visual_objs"
	bl_description = "Contpy the visual position from selected objects"

	def execute(self, context):		
		Scene = bpy.context.scene
		Scene.CopiedObjects.clear()
		PosList = GetVisualObjsPosPacked(bpy.context.selected_objects)
		for pos in PosList:
			Scene.CopiedObjects.add().name = pos[0]
			Scene.CopiedObjects[pos[0]].location = pos[1]
			Scene.CopiedObjects[pos[0]].rotation = pos[2]
			Scene.CopiedObjects[pos[0]].scale = pos[3]
		return {'FINISHED'}
		
		
class CopyVisualBonePosButton(bpy.types.Operator):
	bl_label = "Copy bones"
	bl_idname = "object.copy_pack_visual_bones"
	bl_description = "Contpy the visual position from selected pose bones"

	def execute(self, context):		
		Scene = bpy.context.scene
		Scene.CopiedBones.clear()
		PosList = GetVisualBonesPosPacked(bpy.context.active_object, bpy.context.selected_pose_bones)
		for pos in PosList:
			Scene.CopiedBones.add().name = pos[0]
			Scene.CopiedBones[pos[0]].location = pos[1]
			Scene.CopiedBones[pos[0]].rotation = pos[2]
			Scene.CopiedBones[pos[0]].scale = pos[3]
		return {'FINISHED'}
		
		
class CopyVisualVertPosButton(bpy.types.Operator):
	bl_label = "Copy vertex"
	bl_idname = "object.copy_pack_visual_vertex"
	bl_description = "Contpy the visual position from selected mesh vertex"

	def execute(self, context):		
		Scene = bpy.context.scene
		Scene.CopiedVertex.clear()
		PosList = []
		obj = bpy.context.edit_object
		me = obj.data
		bm = bmesh.from_edit_mesh(me)
		for vert in bm.verts:
			if vert.select:
				#v.co.x = 0
				ref = vert.index
				PosList.append((ref, vert.co))
				print(ref)
		for pos in PosList:
			id = pos[0]
			prop = Scene.CopiedVertex.add()
			prop.id = id
			prop.location = pos[1]
		return {'FINISHED'}
			
			
class PasteVisualObjPosButton(bpy.types.Operator):
	bl_label = "Paste objs"
	bl_idname = "object.paste_pack_visual_objs"
	bl_description = "Paste the visual position to selected objects"

	def execute(self, context):		
		Scene = bpy.context.scene
		PosList = []
		for co in Scene.CopiedObjects:
			PosList.append((co.name, co.location, co.rotation, co.scale))
		SetVisualObjsPosPacked(bpy.context.selected_objects, PosList, True, True, True)
		return {'FINISHED'}
		
		
class PasteVisualBonePosButton(bpy.types.Operator):
	bl_label = "Paste bones"
	bl_idname = "object.paste_pack_visual_bones"
	bl_description = "Paste the visual position to selected pose bones"

	def execute(self, context):		
		Scene = bpy.context.scene
		PosList = []
		for co in Scene.CopiedBones:
			PosList.append((co.name, co.location, co.rotation, co.scale))
		SetVisualBonesPosPacked(bpy.context.active_object, bpy.context.selected_pose_bones, PosList, True, True, True)
		return {'FINISHED'}
		
		
class PasteVisualVertPosButton(bpy.types.Operator):
	bl_label = "Paste vertex"
	bl_idname = "object.paste_pack_visual_vertex"
	bl_description = "Paste the visual position to selected mesh vertex"

	def execute(self, context):		
		Scene = bpy.context.scene
		PosList = []
		obj = bpy.context.edit_object
		me = obj.data
		bm = bmesh.from_edit_mesh(me)
		
		for cb in Scene.CopiedVertex:
			for vert in bm.verts:
				if vert.select:
					if vert.index == cb.id:
						vert.co = cb.location
						print("VertMove")
		bmesh.update_edit_mesh(me)
		me.update()
		return {'FINISHED'}
		
########################### [Function] ###########################

def ApplyRealMatrixWorldObj(obj, matrix):
	for cons in obj.constraints:
		if cons.type == "CHILD_OF":
			if cons.mute == False:
				if cons.target is not None:
					Child = cons.inverse_matrix
					par = cons.target.matrix_world
					obj.matrix_world = Child.inverted()*par.inverted()*matrix
					return
	obj.matrix_world = matrix
	
def ApplyRealMatrixWorldBones(bone, obj, matrix):
	for cons in bone.constraints:
		if cons.type == "CHILD_OF":
			if cons.mute == False:
				if cons.target is not None:
					Child = cons.inverse_matrix
					if cons.target.type == "ARMATURE":
						par = obj.matrix_world * obj.pose.bones[cons.subtarget].matrix
					else:
						par = cons.target.matrix_world
					bone.matrix = obj.matrix_world.inverted() * (Child.inverted()*par.inverted()*matrix)
					return
	bone.matrix = obj.matrix_world.inverted() * matrix
	
def FindItemInListByName(item, list):
	for TargetItem in list:
		if TargetItem.name == item:
			return TargetItem
	return None

def SetVisualObjPos(obj, loc, rot, scale, UseLoc, UseRot, UseScale):
	#Save
	BaseLoc = copy.deepcopy(obj.location)
	BaseRot = copy.deepcopy(obj.rotation_euler)
	BaseScale = copy.deepcopy(obj.scale)
	#ApplyPos
	mat_loc = Matrix.Translation(loc)
	mat_rot = rot.to_matrix().to_4x4()
	matrix = mat_loc * mat_rot
	ApplyRealMatrixWorldObj(obj, matrix)
	obj.scale = scale
	#ResetNotDesiredValue
	if UseLoc == False:
		obj.location = BaseLoc
	if UseRot == False:
		obj.rotation_euler = BaseRot
	if UseScale == False:
		obj.scale = BaseScale
		
def GetVisualVertLoc(obj):
	#Save
	BaseLoc = copy.deepcopy(bpy.context.space_data.cursor_location)
	#ApplyPos
	bpy.ops.view3d.snap_cursor_to_selected()
	loc = copy.deepcopy(bpy.context.space_data.cursor_location)
	bpy.context.space_data.cursor_location = BaseLoc
	return(loc)

def SetVisualVertLoc(obj, loc):
	#Save
	BaseLoc = copy.deepcopy(bpy.context.space_data.cursor_location)
	#ApplyPos
	bpy.context.space_data.cursor_location = loc
	bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
	bpy.context.space_data.cursor_location = BaseLoc

def GetVisualBonePos(obj, Bone):
	matrix_Pose = obj.matrix_world * Bone.matrix
	loc = matrix_Pose * Vector((0,0,0))
	rot = matrix_Pose.to_euler()
	scale = Bone.scale
	return((loc, rot, scale))
	
def SetVisualBonePos(obj, Bone, loc, rot, scale, UseLoc, UseRot, UseScale):
	#Save
	BaseLoc = copy.deepcopy(Bone.location)
	BaseScale = copy.deepcopy(Bone.scale)
	RotModeBase = copy.deepcopy(Bone.rotation_mode)
	Bone.rotation_mode = 'XYZ'
	BaseRot = copy.deepcopy(Bone.rotation_euler)
	#ApplyPos	
	mat_loc = Matrix.Translation(loc)
	mat_rot = rot.to_matrix().to_4x4()
	matrix = mat_loc * mat_rot
	ApplyRealMatrixWorldBones(Bone, obj, matrix)
	Bone.scale = scale
	#ResetNotDesiredValue
	if UseLoc == False:
		Bone.location = BaseLoc
	if UseRot == False:
		Bone.rotation_euler = BaseRot
	if UseScale == False:
		Bone.scale = BaseScale
	Bone.rotation_mode = RotModeBase
		
def GetVisualObjsPosPacked(TargetObjs):
	PositionList = []
	for obj in TargetObjs:
		loc = obj.matrix_world * (obj.location * 0)
		rot = obj.matrix_world.to_euler()
		scale = obj.scale
		PositionList.append((obj.name, loc, rot, scale))
	return PositionList
		
def SetVisualObjsPosPacked(TargetObjs, PositionList, UseLoc, UseRot, UseScale):
		
	for pl in PositionList:
		TargetBone = FindItemInListByName(pl[0], TargetObjs)
		if TargetBone is not None:
			loc = Vector(pl[1])
			rot = Euler(pl[2], 'XYZ')
			scale = Vector(pl[3])
			SetVisualObjPos(TargetBone, loc, rot, scale, UseLoc, UseRot, UseScale)
			
def GetVisualBonesPosPacked(obj, TargetBones):
	PositionList = []
	for bone in TargetBones:
		loc = GetVisualBonePos(obj, bone)[0]
		rot = GetVisualBonePos(obj, bone)[1]
		scale = GetVisualBonePos(obj, bone)[2]
		PositionList.append((bone.name, loc, rot, scale))
	return PositionList
		
def SetVisualBonesPosPacked(obj, TargetBones, PositionList, UseLoc, UseRot, UseScale):
			
	for pl in PositionList:
		TargetBone = FindItemInListByName(pl[0], TargetBones)
		if TargetBone is not None:
			loc = Vector(pl[1])
			rot = Euler(pl[2], 'XYZ')
			scale = Vector(pl[3])
			SetVisualBonePos(obj, TargetBone, loc, rot, scale, UseLoc, UseRot, UseScale)

#############################[...]#############################


def register():

	bpy.utils.register_module(__name__)
	bpy.types.Scene.my_prop = bpy.props.StringProperty(default="default value")


def unregister():
	bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
	register()