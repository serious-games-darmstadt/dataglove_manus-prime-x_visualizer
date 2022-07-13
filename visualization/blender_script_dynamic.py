import bpy
import os
from math import radians
import mathutils
import visualization.constraints as cnstr


"""
    GLOBAL VARIABLES
"""
# These variables will be set in viz.py
EXPORT = None
EXPORT_FILE_TYPE = ''
BLEND_PATH_STR = ''
LABEL = ''
HAND = ''
gesture_data = {}

# Input Paths
FBX_HAND_LEFT_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 R"resources/Manus-Hand-Left.fbx"))
FBX_HAND_RIGHT_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 R"resources/Manus-Hand-Right.fbx"))

# Output Paths
BLEND_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), BLEND_PATH_STR))

# Global variables
WRIST_NAME = "hand"  # wrist object name in blender
HAND_NAME = "SK_Hand"  # hand object name in blender
FINGER_NAMES = ["thumb", "index", "middle", "ring", "pinky"]  # finger object names in blender
QUAT_WRIST_IDX_PROCESSED_DATA_START = 0  # Indices for w,x,y,z quat values in the processed data format in 'rotations'
QUAT_WRIST_IDX_PROCESSED_DATA_END = 3
QUAT_HAND_IDX_PROCESSED_DATA_START = 4
QUAT_HAND_IDX_PROCESSED_DATA_END = 7


