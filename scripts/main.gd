extends Node3D

@onready var gltf_document_save := GLTFDocument.new()
@onready var gltf_state_save := GLTFState.new()


func _input(event):
	if event.is_action_pressed("saveScene"):
		save_scene()


func save_scene():
	gltf_document_save.append_from_scene($".", gltf_state_save)
	gltf_document_save.write_to_filesystem(gltf_state_save, "user://savedSnapshot.glb")
	print("Scene dumped.")
