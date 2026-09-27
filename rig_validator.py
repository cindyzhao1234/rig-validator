import bpy


    
def isArmature(obj):
    return obj and obj.type == 'ARMATURE'

def boneCount(obj) -> int:
    bone_count = len(obj.data.bones)
    return bone_count
    
def printBones(bones):
    for bone in bones:
        if bone.parent:
            print(f"{bone.name}, parent: {bone.parent.name}")
            if usesDeform(bone):
                print(f"{bone.name} uses deform\n")
            else:
                print(f"{bone.name} does not use deform\n")
        else:
            print(bone.name)
            if usesDeform(bone):
                print(f"{bone.name} uses deform\n")

def usesDeform(bone):
    return bone.use_deform

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
            bone_count = boneCount(obj)
            layout.label(text=f"There are {bone_count} bones")
            printBones(obj.data.bones)
        else:
            layout.label(text="Select valid armature")


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