"""
    HELPER FUNCTION
"""
def create_keyframe_for_data_sample(idx, data_sample):
    rotation_data = data_sample['rotations']
    spread_data = data_sample['spread']
    stretch_data = data_sample['stretch']

    # Rotate wrist and hand with rotation quaternions (for hand orientation)
    for name in [WRIST_NAME, HAND_NAME]:
        pose_bone_name = f"{name}_{HAND[0].lower()}" if name == WRIST_NAME else HAND_NAME
        start_idx = QUAT_WRIST_IDX_PROCESSED_DATA_START if name == WRIST_NAME else QUAT_HAND_IDX_PROCESSED_DATA_START
        end_idx = QUAT_WRIST_IDX_PROCESSED_DATA_END if name == WRIST_NAME else QUAT_HAND_IDX_PROCESSED_DATA_END
        quaternion_raw = tuple(rotation_data[start_idx:end_idx+1])
        wrist_pose_bone = obj.pose.bones[pose_bone_name]
        wrist_pose_bone.rotation_mode = 'QUATERNION'

        wrist_pose_bone.rotation_quaternion = mathutils.Quaternion(quaternion_raw)  # (w, x, y, z)
        wrist_pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=idx + 1)

    # Traverse all fingers and apply joint value rotations to all joints
    for finger_name_idx, finger_name in enumerate(FINGER_NAMES):
        spread_value = spread_data[finger_name_idx]

        for joint_idx in range(3):  # model indices (1,2,3): cmc, mcp, ip (thumb) or mcp, pip, dip (finger)
            # Get blender pose bone object
            blender_joint_index = joint_idx + 1
            pose_bone_name = f"{finger_name}_0{blender_joint_index}_{HAND[0].lower()}"
            pose_bone = obj.pose.bones[pose_bone_name]
            pose_bone.rotation_mode = 'QUATERNION'

            # Extract stretch value for specific joint of finger
            stretch_value = stretch_data[finger_name_idx][joint_idx]

            # THUMB
            if finger_name == "thumb":
                if blender_joint_index == 1:  # Thumb CMC
                    # Convert normalized sample values to degree
                    stretch_value_degree = cnstr.get_stretch_thumb_cmc_constraint_degree(stretch_value)
                    spread_value_degree = cnstr.get_spread_thumb_cmc_constraint_degree(spread_value)

                    # Apply spread rotation for thumb cmc
                    # Also switch signs for values except spread (CMC) because of blender ...
                    rot_eul = mathutils.Euler(
                        (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                elif blender_joint_index == 2:  # Thumb MCP
                    stretch_value_degree = cnstr.get_stretch_thumb_mcp_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                else:  # Thumb IP
                    stretch_value_degree = cnstr.get_stretch_thumb_ip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            # INDEX
            elif finger_name == "index":
                if blender_joint_index == 1:  # Index MCP
                    stretch_value_degree = cnstr.get_stretch_finger_mcp_rest_constraint_degree(stretch_value)
                    spread_value_degree = cnstr.get_spread_finger_constraint_degree(spread_value)
                    rot_eul = mathutils.Euler(
                        (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                elif blender_joint_index == 2:  # Index PIP
                    stretch_value_degree = cnstr.get_stretch_finger_pip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                else:  # Index DIP
                    stretch_value_degree = cnstr.get_stretch_finger_dip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            # MIDDLE
            elif finger_name == "middle":
                if blender_joint_index == 1:  # Middle MCP
                    stretch_value_degree = cnstr.get_stretch_finger_mcp_rest_constraint_degree(stretch_value)
                    spread_value_degree = cnstr.get_spread_finger_constraint_degree(spread_value)
                    rot_eul = mathutils.Euler(
                        (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                elif blender_joint_index == 2:  # Middle PIP
                    stretch_value_degree = cnstr.get_stretch_finger_pip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                else:  # Middle DIP
                    stretch_value_degree = cnstr.get_stretch_finger_dip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            # RING
            elif finger_name == "ring":
                if blender_joint_index == 1:  # Ring MCP
                    stretch_value_degree = cnstr.get_stretch_finger_mcp_rest_constraint_degree(stretch_value)
                    spread_value_degree = cnstr.get_spread_finger_constraint_degree(spread_value)
                    rot_eul = mathutils.Euler(
                        (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                elif blender_joint_index == 2:  # Ring PIP
                    stretch_value_degree = cnstr.get_stretch_finger_pip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                else:  # Ring DIP
                    stretch_value_degree = cnstr.get_stretch_finger_dip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            # PINKY
            else:
                if blender_joint_index == 1:  # Pinky MCP
                    stretch_value_degree = cnstr.get_stretch_finger_mcp_rest_constraint_degree(stretch_value)
                    spread_value_degree = cnstr.get_spread_finger_constraint_degree(spread_value)
                    rot_eul = mathutils.Euler(
                        (radians(spread_value_degree), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                elif blender_joint_index == 2:  # Pinky PIP
                    stretch_value_degree = cnstr.get_stretch_finger_pip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

                else:  # Pinky DIP
                    stretch_value_degree = cnstr.get_stretch_finger_dip_constraint_degree(stretch_value)
                    rot_eul = mathutils.Euler(
                        (radians(0.0), radians(0.0), radians(-1 * stretch_value_degree)), 'XYZ')
                    pose_bone.rotation_quaternion = rot_eul.to_quaternion()

            # Add keyframe for animation (each sample one frame)
            pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=idx+1)


"""
    ANIMATION
"""
# Clean scene
while bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[0], do_unlink=True)

# Import FBX for right or left hand
fbx_path = FBX_HAND_LEFT_FILE_PATH if HAND == "Left" else FBX_HAND_RIGHT_FILE_PATH
bpy.ops.import_scene.fbx(filepath=fbx_path, automatic_bone_orientation=True)

# Select Hand Models Armature as Active
obj = bpy.data.objects['Armature']
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='POSE')  # pose mode for changing joint values

# Process start_to_hold (dynamic part of the gesture)
start_to_hold_data = gesture_data['startToHold']
for idx, data_sample in enumerate(start_to_hold_data):
    create_keyframe_for_data_sample(idx, data_sample)

# Process hold_to_end (holding part of the gesture)
hold_to_end_data = gesture_data['holdToEnd']
for idx, data_sample in enumerate(hold_to_end_data):
    create_keyframe_for_data_sample(idx+len(start_to_hold_data), data_sample)


"""
    EXPORT
"""
# Hide the armature bone (so that hand model more visible)
obj.hide_set(True)

# Export result as blend file when flag set
if EXPORT:
    if EXPORT_FILE_TYPE == "blend":
        bpy.ops.wm.save_mainfile(filepath=BLEND_FILE_PATH)
