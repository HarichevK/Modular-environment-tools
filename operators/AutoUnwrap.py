import bpy

class AutoUnwrap(bpy.types.Operator):
    bl_idname = "objects.auto_unwrap"
    bl_label = "Auto unwrap"
    bl_description = "Uses UnwrapConformal, ZenUV texel density and world orient"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.reveal()

        bpy.ops.mesh.select_all(action='DESELECT')

        props = context.scene.auto_unwrap_props


        bpy.ops.mesh.edges_select_sharp(sharpness=props.edge_angle)
        bpy.ops.mesh.mark_seam(clear=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap(method='CONFORMAL', fill_holes=True, correct_aspect=False, use_subsurf_data=False, margin=0.001, no_flip=False, iterations=10, use_weights=False, weight_group="uv_importance", weight_factor=1)
        bpy.ops.uv.zenuv_world_orient(further_orient=False)
        
        context.scene.zen_uv.td_props.prp_current_td = props.texel_density
        bpy.ops.uv.zenuv_set_texel_density(global_mode=True)
        
        bpy.ops.object.editmode_toggle()
            
        
        return {"FINISHED"}
