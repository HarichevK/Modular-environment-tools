import bpy

class ObjectScaleNamingProperties(bpy.types.PropertyGroup):
        
        use_x_size: bpy.props.BoolProperty(name = "X", default=True)
        
        use_Y_size: bpy.props.BoolProperty(name = "Y", default=False)
        
        use_Z_size: bpy.props.BoolProperty(name = "Z", default=True)
        
        my_enum: bpy.props.EnumProperty(
            name="Units", 
            items=[
                ('cm', "centimeters", ""), 
                ('m', "meters", "")
                ]
            )
                                        
                                        
        rounding: bpy.props.IntProperty(name="rounding", default=1)
        
    