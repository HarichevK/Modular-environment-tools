import bpy

class SelectCollisionsWithBoxShape(bpy.types.Operator):
    bl_idname = "object.select_collisions_with_box_shape"
    bl_label = "Select collisions with box shape"
    bl_description = "Selects geometry with 8 verts in box shape"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        selected_objects = bpy.context.selected_objects

        meshes = [obj for obj in selected_objects if obj.type == "MESH"]
        
        objects_to_select = []
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in meshes:
            depsgraph = bpy.context.evaluated_depsgraph_get()
            obj_eval = obj.evaluated_get(depsgraph)
            mesh_data = obj_eval.to_mesh()
            
            verts = [v.co for v in mesh_data.vertices]
            
            if len(verts) != 8:
                continue

            xs = {round(v.x, 2) for v in verts}
            ys = {round(v.y, 2) for v in verts}
            zs = {round(v.z, 2) for v in verts}

            # Для параллелепипеда должны быть ровно по 2 уникальных значения по каждой оси
            if not (len(xs) == 2 and len(ys) == 2 and len(zs) == 2):
                continue
            
            objects_to_select.append(obj)

            # Освобождаем временную геометрию
            obj_eval.to_mesh_clear()
            
        for obj in objects_to_select:
            obj.select_set(True)
            
        return {"FINISHED"}