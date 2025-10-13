from window import Window
from texture import Texture
from material import Material, StandardMaterial
from shader_program import ShaderProgram
from scene import Scene, RayScene, RaySceneGPU
from camera import Camera
from cube import Cube
from quad import Quad
import numpy as np
import glm

from pathlib import Path

HERE = Path(__file__).resolve().parent      # .../TP4/src
SHADERS = HERE.parent / "shaders"           # .../TP4/shaders

WIDTH, HEIGHT = 800, 600

SCENE_TYPE = "gpu" # Opciones: "normal", "cpu", "gpu"

scene_configs = {
    "normal": {
        "needs_sprite": False,
        "sprite_channels_amount": 3,
        "sprite_default_color": (255, 255, 255)
    },
    "cpu": {
        "needs_sprite": True,
        "sprite_channels_amount": 3,
        "sprite_default_color": (255, 255, 255)
    }, 
    "gpu": {
        "needs_sprite": True,
        "sprite_channels_amount": 4,
        "sprite_default_color": (255, 255, 255, 255)
    }
}

config = scene_configs[SCENE_TYPE]

# Ventana
window = Window(WIDTH, HEIGHT, f"Basic Graphic Engine - {SCENE_TYPE.upper()}")

# Shader
shader = ShaderProgram(window.ctx, SHADERS / "basic.vert", SHADERS / "basic.frag")
shader_sprite = ShaderProgram(window.ctx, SHADERS / "sprite.vert", SHADERS / "sprite.frag")

albedo_red = Texture("u_texture", WIDTH, HEIGHT, 3, None, (200, 10, 190))
albedo_blue = Texture("u_texture", WIDTH, HEIGHT, 3, None, (0, 0, 255))
albedo_pearl = Texture("u_texture", WIDTH, HEIGHT, 3, None, (120, 90, 90))

sprite_texture = Texture(width=WIDTH, height=HEIGHT, channels_amount=config["sprite_channels_amount"], color=config["sprite_default_color"])

material_plastic = StandardMaterial(shader, albedo_red, reflectivity=0.0)
material_glass = StandardMaterial(shader, albedo_blue, reflectivity=0.2)
material_ceramic = StandardMaterial(shader, albedo_pearl, reflectivity=0.1)
material_sprite = Material(shader_sprite, textures_data=[sprite_texture])

#Objetos
cube1 = Cube((-2, 0, 2), (0, 45, 0), (1, 1, 1), name="Cube1")
cube2 = Cube((2, 0, 2), (0, 45, 0), (1, 1, 1), name="Cube2")
quad = Quad((0, -2, 0), (-90, 0, 0), (10, 15, 1), name="Floor", animated=False)
sprite = Quad((0, 0, 0), (0, 0, 0), (6, 5, 1), name="Sprite", animated=False, hittable = False)

cube1gpu = Cube((-2, 2, 5), (0, 0, 0), (1, 1, 1), name="Cube1", animated=True)
cube2gpu = Cube((2, 2, 5), (0, 0, 0), (1, 1, 1), name="Cube2", animated=True)

# Cámara
camera = Camera((0, 0, 10), (0, 0, 0), (0, 1, 0), 45, WIDTH / HEIGHT, 0.01, 100.0)
cameraGPU = Camera((0, 1, 20), (0, 0, 0), (0, 1, 0), 45, WIDTH / HEIGHT, 0.01, 100.0)
camera.set_sky_colors(top=(16, 150, 222), bottom=(181, 224, 247))

if SCENE_TYPE == "normal":
    scene = Scene(window.ctx, camera)
    scene.add_object(cube1, material_plastic)
    scene.add_object(cube2, material_glass)

elif SCENE_TYPE == "cpu":
    scene = RayScene(window.ctx, camera, WIDTH, HEIGHT)
    scene.add_object(sprite, material_sprite)
    scene.add_object(cube1, material_plastic)
    scene.add_object(cube2, material_glass)
    scene.add_object(quad, material_ceramic)

elif SCENE_TYPE == "gpu":
    scene = RaySceneGPU(window.ctx, cameraGPU, WIDTH, HEIGHT, sprite, material_sprite)
    scene.add_object(cube1gpu, material_plastic)
    scene.add_object(cube2gpu, material_glass)
    scene.add_object(quad, material_ceramic)

# Carga de la escena y ejecución del loop principal
window.set_scene(scene)
window.run()