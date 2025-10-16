import numpy as np
import glm

class Graphics:
    def __init__(self, ctx, model, material):
        self.__ctx = ctx
        self.__model = model
        self.__material = material

        self.__vbo = self.create_buffers() # almacena los datos de los vertices (posicion, color, normales, UV)
        self.__ibo = ctx.buffer(model.indices.tobytes()) # almacena los indices para dibujar los vertices
        self.__vao = ctx.vertex_array(material.shader_program.prog, [*self.__vbo], self.__ibo) # combina VBO e IBO y define el formato de los datos; se vincula con el shader

        self.__textures = self.load_textures(material.textures_data) # se cargan automáticamente las texturas desde el material
    
    def create_buffers(self): # crea los buffers VBOs y los vincula con el shader
        buffers = []
        shader_attributes = self.__material.shader_program.attributes

        for attribute in self.__model.vertex_layout.get_attributes(): # se recorre cada tributo expuesto del shader
            if attribute.name in shader_attributes: # se compara con los atributos del modelo
                vbo = self.__ctx.buffer(attribute.array.tobytes()) # se agrega el VBO al array de buffers
                buffers.append((vbo, attribute.format, attribute.name)) # se crea el VBO ccomo tuplas con su formato y nombre
        return buffers # retorna una lista de buffers VBOs para crear el VAO
    
    def load_textures(self, textures_data): 
        textures = {}
        for texture in textures_data: # se recorren las texturas del material
            if texture.image_data: # si la textura tiene datos de imagen
                texture_ctx = self.__ctx.texture(texture.size, texture.channels_amount, texture.get_bytes()) # carga la textura en el GPU con sus datos
                if texture.build_mipmaps:
                    texture_ctx.build_mipmaps()
                texture_ctx.repeat_x = texture.repeat_x
                texture_ctx.repeat_y = texture.repeat_y
                textures[texture.name] = (texture, texture_ctx)
        return textures 
    
    def bind_to_image(self, name = "u_texture", unit = 0, read = False, write = True):
        self.__textures[name][1].bind_to_image(unit, read, write)
    
    def render(self, uniforms): # renderiza el VAO en el context
        for name, value in uniforms.items():
            if name in self.__material.shader_program.prog: # si el nombre del uniform existe en el shader
                self.__material.set_uniform(name, value) # actualiza los uniforms del shader
        
        for i, (name, (tex, tex_ctx)) in enumerate(self.__textures.items()): # diccionario de texturas
            tex_ctx.use(i)
            self.__material.shader_program.set_uniform(name, i)
        
        self.__vao.render() # dibuja el VAO en el context

    def update_texture(self, texture_name, new_data): # toma los nuevos datos de una textura y los manda a la GPU
        if texture_name not in self.__textures: 
            raise ValueError(f"No existe la textura {texture_name}")
        
        texture_obj, texture_ctx = self.__textures[texture_name]
        texture_obj.update_data(new_data) # si existe, actualizamos el ImageData en la instancia de Texture
        texture_ctx.write(texture_obj.get_bytes()) # escribimos los bytes en la textura de la GPU

class ComputeGraphics(Graphics): # interfaz entre un modelo y el sistema de raytracing en GPU
    def __init__(self, ctx, model, material):
        self.__ctx = ctx
        self.__model = model
        self.__material = material
        self.textures = material.textures_data
        super().__init__(ctx, model, material) # reutiliza el mismo mecanismo de creacion de buffers y VAO que Graphics
    
    def create_primitive(self, primitives): # añade la primitive mínima del modelo actual a la lista de primitivas
        amin, amax = self.__model.aabb
        primitives.append({"aabb_min": amin, "aabb_max": amax})

    def create_transformation_matrix(self, transformations_matrix, index): # escribe la matriz de modelo en la fila index del array de transformaciones
        m = self.__model.get_model_matrix()
        transformations_matrix[index, :] = np.array(m.to_list(), dtype="f4").reshape(16)
    
    def create_inverse_transformation_matrix(self, inverse_transformations_matrix, index): # escribe la matriz de modelo inversa
        m = self.__model.get_model_matrix()
        inverse = glm.inverse(m)
        inverse_transformations_matrix[index, :] = np.array(inverse.to_list(), dtype="f4").reshape(16)
    
    def create_material_matrix(self, materials_matrix, index):
        reflectivity = self.__material.reflectivity
        r,g,b = self.__material.colorRGB

        r = r / 255.0 if r > 1.0 else r
        g = g / 255.0 if g > 1.0 else g
        b = b / 255.0 if b > 1.0 else b

        materials_matrix[index, :] = np.array([r, g, b, reflectivity], dtype="f4")