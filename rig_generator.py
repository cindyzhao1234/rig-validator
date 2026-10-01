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

root_bone = bones.new("root bone") #new bone

#give coordinates for head and tail of bone
root_bone.head = (0, 0, 0)
root_bone.tail = (0, 0, 0.5)

pelvis_bone = bones.new("pelvis bone")
pelvis_bone.head = (0, 0, 0.85)
pelvis_bone.tail = (0, 0, 1.0)

#set the parent of the pelvis_bone to root_bone
pelvis_bone.parent = root_bone
pelvis_bone.use_connect = False