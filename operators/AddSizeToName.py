import bpy

class AddSizeToNameOperator(bpy.types.Operator):
    bl_idname = "object.add_size_to_name"
    bl_label = "Add Size to Name"

    def execute(self, context):
        
        props = context.scene.object_scale_naming
        
        return {"FINISHED"}

