import bpy
import os

NODE_GROUP_NAME = "IslandConvexHull"

ASSET_FILENAME = "ModularEnvironmentTools.blend"

def asset_path():
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "assets", ASSET_FILENAME)
    )

def load_node_group(name=NODE_GROUP_NAME):

    existing = bpy.data.node_groups.get(name)
    if existing is not None:
        return existing

    path = asset_path()
    if not os.path.exists(path):
        return None

    with bpy.data.libraries.load(path, link=False) as (data_from, data_to):
        if name not in data_from.node_groups:
            return None
        data_to.node_groups = [name]

    group = bpy.data.node_groups.get(name)
    if group is not None:
        # Nothing points at it until a modifier does, so it would be dropped
        # on save without this.
        group.use_fake_user = True
    return group

class MakeCollisionDraftsForSelected(bpy.types.Operator):
    bl_idname = "object.make_collision_draft_for_selected"
    bl_label = "Make collision draft for selected objects"
    bl_description = "Duplicates objects and applies modifiers stack"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        collision_mat = bpy.data.materials.get("Collision")
        if collision_mat is None:
            collision_mat = bpy.data.materials.new("Collision")

        collision_objects = []

        selected_objects = context.selected_objects
        
        node_group = load_node_group()

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
            geo_mod.node_group = node_group
            
            dec_mod = obj_collision.modifiers.new("Decimate", type='DECIMATE')
            dec_mod.decimate_type = 'DISSOLVE'
            dec_mod.angle_limit = 0.0349066

            # Добавляем Displace модификатор
            disp_mod = obj_collision.modifiers.new("Displace", type='DISPLACE')
            disp_mod.strength = -0.01
            
            # Добавляем GeometryNodes модификатор
            geo_mod2 = obj_collision.modifiers.new("IslandConvexHull2", type='NODES')
            geo_mod2.node_group = node_group
            
            
            collision_objects.append(obj_collision)
            print(f"Создан: {obj_collision.name}")
        return {"FINISHED"}
