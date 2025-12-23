from .base import Entidad

class Acceso(Entidad):
    def __init__(self, Id=None, Orden=None, Codigo=None, Nombre=None, Descripcion=None, 
                 Tipo=None, Nivel=None, Padre=None, UrlAcceso=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Orden = Orden
        self.Codigo = Codigo
        self.Nombre = Nombre
        self.Descripcion = Descripcion
        self.Tipo = Tipo
        self.Nivel = Nivel
        self.Padre = Padre
        self.UrlAcceso = UrlAcceso
