import bpy

class SelectLocalMeshes(bpy.types.Operator):
    bl_idname = "object.select_local_meshes"
    bl_label = "Select local meshes"
    bl_description = "Selects only editable meshes from selected"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        result = [obj for obj in context.selected_objects if  obj.type == "MESH" and obj.is_editable and obj.data.is_editable]
        
        bpy.ops.object.select_all(action = 'DESELECT')
        
        if not result:
            self.report({'WARNING'}, message="Local meshes not selected")
            return {"FINISHED"}
        
        for obj in result:
            obj.select_set(True);
            
        context.view_layer.objects.active = result[0]
            
        
                
        return {"FINISHED"}
