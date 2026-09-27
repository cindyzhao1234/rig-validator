import bpy


class RIGVALIDATOR_PT_main_panel(bpy.types.Panel):
    bl_label = "Rig Validator"
    bl_idname = "RIGVALIDATOR_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig Validator"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Rig Validator")
        layout.label(text="Select an armature to begin.")


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