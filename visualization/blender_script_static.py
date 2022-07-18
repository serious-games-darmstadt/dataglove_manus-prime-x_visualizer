import bpy
import os
from math import radians
from enum import Enum
import mathutils
import visualization.constraints as cnstr


"""
    Enum class for the mapping between index and spread/stretch value (WACH format)
"""
class WachFormat(Enum):
    THUMB_SPREAD = 0
    INDEX_FINGER_SPREAD = 1
    MIDDLE_FINGER_SPREAD = 2
    RING_FINGER_SPREAD = 3
    PINKY_SPREAD = 4
    THUMB_STRETCH_CMC = 5
    THUMB_STRETCH_MCP = 6
    THUMB_STRETCH_IP = 7
    INDEX_FINGER_STRETCH_MCP = 8
    INDEX_FINGER_STRETCH_PIP = 9
    INDEX_FINGER_STRETCH_DIP = 10
    MIDDLE_FINGER_STRETCH_MCP = 11
    MIDDLE_FINGER_STRETCH_PIP = 12
    MIDDLE_FINGER_STRETCH_DIP = 13
    RING_FINGER_STRETCH_MCP = 14
    RING_FINGER_STRETCH_PIP = 15
    RING_FINGER_STRETCH_DIP = 16
    PINKY_STRETCH_MCP = 17
    PINKY_STRETCH_PIP = 18
    PINKY_STRETCH_DIP = 19


"""
    GLOBAL VARIABLES
"""
# These variables will be set in viz.py
EXPORT_FILE_TYPE = ''
STL_PATH_STR = ''
BLEND_PATH_STR = ''
OBJ_PATH_STR = ''
LABEL = ''
HAND = ''
sample_values = []
EXPORT_PNG = False
EXPORT_PNG_STR = ''


# Input Paths
FBX_HAND_LEFT_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 R"resources/Manus-Hand-Left.fbx"))
FBX_HAND_RIGHT_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 R"resources/Manus-Hand-Right.fbx"))

# Output Paths
STL_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), STL_PATH_STR))
BLEND_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), BLEND_PATH_STR))
OBJ_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), OBJ_PATH_STR))
EXPORT_PNG_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), EXPORT_PNG_STR))

# Convert values to float
sample_values = [float(e) for _, e in enumerate(sample_values)]

# Clean scene with cube
bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink=True)
if not EXPORT_PNG:  # clean scene of every object that is not needed
    bpy.data.objects.remove(bpy.data.objects['Camera'], do_unlink=True)
    bpy.data.objects.remove(bpy.data.objects['Light'], do_unlink=True)

# Import FBX for right or left hand
fbx_path = FBX_HAND_LEFT_FILE_PATH if HAND == "Left" else FBX_HAND_RIGHT_FILE_PATH
bpy.ops.import_scene.fbx(filepath=fbx_path, automatic_bone_orientation=True)

# Select Hand Models Armature as Active
obj = bpy.data.objects['Armature']
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='POSE')  # pose mode for changing joint values


