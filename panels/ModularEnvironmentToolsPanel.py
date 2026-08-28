import bpy

class ModularEnironmentToolsPanel(bpy.types.Panel):
    bl_idname = "panel.modular_environment_tools"
    bl_label = "Modular environment tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        
        if not hasattr(context.scene, "object_scale_naming"):
            layout.label(text="Property not registered – reload addon", icon='ERROR')
            return
        
        layout.label(text = "Modular Tools")
        
        col = layout.column(align=True)
        
        col.operator("object.select_unprocessed_modules", text="Select unprocessed modules")
        col.operator("object.select_unused_modules", text="Select unused modules")
        col.operator("object.count_unique_object_data", text = "Count unique modules")

        layout.label(text =  "Collision tools")
        
        col2 = layout.column(align=True)
        
        col2.operator("object.make_collision_draft_for_selected", text="Make collision draft")
        col2.operator("object.select_incorrect_collision_geometry", text="Select incorrect collision")
        col2.operator("object.select_collisions_with_box_shape", text = "Selsect box shaped collison")
        
        layout.label(text =  "Naming tools")
        
        col3 = layout.column(align=True)
        
        props = context.scene.object_scale_naming
        
        col3.operator("object.ucx_to_ubx", text = "UCX -> UBX")
        col3.operator("object.ubx_to_ucx", text = "UBX -> UCX")
        
        col4 = layout.column(align=True)
        
        col4.label(text="Add dimensions to name")
        
        
        col4row1 = col4.row(align=True)
        col4row1.prop(props, "use_x_size", toggle=True)
        col4row1.prop(props, "use_y_size", toggle=True)
        col4row1.prop(props, "use_z_size", toggle=True)
        
        col4.prop(props, "units")
        
        col4.prop(props, "rounding")
        
        col4.operator("object.add_size_to_name", text="Add size to names")
        
        layout.label(text="Transformation tools")
        
        col5 = layout.column(align=True)
        col5.operator("object.batch_apply_transform", text="Apply transform for modules")
        
        layout.label(text="UV tools")
        
        if not hasattr(context.scene, "auto_unwrap_props"):
            layout.label(text="Property not registered – reload addon", icon='ERROR')
            return
        
        props_unwrap = context.scene.auto_unwrap_props
        
        col6 = layout.column(align=True)
        
        col6.prop(props_unwrap, "edge_angle")
        col6.prop(props_unwrap, "texel_density")
        
        col6.operator("objects.auto_unwrap", text="Unwrap selected")
        
        
        