import bpy

class SelectUnusedModules(bpy.types.Operator):
    bl_idname = "object.select_unused_modules"
    bl_label = "Select Unused Modules"
    bl_description = "Select object from collection Modules that has only one ObjectData Users"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        modules_coll = bpy.data.collections.get("Modules")
        if not modules_coll:
            return {"FINISHED"}
    
        single_user_data_objects = [obj for obj in modules_coll.objects if obj.data is not None and obj.data.users == 1]
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in single_user_data_objects:
            obj.select_set(True)
        
        if single_user_data_objects:
            context.view_layer.objects.active = single_user_data_objects[0]
        
        return {"FINISHED"}