"""
    ALTER JOINT VALUES
"""
# Make changes to joint values based on input data
# For each joint on each finger, namely
# MCP, PIP, DIP (idx: 1, 2, 3) for the fingers
# CMC, MCP, IP (idx: 1, 2, 3) for the thumb
for pose_bone_index in range(1, 4):
    for finger_name in ["thumb", "index", "middle", "ring", "pinky"]:

        # Get blender pose bone object
        pose_bone_name = f"{finger_name}_0{pose_bone_index}_{HAND[0].lower()}"
        pose_bone = obj.pose.bones[pose_bone_name]
        pose_bone.rotation_mode = 'QUATERNION'

        # Local coordinate system for joints different than global coordinate system
        # Local coordinate axis of joints for spread and stretch value
        # EULER: (X, Y, Z) ==> (axis_spread, 0.0, -1*axis_stretch)

        # THUMB
        if finger_name == "thumb":
            if pose_bone_index == 1:  # Thumb CMC
                # Extract spread and stretch values from sample data
                v_stretch = sample_values[WachFormat.THUMB_STRETCH_CMC.value]
                v_spread = sample_values[WachFormat.THUMB_SPREAD.value]

                # Convert normalized sample values to degree
                stretch_value_degree = cnstr.get_stretch_thumb_cmc_constraint_degree(v_stretch)
                spread_value_degree = cnstr.get_spread_thumb_cmc_constraint_degree(v_spread)

                # Apply spread rotation for thumb cmc
                # Also switch signs for values except spread (CMC) because of blender ...
                rot_eul = mathutils.Euler(
                    (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            elif pose_bone_index == 2:  # Thumb MCP
                v_stretch = sample_values[WachFormat.THUMB_STRETCH_MCP.value]
                stretch_value_degree = cnstr.get_stretch_thumb_mcp_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            else:  # Thumb IP
                v_stretch = sample_values[WachFormat.THUMB_STRETCH_IP.value]
                stretch_value_degree = cnstr.get_stretch_thumb_ip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

        # Index finger
        elif finger_name == "index":
            if pose_bone_index == 1:  # Index MCP
                v_stretch = sample_values[WachFormat.INDEX_FINGER_STRETCH_MCP.value]
                v_spread = sample_values[WachFormat.INDEX_FINGER_SPREAD.value]
                stretch_value_degree = cnstr.get_stretch_finger_mcp_rest_constraint_degree(v_stretch)
                spread_value_degree = cnstr.get_spread_finger_constraint_degree(v_spread)
                rot_eul = mathutils.Euler(
                    (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            elif pose_bone_index == 2:  # Index PIP
                v_stretch = sample_values[WachFormat.INDEX_FINGER_STRETCH_PIP.value]
                stretch_value_degree = cnstr.get_stretch_finger_pip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            else:  # Index DIP
                v_stretch = sample_values[WachFormat.INDEX_FINGER_STRETCH_DIP.value]
                stretch_value_degree = cnstr.get_stretch_finger_dip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

        # Middle finger
        elif finger_name == 'middle':
            if pose_bone_index == 1:  # Middle MCP
                v_stretch = sample_values[WachFormat.MIDDLE_FINGER_STRETCH_MCP.value]
                v_spread = sample_values[WachFormat.MIDDLE_FINGER_SPREAD.value]
                stretch_value_degree = cnstr.get_stretch_finger_mcp_rest_constraint_degree(v_stretch)
                spread_value_degree = cnstr.get_spread_finger_constraint_degree(v_spread)
                rot_eul = mathutils.Euler(
                    (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            elif pose_bone_index == 2:  # Middle PIP
                v_stretch = sample_values[WachFormat.MIDDLE_FINGER_STRETCH_PIP.value]
                stretch_value_degree = cnstr.get_stretch_finger_pip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            else:  # Middle DIP
                v_stretch = sample_values[WachFormat.MIDDLE_FINGER_STRETCH_DIP.value]
                stretch_value_degree = cnstr.get_stretch_finger_dip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

        # Ring finger
        elif finger_name == 'ring':
            if pose_bone_index == 1:  # Ring MCP
                v_stretch = sample_values[WachFormat.RING_FINGER_STRETCH_MCP.value]
                v_spread = sample_values[WachFormat.RING_FINGER_SPREAD.value]
                stretch_value_degree = cnstr.get_stretch_finger_mcp_rest_constraint_degree(v_stretch)
                spread_value_degree = cnstr.get_spread_finger_constraint_degree(v_spread)
                rot_eul = mathutils.Euler(
                    (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            elif pose_bone_index == 2:  # Ring PIP
                v_stretch = sample_values[WachFormat.RING_FINGER_STRETCH_PIP.value]
                stretch_value_degree = cnstr.get_stretch_finger_pip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            else:  # Ring DIP
                v_stretch = sample_values[WachFormat.RING_FINGER_STRETCH_DIP.value]
                stretch_value_degree = cnstr.get_stretch_finger_dip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

        # Pinky
        else:
            if pose_bone_index == 1:  # Pinky MCP
                v_stretch = sample_values[WachFormat.PINKY_STRETCH_MCP.value]
                v_spread = sample_values[WachFormat.PINKY_SPREAD.value]
                stretch_value_degree = cnstr.get_stretch_finger_mcp_rest_constraint_degree(v_stretch)
                spread_value_degree = cnstr.get_spread_finger_constraint_degree(v_spread)
                rot_eul = mathutils.Euler(
                    (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            elif pose_bone_index == 2:  # Pinky PIP
                v_stretch = sample_values[WachFormat.PINKY_STRETCH_PIP.value]
                stretch_value_degree = cnstr.get_stretch_finger_pip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            else:  # Pinky DIP
                v_stretch = sample_values[WachFormat.PINKY_STRETCH_DIP.value]
                stretch_value_degree = cnstr.get_stretch_finger_dip_constraint_degree(v_stretch)
                rot_eul = mathutils.Euler(
                    (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                pose_bone.rotation_quaternion = rot_eul.to_quaternion()


# Export result as different file types
if EXPORT_FILE_TYPE == "stl":
    bpy.ops.export_mesh.stl(filepath=STL_FILE_PATH)  # STL file
elif EXPORT_FILE_TYPE == "blend":
    bpy.ops.wm.save_mainfile(filepath=BLEND_FILE_PATH)  # blend file
elif EXPORT_FILE_TYPE == "obj":
    bpy.ops.export_scene.obj(filepath=OBJ_FILE_PATH)  # obj file

# Render and export PNG
if EXPORT_PNG:  # Set camera and light positions when exporting as png
    # Camera
    camera_obj = bpy.data.objects['Camera']
    bpy.context.view_layer.objects.active = camera_obj
    bpy.ops.object.mode_set(mode='OBJECT')
    c = bpy.data.cameras['Camera']
    camera_distance = -0.7
    camera_obj.location = mathutils.Vector((0.09, -0.012574, camera_distance))
    camera_obj.rotation_euler = mathutils.Euler((radians(180.155), radians(0.448426), radians(90.0183)), 'XYZ')

    # Light
    light_obj = bpy.data.objects['Light']
    bpy.context.view_layer.objects.active = light_obj
    bpy.ops.object.mode_set(mode='OBJECT')
    light_distance = -5.5
    light_obj.location = mathutils.Vector((0.091267, -0.002574, light_distance))
    light_obj.rotation_euler = mathutils.Euler((radians(180.155), radians(0.448426), radians(90.0183)), 'XYZ')

    # Hand Model
    obj = bpy.data.objects['Armature']
    bpy.context.view_layer.objects.active = obj
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = EXPORT_PNG_PATH
    bpy.ops.render.render(write_still=True)
