import bpy
import math
from mathutils import Matrix

bl_info = {
    "name": "Rotate Them Bones",
    "author": "Peter Riel",
    "version": (0, 1),
    "blender": (4, 0, 0),
    "description": "Rotates each bone 90 degrees in an armature around the X axis",
    "category": "Object",
}

# List of bones to exclude from reconnection
excluded_bones = [
    "Wrist_L", "Thumb_Metacarpal_L", "Index_Metacarpal_L", 
    "Middle_Metacarpal_L", "Ring_Metacarpal_L", "Little_Metacarpal_L", "Palm_L",
    "Wrist_R", "Thumb_Metacarpal_R", "Index_Metacarpal_R", 
    "Middle_Metacarpal_R", "Ring_Metacarpal_R", "Little_Metacarpal_R", "Palm_R"
]

original_positions = {}

bone_roll_values = {}

# Function to store bone roll values
def store_bone_rolls(armature_obj):
    global bone_roll_values
    bone_roll_values = {}
    if armature_obj.type == 'ARMATURE':
        bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit Mode
        for bone in armature_obj.data.edit_bones:
            bone_roll_values[bone.name] = bone.roll
        bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to Object Mode
    else:
        print("The provided object is not an armature.")

def store_original_positions(selected_obj):
    global original_positions
    if selected_obj.type == 'ARMATURE':
        # Ensure we are in Edit Mode to access edit_bones
        bpy.ops.object.mode_set(mode='EDIT')
        armature_data = selected_obj.data
        # Store head, tail, and roll for each bone
        original_positions = {bone.name: (bone.head.copy(), bone.tail.copy(), bone.roll) for bone in armature_data.edit_bones}
        # Return to Object Mode after storing positions and rolls
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("The provided object is not an armature.")

# Un-Connect all the bones
def disconnect_bones(selected_obj):
        # Store the original bone positions
        store_original_positions(selected_obj)
        bpy.ops.object.mode_set(mode='EDIT')
        for bone in selected_obj.data.edit_bones:
            # Disconnect the bone from its parent
            bone.use_connect = False

# Rotate functions
def rotate_bones(selected_obj):
    # Store the original bone positions
    # store_original_positions(selected_obj)

    # Ensure Blender is in Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Get the selected object (should be an armature)
    selected_obj = bpy.context.active_object

    # Check if the selected object is an armature
    if selected_obj and selected_obj.type == 'ARMATURE':
        # Switch to Edit Mode to edit bones
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Define a 90-degree rotation around the X-axis
        rotation_angle = math.radians(90)
        rotation_axis = 'X'
        for bone in selected_obj.data.edit_bones:
            # Disconnect the bone from its parent
            bone.use_connect = False

        # Iterate through all bones in the armature
        for bone in selected_obj.data.edit_bones:
            # Calculate the rotation matrix
            if rotation_axis == 'X':
                rotation_matrix = Matrix.Rotation(rotation_angle, 4, bone.x_axis)
            elif rotation_axis == 'Y':
                rotation_matrix = Matrix.Rotation(rotation_angle, 4, bone.y_axis)
            else: # rotation_axis == 'Z'
                rotation_matrix = Matrix.Rotation(rotation_angle, 4, bone.z_axis)
            
            # Apply the rotation to the bone's tail
            bone.tail = bone.head + rotation_matrix @ (bone.tail - bone.head)

        for bone in selected_obj.data.edit_bones:
            if bone.name in bone_roll_values:
                bone.roll = bone_roll_values[bone.name]

        # Switch back to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

    else:
        print("Selected object is not an armature or no object is selected.")


def rotate_bones_back(selected_obj):
    global original_positions
    if selected_obj and selected_obj.type == 'ARMATURE':
        # Ensure we are in Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        for bone in selected_obj.data.edit_bones:
            # Restore original position and roll
            if bone.name in original_positions:
                orig_head, orig_tail, orig_roll = original_positions[bone.name]
                bone.head = orig_head
                bone.tail = orig_tail
                bone.roll = orig_roll

            # Reconnect the bone unless it's an excluded bone
            if bone.name not in excluded_bones:
                bone.use_connect = True

        # Return to Object Mode after operation
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Selected object is not an armature or no object is selected.")


# Define the operator class for disconnecting bones
class DisconnectBonesOperator(bpy.types.Operator):
    """Disconnect Bones"""
    bl_idname = "object.disconnect_bones"
    bl_label = "2. Disconnect Bones"

    def execute(self, context):
        disconnect_bones(context.active_object)
        return {'FINISHED'}

# Define the operator class for storing rolls
class StoreBoneRollsOperator(bpy.types.Operator):
    """Store Bone Rolls"""
    bl_idname = "object.store_bone_rolls"
    bl_label = "4. Store Bone Roll angles"

    def execute(self, context):
        store_bone_rolls(context.active_object)
        return {'FINISHED'}
    
# Define the operator class for rotating bones
class RotateBonesOperator(bpy.types.Operator):
    """Rotate Bones 90 degrees around the X-axis"""
    bl_idname = "object.rotate_bones"
    bl_label = "5. Rotate"

    def execute(self, context):
        rotate_bones(context.active_object)
        return {'FINISHED'}

# Define the operator class for setting bones back to original
class RotateBonesBackOperator(bpy.types.Operator):
    """Rotate Bones -90 degrees around the X-axis"""
    bl_idname = "object.rotate_bones_back"
    bl_label = "6. Rotate back"

    def execute(self, context):
        rotate_bones_back(context.active_object)
        return {'FINISHED'}

# Define the panel class
class RotateBonesPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Rotate Them Bones!"
    bl_idname = "OBJECT_PT_rotate_bones"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.label(text="1. Select the Armature")
        layout.operator(DisconnectBonesOperator.bl_idname)
        layout.label(text="3. Manually rotate all bones")
        layout.label(text="(a, r, x, 90 enter)")
        layout.operator(StoreBoneRollsOperator.bl_idname)
        layout.label(text="After steps 1-4, you can")
        layout.label(text="flip between step 5 & 6.")
        layout.operator(RotateBonesOperator.bl_idname)
        layout.operator(RotateBonesBackOperator.bl_idname)

# Register and unregister functions
def register():
    bpy.utils.register_class(DisconnectBonesOperator)
    bpy.utils.register_class(StoreBoneRollsOperator)
    bpy.utils.register_class(RotateBonesOperator)
    bpy.utils.register_class(RotateBonesBackOperator)
    bpy.utils.register_class(RotateBonesPanel)

def unregister():
    bpy.utils.unregister_class(DisconnectBonesOperator)
    bpy.utils.unregister_class(StoreBoneRollsOperator)
    bpy.utils.unregister_class(RotateBonesOperator)
    bpy.utils.unregister_class(RotateBonesBackOperator)
    bpy.utils.unregister_class(RotateBonesPanel)

if __name__ == "__main__":
    register()
