extends Skeleton3D

@export var show_joint_axes : bool = false

var joint_mesh: Mesh
var multi_mesh_instance: MultiMeshInstance3D

func _ready():
	if show_joint_axes:
		setup_multi_mesh_instance()

func _process(_delta):
	if show_joint_axes:
		update_multi_mesh_instance_transforms()

func setup_multi_mesh_instance():
	multi_mesh_instance = MultiMeshInstance3D.new()
	var multi_mesh = MultiMesh.new()
	if not joint_mesh:
		joint_mesh = %Axis.mesh  # Fallback to a default mesh if none is provided
	multi_mesh.mesh = joint_mesh
	multi_mesh.transform_format = MultiMesh.TRANSFORM_3D
	multi_mesh.instance_count = get_bone_count()
	multi_mesh_instance.multimesh = multi_mesh
	add_child(multi_mesh_instance)

func update_multi_mesh_instance_transforms():
	for bone_index in range(get_bone_count()):
		var bone_global_pose = get_bone_global_pose(bone_index)
		multi_mesh_instance.multimesh.set_instance_transform(bone_index, bone_global_pose)
