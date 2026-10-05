import bpy
import hashlib


def mesh_signature(mesh, precision=5):
    """Строит хэш-подпись геометрии меша (вершины, рёбра, полигоны)."""
    fmt = f".{precision}f"
    h = hashlib.md5()

    # Вершины
    for v in mesh.vertices:
        h.update((f"{v.co.x:{fmt}},{v.co.y:{fmt}},{v.co.z:{fmt}}|").encode())
    h.update(b";")

    # Рёбра
    for e in mesh.edges:
        h.update(f"{e.vertices[0]},{e.vertices[1]}|".encode())
    h.update(b";")

    # Полигоны
    for p in mesh.polygons:
        h.update((",".join(str(i) for i in p.vertices) + "|").encode())

    return h.hexdigest()


class OBJECT_OT_select_duplicates(bpy.types.Operator):
    bl_idname = "object.select_duplicates"
    bl_label = "Select Duplicate Objects"
    bl_description = (
        "Выделяет объекты среди выбранных, чья геометрия меша полностью "
        "совпадает (вершины, рёбра, грани)"
    )
    bl_options = {'REGISTER', 'UNDO'}

    precision: bpy.props.IntProperty(
        name="Precision",
        description="Количество знаков после запятой при сравнении координат вершин",
        default=5,
        min=0,
        max=9,
    )

    keep_one: bpy.props.BoolProperty(
        name="Keep One Per Group",
        description="Оставить по одному объекту в каждой группе невыделенным",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return (
            context.mode == 'OBJECT'
            and len([o for o in context.selected_objects if o.type == 'MESH']) > 1
        )

    def execute(self, context):
        selected = [o for o in context.selected_objects if o.type == 'MESH']

        # Группировка по подписи геометрии
        groups = {}
        for obj in selected:
            try:
                sig = mesh_signature(obj.data, self.precision)
            except Exception as ex:
                self.report({'WARNING'}, f"Error when processing: {obj.name}: {ex}")
                continue
            groups.setdefault(sig, []).append(obj)

        dup_groups = [g for g in groups.values() if len(g) > 1]

        if not dup_groups:
            self.report({'INFO'}, "Duplicates not found")
            return {'CANCELLED'}

        to_select = set()
        for group in dup_groups:
            # Оставляем первый объект невыделенным, если нужно
            items = group[1:] if self.keep_one else group
            for obj in items:
                to_select.add(obj.name)

        # Сброс выделения и выделение дубликатов
        for obj in selected:
            obj.select_set(False)
        for name in to_select:
            obj = bpy.data.objects.get(name)
            if obj:
                obj.select_set(True)
        if context.view_layer.objects.active and context.view_layer.objects.active.name in to_select:
            pass
        elif to_select:
            context.view_layer.objects.active = bpy.data.objects[next(iter(to_select))]

        total = sum(len(g) for g in dup_groups)
        self.report(
            {'INFO'},
            f"Найдено {len(dup_groups)} групп(ы) дубликатов, "
            f"всего объектов: {total}, выделено: {len(to_select)}"
        )
        return {'FINISHED'}
