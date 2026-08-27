import bpy

class SelectUnprocessedModulesOperator(bpy.types.Operator):
    bl_idname = "object.select_unprocessed_modules"
    bl_label = "Select Unprocessed Modules"

    def execute(self, context):
        
        bpy.ops.object.select_all(action='DESELECT')
        
        modules_coll = bpy.data.collections.get("Modules")
        if not modules_coll:
            modules_coll = bpy.data.collections.new(name = "Modules")
            bpy.context.scene.collection.children.link(modules_coll)
        
        module_data = {obj.data for obj in modules_coll.objects if obj.type == 'MESH'}
        
        all_meshes = [obj for obj in bpy.context.scene.objects
                      if obj.type == 'MESH' and obj.visible_get()]
        
        objects_to_select = [obj for obj in all_meshes if obj.data not in module_data]
        
        for obj in objects_to_select:
            obj.select_set(True)
        
        bpy.context.workspace.status_text_set(f"Selected modules: {len(objects_to_select)}")
        
        return {"FINISHED"}