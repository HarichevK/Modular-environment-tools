import bpy

class BatchApplyTransform(bpy.types.Operator):
    bl_idname = "object.batch_apply_transform"
    bl_label = "Batched apply transform"
    bl_description = "Applies transform to selected objects and all their instances"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        selected_objects = bpy.context.selected_objects.copy()

        for obj in selected_objects:
            bpy.ops.object.select_all(action='DESELECT')
            
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.object.select_linked(type='OBDATA')
            
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        bpy.ops.object.select_all(action='DESELECT')
        
        return {"FINISHED"}
