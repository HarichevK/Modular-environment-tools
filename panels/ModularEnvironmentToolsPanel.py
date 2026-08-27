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
        col.operator("object.count_unique_object_data", text = "Count unique modules from selected")

        layout.label(text =  "Collision tools")
        
        col2 = layout.column(align=True)
        
        col2.operator("object.make_collision_draft_for_selected", text="Make collision draft for selected objects")
        col2.operator("object.select_incorrect_collision_geometry", text="Select incorrect collision geometry from selected")
        col2.operator("object.select_collisions_with_box_shape", text = "Selsect collison with box shape")
        
        layout.label(text =  "Naming tools")
        
        col3 = layout.column(align=True)
        
        props = context.scene.object_scale_naming
        
        col3.operator("object.ucx_to_ubx", text = "UCX -> UBX")
        col3.operator("object.ubx_to_ucx", text = "UBX -> UCX")
        
        layout.prop(props, "use_x_size")
        layout.prop(props, "use_Y_size")
        layout.prop(props, "use_Z_size")

        layout.prop(props, "my_enum")

        layout.prop(props, "rounding")
        
        