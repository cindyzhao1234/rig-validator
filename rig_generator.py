import bpy

#create new armature data
armature_data = bpy.data.armatures.new("NewArmatureData")

#create new armature object
rig = bpy.data.objects.new("NewArmatureRig", armature_data)
rig.show_in_front = True #always make it show in front

#add the object in collection
bpy.context.collection.objects.link(rig)

bpy.context.view_layer.objects.active = rig
rig.select_set(True) #select the armature

bpy.ops.object.mode_set(mode="EDIT") #enter edit mode

bones = armature_data.edit_bones #the collection of bones we are allowed to edit

#helper function to create a bone
def createBone(name, parent, head, tail, connected):
    bone = bones.new(name)
    bone.parent = parent
    bone.tail = tail
    
    if connected:
        bone.head = parent.tail
    else:
        bone.head = head

    if parent == None:
        bone.use_connect = False
    else:
        bone.use_connect = connected

    return bone


root = createBone("root", None, (0, 0, 0), (0, 0, 0.5), False)
pelvis_bone = createBone("pelvis_bone", root, (0, 0, 0.85), (0, -0.05, 1.05), False)
spine001 = createBone("spine001", pelvis_bone, None, (0, -0.04, 1.25), True)
spine002 = createBone("spine002", spine001, None, (0, -0.01, 1.45), True)
neck = createBone("neck", spine002, None, (0, -0.04, 1.55), True)
head = createBone("head", neck, None, (0, -0.1, 1.75), True)

shoulder_L = createBone("shoulder.L", spine002, (0.05, 0, 1.45), (0.18, 0.01, 1.41), False)
arm001 = createBone("arm001.L", shoulder_L, None, (0.43, 0.03, 1.40), True)
arm002 = createBone("arm002.L", arm001, None, (0.66, 0.02, 1.41), True)
hand = createBone("hand.L", arm002, None, (0.83, 0, 1.39), True)

leg001 = createBone("leg001.L", pelvis_bone, (0.1, -0.01, 0.85), (0.12, 0, 0.47), False)
leg002 = createBone("leg002.L", leg001, None, (0.15, 0.06, 0.05), True)

foot = createBone("foot.L", leg002, None, (0.16, -0.07, 0), True)

for bone in bones:
    if bone.name.endswith(".L"):
        bone.select = True
        bone.select_head = True
        bone.select_tail = True

#symmetrise the left to the right 
bpy.ops.armature.symmetrize(direction='POSITIVE_X', copy_bone_colors=False)

bpy.ops.object.mode_set(mode="OBJECT") #enter object mode

#select mesh first then rig
body_mesh = bpy.data.objects["MainBody"]
head_mesh = bpy.data.objects["Head"]
lash_mesh = bpy.data.objects["head_eyelashes"]
eyes_mesh = bpy.data.objects["head_eyes"]
teeth_mesh = bpy.data.objects["head_teeth"]

body_mesh.select_set(True)
head_mesh.select_set(True)
lash_mesh.select_set(True)
eyes_mesh.select_set(True)
teeth_mesh.select_set(True)

#make the rig the main target selection
bpy.context.view_layer.objects.active = rig

#connect
bpy.ops.object.parent_set(type='ARMATURE_AUTO')