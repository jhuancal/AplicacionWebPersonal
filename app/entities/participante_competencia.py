from .base import Entidad

class ParticipanteCompetencia(Entidad):
    def __init__(self, Id=None, IdCompetencia=None, IdJugador=None, PuntosObtenidos=None, PosicionFinal=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdCompetencia = IdCompetencia
        self.IdJugador = IdJugador
        self.PuntosObtenidos = PuntosObtenidos
        self.PosicionFinal = PosicionFinal

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdCompetencia': self.IdCompetencia,
            'IdJugador': self.IdJugador,
            'PuntosObtenidos': self.PuntosObtenidos,
            'PosicionFinal': self.PosicionFinal,
            'ESTADO': self.ESTADO
        }
