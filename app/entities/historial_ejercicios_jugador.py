from .base import Entidad

class HistorialEjerciciosJugador(Entidad):
    def __init__(self, Id=None, IdJugador=None, TotalEjerciciosResueltos=None, PorcentajeExito=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.TotalEjerciciosResueltos = TotalEjerciciosResueltos
        self.PorcentajeExito = PorcentajeExito

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'TotalEjerciciosResueltos': self.TotalEjerciciosResueltos,
            'PorcentajeExito': self.PorcentajeExito,
            'ESTADO': self.ESTADO
        }
