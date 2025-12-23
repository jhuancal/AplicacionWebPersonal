from .base import Entidad

class MetodoResolucion(Entidad):
    def __init__(self, Id=None, IdOperacion=None, Nombre=None, Pasos=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdOperacion = IdOperacion
        self.Nombre = Nombre
        self.Pasos = Pasos

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdOperacion': self.IdOperacion,
            'Nombre': self.Nombre,
            'Pasos': self.Pasos,
            'ESTADO': self.ESTADO
        }
