from .base import Entidad

class HistorialCompetenciasJugador(Entidad):
    def __init__(self, Id=None, IdJugador=None, TotalCompetencias=None, Victorias=None, MejorPosicion=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.TotalCompetencias = TotalCompetencias
        self.Victorias = Victorias
        self.MejorPosicion = MejorPosicion

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'TotalCompetencias': self.TotalCompetencias,
            'Victorias': self.Victorias,
            'MejorPosicion': self.MejorPosicion,
            'ESTADO': self.ESTADO
        }
