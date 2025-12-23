from .base import Entidad

class TemaCurso(Entidad):
    def __init__(self, Id=None, IdCurso=None, Nombre=None, Descripcion=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdCurso = IdCurso
        self.Nombre = Nombre
        self.Descripcion = Descripcion

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdCurso': self.IdCurso,
            'Nombre': self.Nombre,
            'Descripcion': self.Descripcion
        }
