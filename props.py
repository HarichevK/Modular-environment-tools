import bpy

class ObjectScaleNamingProperties(bpy.types.PropertyGroup):
        
        use_x_size: bpy.props.BoolProperty(name = "X", default=True)
        
        use_y_size: bpy.props.BoolProperty(name = "Y", default=False)
        
        use_z_size: bpy.props.BoolProperty(name = "Z", default=True)
        
        units: bpy.props.EnumProperty(
            name="Units", 
            items=[
                ('cm', "centimeters", ""), 
                ('m', "meters", "")
                ]
            )
                                        
                                        
        rounding: bpy.props.IntProperty(name="rounding", default=1)
        
    
class AutoUnwrapProperties(bpy.types.PropertyGroup):
    
    edge_angle: bpy.props.IntProperty(
        name = "Sharp angle", 
        default=40)
    
    texel_density: bpy.props.FloatProperty(
        name = "Texel density",
        default=1024)