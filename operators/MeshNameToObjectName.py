import bpy

class MeshNameToObjectName(bpy.types.Operator):
    bl_idname = "object.mesh_name_to_object_name"
    bl_label = "Mesh name to object name"
    bl_description = "Replaces object name witn mesh_name_XX"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        modules_coll = bpy.data.collections.get("Modules") or bpy.data.collections.new("Modules")
        if "Modules" not in context.scene.collection.children:
            bpy.context.scene.collection.children.link(modules_coll)
        
        modules_obj = set(modules_coll.objects)
        
        # Собираем объекты по имени их Object data, сохраняя порядок появления
        groups = {}
        for obj in context.selected_objects:
            if obj.data is None:
                continue
            name = obj.data.name
            groups.setdefault(name, []).append(obj)

        # Временные имена, чтобы избежать конфликтов при переименовании
        for i, obj in enumerate( context.selected_objects):
            obj.name = f"__tmp_rename_{i}__"

        # Финальные имена в порядке появления Object data
        for data_name, objs in groups.items():
            pad = max(2, len(str(len(objs))))
            for i, obj in enumerate(objs, start=1):
                if obj in modules_obj:
                    obj.name = f"{data_name}"
                else:
                    obj.name = f"{data_name}_{str(i).zfill(pad)}"
                
        
        return {"FINISHED"}
