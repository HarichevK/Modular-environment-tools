import bpy
import bmesh

class SelectIncorrectCollisionGeometry(bpy.types.Operator):
    
    bl_idname = "object.select_incorrect_collision_geometry"
    bl_label = "Select incorrect collision geometry from selected"
    bl_description = "Selecte incorrect collision geometry from selected objects"
    bl_options = {"REGISTER"}

    EPSILON = 1e-2

    def select_connected_verts(self, vert):
        verts = []
        stack = [vert]
        visited = set()

        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            verts.append(v)

            for edge in v.link_edges:
                other = edge.other_vert(v)
                if other not in visited:
                    stack.append(other)

        return verts

    def make_islands(self, bm):
        unvisited = set(bm.verts)
        islands = []

        while unvisited:
            start_vert = next(iter(unvisited))
            island = self.select_connected_verts(start_vert)
            islands.append(island)
            unvisited.difference_update(island)

        return islands
    

    def IsIslandNonManifold(self, island):
        for v in island:
            for e in v.link_edges:
                if not e.is_manifold and not e.is_boundary and not e.is_wire:
                    return True
            if not v.is_manifold and not v.is_boundary:
                return True
        return False


    def IsIslandFlat(self, island):
        if len(island) < 3:
            return True

        p0 = island[0].co
        p1 = None
        p2 = None

        for v in island[1:]:
            if (v.co - p0).length > 1e-12:
                p1 = v.co
                break
        if p1 is None:
            return True

        dir1 = p1 - p0
        normal = None

        for v in island[1:]:
            if v.co == p1:
                continue
            cross = (v.co - p0).cross(dir1)
            if cross.length > 1e-12:
                p2 = v.co
                normal = cross.normalized()
                break

        if normal is None:
            return True

        for v in island:
            dist = abs((v.co - p0).dot(normal))
            if dist > self.EPSILON:
                return False

        return True
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        if not selected_objects:
            return

        for obj in selected_objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.reveal()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')

        for obj in selected_objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')

            bm = bmesh.from_edit_mesh(obj.data)
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()

            islands = self.make_islands(bm)

            verts_to_select = set()
            for island in islands:
                if self.IsIslandNonManifold(island):
                    verts_to_select.update(island)
                    continue
                if self.IsIslandFlat(island):
                    verts_to_select.update(island)
                    continue

            for v in verts_to_select:
                v.select = True

            bm.select_flush(True)
            bmesh.update_edit_mesh(obj.data)

            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {"FINISHED"}
