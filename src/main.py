from window import Window
from texture import Texture
from material import Material
from scene import Scene, RayScene
from shader_program import ShaderProgram
from camera import Camera
from cube import Cube
from quad import Quad
import numpy as np
import glm

from pathlib import Path

HERE = Path(__file__).resolve().parent      # .../TP4/src
SHADERS = HERE.parent / "shaders"           # .../TP4/shaders

WIDTH, HEIGHT = 800,600

# Ventana
window = Window(WIDTH, HEIGHT, "Basic Graphic Engine")

# Shader
shader_program = ShaderProgram(window.ctx, SHADERS / "basic.vert", SHADERS / "basic.frag")
shader_program_skybox = ShaderProgram(window.ctx, SHADERS / "sprite.vert", SHADERS / "sprite.frag")

skybox_texture = Texture(width=WIDTH, height=HEIGHT, channels_amount=3, color=(0, 0, 0))

material = Material(shader_program)
material_sprite = Material(shader_program_skybox, textures_data = [skybox_texture])
material_piso = Material(shader_program)

# Cámara
camera = Camera((0, 0, 10), (0, 0, 0), (0, 1, 0), 45, window.width / window.height, 0.1, 100.0)

#Objetos
cube1 = Cube((-2, 0, 2), (0, 45, 0), (1, 1, 1), name="Cube 1")
cube2 = Cube((2, 0, 2), (0, 45, 0), (1, 1, 1), name="Cube 2")
sprite = Quad((0,0,0), (0,0,0), (6,5,1), name="Sprite", hittable = False)
quad = Quad((0, -2, 0), (-90, 0, 0), (10, 15, 1), name="Piso", hittable=False)

# Escena
scene = RayScene(window.ctx, camera, WIDTH, HEIGHT)
scene.view = camera.get_view_matrix()
scene.projection = camera.get_perspective_matrix()

scene.add_object(sprite, material_sprite)
scene.add_object(quad, material_piso)
scene.add_object(cube1, material)
scene.add_object(cube2, material)

# Carga de la escena y ejecución del loop principal
window.set_scene(scene)
window.run()