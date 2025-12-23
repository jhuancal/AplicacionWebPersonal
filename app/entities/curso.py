from .base import Entidad

class Curso(Entidad):
    def __init__(self, Id=None, Nombre=None, Descripcion=None, Rama=None, Nivel=None, UrlImagen=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Nombre = Nombre
        self.Descripcion = Descripcion
        self.Rama = Rama
        self.Nivel = Nivel
        self.UrlImagen = UrlImagen

    def to_dict(self):
        return {
            'Id': self.Id,
            'Nombre': self.Nombre,
            'Descripcion': self.Descripcion,
            'Rama': self.Rama,
            'Nivel': self.Nivel,
            'UrlImagen': self.UrlImagen,
            'ESTADO': self.ESTADO
        }
