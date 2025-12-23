from .base import Entidad

class Rol(Entidad):
    def __init__(self, Id=None, Nombre=None, Descripcion=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Nombre = Nombre
        self.Descripcion = Descripcion
