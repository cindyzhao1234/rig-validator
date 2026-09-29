import bpy

def isArmature(obj):
    return obj is not None and obj.type == 'ARMATURE'


def boneCount(obj):
    return len(obj.data.bones)


def removeSide(name):
    #remove the .L or .R of bone names
    if name.endswith((".L", ".R")):
        return name[:-2]

    return name


def printBones(bones):
    for bone in bones:

        if bone.parent:
            print(
                f"{bone.name}, "
                f"parent: {bone.parent.name}, "
                f"deform: {bone.use_deform}"
            )
        else:
            print(
                f"{bone.name}, "
                f"no parent, "
                f"deform: {bone.use_deform}"
            )


def checkSymmetry(bones, layout):

    has_name_symmetry = True
    has_parent_symmetry = True
    has_length_symmetry = True
    has_deform_symmetry = True

    for bone in bones:
        if not bone.name.endswith(".L"):
            continue

        right_name = bone.name[:-2] + ".R"

        #CHECK MATCHING RIGHT BONE
        if right_name not in bones:
            print(f"{bone.name} is missing {right_name}")
            has_name_symmetry = False
            continue

        right_bone = bones[right_name]

        print(f"{bone.name} has matching {right_name}")

        
        #CHECK MATCHING BONES HAVE MATCHING PARENTS
        # Both bones have parents
        if bone.parent and right_bone.parent:

            left_parent = removeSide(bone.parent.name)
            right_parent = removeSide(right_bone.parent.name)

            if left_parent != right_parent:
                print(
                    f"{bone.name} and {right_name} "
                    f"have different parents: "
                    f"{bone.parent.name} / {right_bone.parent.name}"
                )

                has_parent_symmetry = False

        # Only one bone has a parent
        elif bone.parent or right_bone.parent:

            print(
                f"{bone.name} and {right_name} "
                f"have different parent structures"
            )

            has_parent_symmetry = False

        #CHECK MATCHING BONES HAVE MATCHING LENGTHS

        if round(bone.length, 5) != round(right_bone.length, 5):

            print(
                f"{bone.name} length: {bone.length} | "
                f"{right_name} length: {right_bone.length}"
            )

            has_length_symmetry = False

        #CHECK MATCHING BONES HAVE MATCHING DEFORM SETTINGS
        if bone.use_deform != right_bone.use_deform:

            print(
                f"{bone.name} deform: {bone.use_deform} | "
                f"{right_name} deform: {right_bone.use_deform}"
            )

            has_deform_symmetry = False


    layout.label(text="Symmetry:")

    if has_name_symmetry:
        layout.label(text="✓ Name symmetry")
    else:
        layout.label(text="✗ Name symmetry")

    if has_parent_symmetry:
        layout.label(text="✓ Parent symmetry")
    else:
        layout.label(text="✗ Parent symmetry")

    if has_length_symmetry:
        layout.label(text="✓ Length symmetry")
    else:
        layout.label(text="✗ Length symmetry")

    if has_deform_symmetry:
        layout.label(text="✓ Deform symmetry")
    else:
        layout.label(text="✗ Deform symmetry")


def hasCorrectDeformSetting(bone):
    if bone.name.startswith("CTRL"):
        return bone.use_deform == False

    if bone.name.startswith("DEF"):
        return bone.use_deform == True

    return True


def checkDeformSettings(bones, layout):

    has_correct_deform_settings = True

    for bone in bones:

        if not hasCorrectDeformSetting(bone):

            print(
                f"{bone.name} has an incorrect "
                f"Deform setting: {bone.use_deform}"
            )

            has_correct_deform_settings = False

    layout.label(text="Deform Settings:")

    if has_correct_deform_settings:
        layout.label(text="✓ Deform settings correct")
    else:
        layout.label(text="✗ Incorrect deform settings")


class RIGVALIDATOR_PT_main_panel(bpy.types.Panel):

    bl_label = "Rig Validator"
    bl_idname = "RIGVALIDATOR_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig Validator"

    def draw(self, context):

        layout = self.layout

        layout.label(text="Rig Validator")

        obj = context.active_object

        #check if selected object is an armature
        if not isArmature(obj):
            layout.label(text="Select a valid armature")
            return

        layout.label(text="✓ Valid armature selected")

        bones = obj.data.bones
        bone_count = boneCount(obj)

        layout.label(text=f"Bones: {bone_count}")

        checkSymmetry(bones, layout)
        checkDeformSettings(bones, layout)

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