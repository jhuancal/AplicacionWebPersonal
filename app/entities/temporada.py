from .base import Entidad

class Temporada(Entidad):
    def __init__(self, Id=None, Nombre=None, FechaInicio=None, FechaFin=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Nombre = Nombre
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin

    def to_dict(self):
        return {
            'Id': self.Id,
            'Nombre': self.Nombre,
            'FechaInicio': self.FechaInicio,
            'FechaFin': self.FechaFin,
            'ESTADO': self.ESTADO
        }
