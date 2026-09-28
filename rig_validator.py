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

def remove_side(name):
    #Remove .L or .R suffix from a bone name.
    if name.endswith((".L", ".R")):
        return name[:-2]
    return name


def checkSymmetry(bones, layout):
    has_name_symmetry = True
    has_parent_symmetry = True
    has_length_symmetry = True
    has_deform_symmetry = True

    for bone in bones:

        if not bone.name.endswith(".L"):
            continue

        right_name = bone.name[:-2] + ".R"

        #CHECK MATCHING BONES EXIST
        if right_name not in bones:
            print(f"{bone.name} is missing {right_name}")
            has_name_symmetry = False
            continue

        right_bone = bones[right_name]

        print(f"{bone.name} has matching {right_name}")

        #CHECK MATCHING BONES HAVE MATCHING PARENTS
        #Both have parents
        if bone.parent and right_bone.parent:

            left_parent = remove_side(bone.parent.name)
            right_parent = remove_side(right_bone.parent.name)

            if left_parent != right_parent:
                print(
                    f"{bone.name} and {right_name} "
                    f"have different parents"
                )
                has_parent_symmetry = False

        #Only one has a parent
        elif bone.parent or right_bone.parent:
            print(
                f"{bone.name} and {right_name} "
                f"have different parent structures"
            )
            has_parent_symmetry = False


        #CHECK LENGTH OF MATCHING BONES
        if round(bone.length, 5) != round(right_bone.length, 5):
            print(
                f"{bone.name}: {bone.length} | "
                f"{right_name}: {right_bone.length}"
            )
            has_length_symmetry = False
        
        #CHECK IF MATCHING BONES HAVE MATCHING DEFORM SETTINGS
        if bone.use_deform == right_bone.use_deform:
            print(f"{bone.name} and {right_bone.name} have matching deform settings")
        else:
            if bone.use_deform == True and right_bone.use_deform == False:
                print(f"{bone.name} uses deform but {right_bone.name} does not")
            elif bone.use_deform == False and right_bone.use_deform == True:
                print(f"{bone.name} does not use deform but {right_bone.name} uses deform")
            has_deform_symmetry = False


    if has_name_symmetry:
        layout.label(text="✓ Name symmetry")
    else:
        layout.label(text="x Name symmetry")

    if has_parent_symmetry:
        layout.label(text="✓ Parent symmetry")
    else:
        layout.label(text="x Parent symmetry")

    if has_length_symmetry:
        layout.label(text="✓ Length symmetry")
    else:
        layout.label(text="x Length symmetry")
        
    if has_deform_symmetry:
        layout.label(text="✓ Deform symmetry")
    else:
        layout.label(text="x Deform symmetry")


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
            checkSymmetry(obj.data.bones, layout)
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