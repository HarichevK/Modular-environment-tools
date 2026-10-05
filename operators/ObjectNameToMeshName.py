import bpy

class ObjectNameToMeshName(bpy.types.Operator):
    bl_idname = "object.object_name_to_mesh_name"
    bl_label = "Object Name -> Data Name"
    bl_description = "Copy object name do data name"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        objects = [obj for obj in context.selected_objects if obj.type == "MESH"]
    
        for obj in objects:
            if not obj.is_editable or not obj.data.is_editable:
                continue

            obj.data.name = obj.name
        return {"FINISHED"}
