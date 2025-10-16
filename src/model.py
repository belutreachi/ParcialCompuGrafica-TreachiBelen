class Vertex: # representa un atributo de vértice de forma abstracta
    def __init__(self, name, format, array):
        self.__name = name
        self.__format = format
        self.__array = array # datos
    
    @property
    def name(self):
        return self.__name
    
    @property
    def format(self):
        return self.__format
    
    @property
    def array(self):
        return self.__array

class VertexLayout: # agrupa un conjunto de atributos de vértices
    def __init__(self):
        self.__attributes = []
    
    def add_attribute(self, name: str, format: str, array):
        self.__attributes.append(Vertex(name, format, array))
    
    def get_attributes(self):
        return self.__attributes

class Model: # clase base de todos los modelos 3D
    def __init__(self, vertices = None, indices = None, colors = None, normals = None, texcoords = None):
        self.vertices = vertices
        self.indices = indices
        self.colors = colors
        self.normals = normals
        self.texcoords = texcoords
        self.vertex_layout = VertexLayout() # construye el VertexLayout con los atributos que se pasen
        
        if vertices is not None:
            self.vertex_layout.add_attribute("in_pos", "3f", vertices) 
        if colors is not None:
            self.vertex_layout.add_attribute("in_color", "3f", colors)
        if normals is not None:
            self.vertex_layout.add_attribute("in_normal", "3f", normals)
        if texcoords is not None:
            self.vertex_layout.add_attribute("in_uv", "2f", texcoords)