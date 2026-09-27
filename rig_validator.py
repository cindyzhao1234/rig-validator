import bpy


    
def isArmature(obj):
    return obj and obj.type == 'ARMATURE'

class RIGVALIDATOR_PT_main_panel(bpy.types.Panel):
    bl_label = "Rig Validator"
    bl_idname = "RIGVALIDATOR_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig Validator"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Rig Validator")
        
        obj = bpy.context.active_object

        if isArmature(obj):
            layout.label(text="Valid armature selected")
        else:
            layout.label(text="Please select an armature")
        
        bone_count = len(obj.data.bones)
        layout.label(text=f"There are {bone_count} bones")


classes = (
    RIGVALIDATOR_PT_main_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()