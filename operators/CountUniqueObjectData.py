import bpy

class CountUniqueObjectData(bpy.types.Operator):
    bl_idname = "object.count_unique_object_data"
    bl_label = "Count unique object data"
    bl_description = "Counts unique object datas from selected objects"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        selected_objects = context.selected_objects
    
        unique_datas = {object.data for object in selected_objects if object.type == "MESH"}
    
        if not unique_datas:
            self.report({"WARNING"}, message = "no selected meshes")
            return {"CANCELLED"}
        
        self.report({"INFO"}, message = f"Unique modules in selected: {len(unique_datas)}")
        
        return {"FINISHED"}
