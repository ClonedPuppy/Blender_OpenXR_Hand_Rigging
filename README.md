# Blender OpenXR Hand Rigging
 How to rig VR hand meshes in Blender for OpenXR & Godot

https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/47b8cca0-4f1a-49a8-b223-b3b573036ac3

The issue with rigging hands for Godot is that OpenXR specifies the bone axes to have Z as the bone longitudinal axes (the axis between the head and tail). 
Blender's bone axes, however, use Y for the longitudinal axis. This complicates both the rigging and the skinning processes in Blender

Following is a workflow that helps from an artist point of view, as it implements a fairly regular bone / skinning workflow that most Blender artists are accustomed to.

As hand meshes can come in all sorts of poses, it's a good idea to first plan out your execution. If your hand mesh comes in a grip pose for instance, then it might be necessary to get a snapshot of how the OpenXR joints are positioned and oriented in that particular pose (if your hand mesh is in a similar pose as my example Blender project, then you can just disregard this step and use my existing bones setup).

In the Godot project, there is a script attached to main, which dumps the entire scene into a glb file and saves it in %APPDATA%\Roaming\Godot\app_userdata\Blender_OpenXR_Hand_Rigging as savedSnapshot.glb. 
Before you do this, switch on the "Show Joint Axes" in the skeleton node. 

![Godot_v4 2 1-stable_win64_dMPFJMZo6r](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/827cfb93-d376-459d-abc4-25b6ee9606f4)

You probably only need the left hand as well, so delete the hand_r under the RightHand node as well. Your node tree should look something like this:

![Godot_v4 2 1-stable_win64_lug62qWBcO](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/bff996ee-6080-4d89-b792-bd258bcf9ff1)

Now you are ready to save the OpenXR joints, run the project and try to pose your hand in a similar pose your mesh is in. Don't worry, it doesn't have to be perfect. Try to position the hand with the palm facing down, as that makes it easier to rig later in Blender. Press Enter key to save a snapshot.

![image](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/4954b3e8-4020-4bc4-a19c-fd98b91d4a94)

Import the savedSnapshot.glb in Blender and you will see a bunch of stuff. Delete everything apart from the _MultiMeshInstance3D (unparent it from the other node by holding shift and drag it to the root. Your blender scene tree should look similar to this:

![blender_xJgxTDSew1](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/f1d3b2d4-56fa-4bcd-9a71-603f53b48c57)

Position and orient the reference joints, I prefer to place the wrist joint at around 0,0,0. You can also scale down the axes a bit if you prefer them smaller. Here is how I lay it out:

![blender_Kx3iehLSFY](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/86100050-b264-47a2-b992-b36a27a237df)

Next step is to prep the bones. Start at the wrist and lay them out following the OpenXR joints. Be careful to align the x,y,z axes, but remember that Blender is Z up, so align the bone's Z axis with the OpenXR joints green axis (don't forget you also need to use the bone's roll angle for some bones). Additionally, you will also need to add a tip bone. This bone is not really used for the skinning, but is necessary to add so that OpenXR can pick it up later in Godot. Don't forget to name your bones as well! Here is my progress after a few bones:

![blender_clIiNz31jq](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/66e06e9d-2656-420f-b7a0-bb1f5639e4e3)

Once this step is done, we can bring in the hand mesh. Position and orient it as you see fit, try to get the three inner fingers and palm to match as well as you can, the thumb and pinky will usually need some adjustments.
After the hand mesh is in place and parented with the Armature, start repositioning the individual bones into the correct position in the hand. Since you already have setup the bones and aligned them correctly, it's just a matter of moving them around slightly, especially if your captured hand pose resembles the actual hand mesh. You should now have all the bones placed in the hand and it should hopefully look something like this:

![blender_v2DBPJUuSQ](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/31652ebb-d75b-419a-92a2-bafd834ebbf0)

Now we move to the skinning part. Select the hand mesh and enter Weight Paint mode. Head over to the Data tab and delete all the vertex groups.

![image](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/1d0ad438-ef7f-4118-b26b-00192918badb)

Ctrl-click Select all the bones apart from the Palm_L bone like so:

![blender_Z1ZpQsraRv](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/c8bf199f-2dd5-428d-a979-89576c227f4b)

Go to Weights and Assign Automatic from Bones:

![image](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/af47e0f4-4fbb-4c47-8b12-8b2733d5537e)

You can check that all is ok, by looking at your newly created vertex groups, each of them should have weight map values (apart from the tips).

![blender_MRO5hEr67h](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/d238e987-49ef-441a-85b6-60d94b0ac717)

Exit Weight Paint mode and save your Blender project. Now we need to prep the rig for gltf export. Install and enable the script called "rotate_them_bones.py" in your Blender addons. It will create a small tool panel:

![blender_AyImTMEGZ3](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/163f8079-88f7-4fc3-a18a-a292bbae2b00)

This script will not do everything for you, as I had issues with getting the bone's roll angle to properly work when rotating the bones 90 degrees via script. So unfortunately for now, we need to do this step manually, and then store the roll values. Once this is done, you can freely move between rotated and non rotated bones.
As per the scripts instructions, first select the Armature in the scene tree, then press "Disconnect Bones". This will disconnect all bones so they can be rotated freely without any parenting hierarchy.
After this, you will be in Bone edit mode, make sure you set your transform and pivot to "Normal" and "Individual Origins"

![blender_DOc0OuAs9Q](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/2cca6b6e-fece-45b5-800f-bf1670c59b43)

Press a to SELECT ALL, then r for ROTATE, x for the X axis and then 90 for the amount of degrees (and Enter key to confirm). Bones should now look like this:

![blender_uMk5fn7xvR](https://github.com/ClonedPuppy/Blender_OpenXR_Hand_Rigging/assets/1387713/0d4ffb00-7350-4499-82fc-f7e163c461ad)

Before gltf export, press "Store Bone Roll angles", this will store all the correct values.

Proceed with the export, make sure you hide the OpenXR reference stuff. There are no other options in the gltf exporter we need to adjust.

Check out your hand in Godot, it should be fairly good, but there will always be areas that could be fixed. The hand I used in the example project are completely auto weighted, without any manual adjustments. And if you look closely at some of the knuckles, they require a bit of work to not looks so hard and angular. Luckily you can easily revert back to Blenders workflow, with the bones aligned in the correct way. Press "Rotate back" and the bones will snap back to their initial position and be connected up as they were originally.
Now you can flip back and forth between "Rotate" and "Rotate back" whenever you need to adjust bone positions, paint weights or export.

Be mindful that there is no undo when using the script, or at least not a very good one. So save your blender project before you start with the export process. Also, if you close Blender, or it crashes... then you will need to do the rotate steps all over again.

As for creating the right hand, it's basically a mirror of the Armature, and then some manual adjustments on the thumb and pinky bones as they usually goa bit wonky. MIrror over the openxr reference as well so you have a something to refer to when adjusting back the axes. You also need to flip the mesh faces etc.. and all the usual stuff you need to do after a mirror operation. 


