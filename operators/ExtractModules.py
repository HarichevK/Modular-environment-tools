import bpy

class ExtractModules(bpy.types.Operator):
    bl_idname = "object.extract_modules"
    bl_label = "Extract modules"
    bl_description = "Extract unique modules from selected objects and add it to collection Modules"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
    
  
        modules_coll = bpy.data.collections.get("Modules") or bpy.data.collections.new("Modules")
        if "Modules" not in context.scene.collection.children:
            bpy.context.scene.collection.children.link(modules_coll)
             
        selected_mesh_data = {obj.data for obj in context.selected_objects if obj.type == 'MESH'}
                
        existing_modules_data = {obj.data for obj in modules_coll.objects if obj.type == 'MESH'}
        
        new_modules = {data for data in selected_mesh_data if data not in existing_modules_data}

        for mesh_data in new_modules:
            obj = bpy.data.objects.new(f"{mesh_data.name}", mesh_data)
            modules_coll.objects.link(obj)
            obj.location = (0, 0, 0)
            
        if new_modules:
            self.report({"INFO"}, message = f"Extracted {len(new_modules)} modules")
        else:
             self.report({"INFO"}, message = "No meshes selected or modules already in 'Modules' Collection")
        
        return {"FINISHED"}
