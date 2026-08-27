import bpy
import os


island_convex_hull_node_group_name = "IslandConvexHull"

island_convex_hull_node_group = None


class MakeCollisionDraftsForSelected(bpy.types.Operator):
    bl_idname = "object.make_collision_draft_for_selected"
    bl_label = "Make collision draft for selected objects"
    bl_description = "Duplicates objects and applies modifiers stack"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        global island_convex_hull_node_group
        global island_convex_hull_node_group_name
        
        if island_convex_hull_node_group is None:
        
            blend_filepath = os.path.join(os.path.dirname(__file__), "..", "assets", "ModularEnvironmentTools.blend")
            
            with bpy.data.libraries.load(blend_filepath, link=False) as (data_from, data_to):
                if island_convex_hull_node_group_name in data_from.node_groups:
                    data_to.node_groups = [island_convex_hull_node_group_name]
                else:
                    print(f"Node group '{island_convex_hull_node_group_name}' not found in {blend_filepath}")
                    return None
                
            
            if island_convex_hull_node_group_name in bpy.data.node_groups:
                island_convex_hull_node_group = bpy.data.node_groups[island_convex_hull_node_group_name]
                island_convex_hull_node_group.use_fake_user = True
            else:
                print(f"Error: node tree {island_convex_hull_node_group_name} could not be loaded")
                return None
        
        # Получаем/создаём материал Collision
        collision_mat = bpy.data.materials.get("Collision")
        if collision_mat is None:
            collision_mat = bpy.data.materials.new("Collision")

        collision_objects = []

        selected_objects = context.selected_objects

        for obj in selected_objects:
            if obj.type != 'MESH':
                print(f"Пропущен '{obj.name}': это не mesh-объект")
                continue

            # Запоминаем мировую матрицу оригинала
            world_matrix = obj.matrix_world.copy()

            # Создаём копию объекта
            obj_collision = obj.copy()
            # Делаем данные меша уникальными, чтобы не затронуть оригинал
            obj_collision.data = obj.data.copy()

            obj_collision.name = f"UCX_{obj.name}"

            # Линкуем в те же коллекции, что и оригинал
            collections = obj.users_collection or [bpy.context.collection]
            for col in collections:
                col.objects.link(obj_collision)

            # Set parent to Object (KeepTransform)
            obj_collision.parent = obj
            obj_collision.matrix_world = world_matrix

            # Удаляем все материалы
            if hasattr(obj_collision.data, "materials"):
                obj_collision.data.materials.clear()

            # Очищаем все материалы на уровне данных меша
            obj_collision.data.materials.clear()
            # Добавляем один материал Collision
            obj_collision.data.materials.append(collision_mat)

            # Добавляем GeometryNodes модификатор
            geo_mod = obj_collision.modifiers.new("IslandConvexHull", type='NODES')
            geo_mod.node_group = island_convex_hull_node_group
            
            dec_mod = obj_collision.modifiers.new("Decimate", type='DECIMATE')
            dec_mod.decimate_type = 'DISSOLVE'
            dec_mod.angle_limit = 0.0349066

            # Добавляем Displace модификатор
            disp_mod = obj_collision.modifiers.new("Displace", type='DISPLACE')
            disp_mod.strength = -0.01
            
            # Добавляем GeometryNodes модификатор
            geo_mod2 = obj_collision.modifiers.new("IslandConvexHull2", type='NODES')
            geo_mod2.node_group = island_convex_hull_node_group
            
            
            collision_objects.append(obj_collision)
            print(f"Создан: {obj_collision.name}")
        return {"FINISHED"}
