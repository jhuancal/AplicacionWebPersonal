from .base import Entidad

class RangoJugadorTemporada(Entidad):
    def __init__(self, Id=None, IdJugador=None, IdTemporada=None, Rango=None, PuntosTemporada=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.IdTemporada = IdTemporada
        self.Rango = Rango
        self.PuntosTemporada = PuntosTemporada

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'IdTemporada': self.IdTemporada,
            'Rango': self.Rango,
            'PuntosTemporada': self.PuntosTemporada,
            'ESTADO': self.ESTADO
        }
