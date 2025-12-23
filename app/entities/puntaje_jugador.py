from .base import Entidad

class PuntajeJugador(Entidad):
    def __init__(self, Id=None, IdJugador=None, PuntajeTotal=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.PuntajeTotal = PuntajeTotal

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'PuntajeTotal': self.PuntajeTotal,
            'ESTADO': self.ESTADO
        }
