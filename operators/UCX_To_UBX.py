import bpy

class UBC_To_UBX(bpy.types.Operator):
    bl_idname = "object.ucx_to_ubx"
    bl_label = "UCX->UBX"
    bl_description = "Changes UCX prefix to UBX prefix"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        for obj in context.selected_objects:
            if 'UCX' in obj.name:
                obj.name = obj.name.replace('UCX', 'UBX')
        
        return {"FINISHED"}
