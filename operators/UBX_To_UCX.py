import bpy

class UBX_To_UCX(bpy.types.Operator):
    bl_idname = "object.ubx_to_ucx"
    bl_label = "UBX->UCX"
    bl_description = "Changes UBX prefix to UCX prefix"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        for obj in context.selected_objects:
            if 'UBX' in obj.name:
                obj.name = obj.name.replace('UBX', 'UCX')
        
        return {"FINISHED"}