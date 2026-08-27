import bpy

class AddSizeToNameOperator(bpy.types.Operator):
    bl_idname = "object.add_size_to_name"
    bl_label = "Add Size to Name"

    def execute(self, context):
        if not hasattr(context.scene, "object_scale_naming"):
            return
                
        props = context.scene.object_scale_naming
        
        objects = [obj for obj in context.selected_objects if obj.type == "MESH"]
        
        
        divider = int(100)
        
        if props.units == "cm":
            divider = 1
        elif props.units == "m":
            divider = 100
            
        rounding = int(props.rounding)
        
        for obj in objects:
            
            result = ""
            
            Xcm = int(round(obj.dimensions.x * 100)) 
            Ycm = int(round(obj.dimensions.y * 100))
            Zcm = int(round(obj.dimensions.z * 100))
            
            if (props.use_x_size):
                result += f"_{int(round(Xcm, rounding) / divider)}"
        
            if (props.use_z_size):
                result += f"_{int(round(Zcm, rounding) / divider)}"
        
            if (props.use_y_size):
                result += f"_{int(round(Ycm, rounding) / divider)}"
                
            obj.name = obj.name + result;
        
        return {"FINISHED"}

