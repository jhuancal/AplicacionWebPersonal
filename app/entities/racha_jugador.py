from .base import Entidad

class RachaJugador(Entidad):
    def __init__(self, Id=None, IdJugador=None, RachaActual=None, RachaMaxima=None, UltimoIngreso=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.RachaActual = RachaActual
        self.RachaMaxima = RachaMaxima
        self.UltimoIngreso = UltimoIngreso

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'RachaActual': self.RachaActual,
            'RachaMaxima': self.RachaMaxima,
            'UltimoIngreso': self.UltimoIngreso,
            'ESTADO': self.ESTADO
        }
