from moderngl import Attribute, Uniform
import glm

class ShaderProgram:
    def __init__(self, ctx, vertex_shader_path, fragment_shader_path):
        with open(vertex_shader_path) as file:
            vertex_shader = file.read()
        with open(fragment_shader_path) as file:
            fragment_shader = file.read()
        
        self.prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        attributes = []
        uniforms = []
        
        for name in self.prog: # itera sobre todos los miembros del programa para detectar que miembros expone el shader
            member = self.prog[name]
            if type(member) is Attribute:
                attributes.append(name) # si es un atributo, lo añade a la lista de atributos
            if type(member) is Uniform:
                uniforms.append(name) # si es un uniform, lo añade a la lista de uniforms
        
        self.attributes = list(attributes)
        self.uniforms = uniforms

    def set_uniform(self, name, value): # modifica un uniform si los shaders lo declaran
        if name in self.uniforms: 
            uniform = self.prog[name] 
            if isinstance(value, glm.mat4): # si el valor es una matriz 4x4 de glm, la convierte a bytes para enviarla en el formato correcto
                uniform.write(value.to_bytes())
            elif hasattr(uniform, "value"): # otros tipos --> se asignan a uniform.value si existe esa propiedad
                uniform.value = value

class ComputeShaderProgram:
    def __init__(self, ctx, compute_shader_path):
        with open(compute_shader_path) as file:
            compute_source = file.read()
        self.prog = ctx.compute_shader(compute_source)

        uniforms = []
        for name in self.prog:
            member = self.prog[name]
            if type(member) is Uniform:
                uniforms.append(name)
        
        self.uniforms = uniforms

    def set_uniform(self, name, value):
        if name in self.uniforms:
            uniform = self.prog[name]
            if isinstance(value, glm.mat4):
                uniform.write(value.to_bytes())
            elif hasattr(uniform, "value"):
                uniform.value = value
    
    def run(self, groups_x, groups_y, groups_z=1):
        self.prog.run(group_x=groups_x, group_y=groups_y, group_z=groups_z)