from .base import Entidad

class AvanceCursoJugador(Entidad):
    def __init__(self, Id=None, IdJugador=None, IdCurso=None, NivelActual=None, PorcentajeAvance=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.IdCurso = IdCurso
        self.NivelActual = NivelActual
        self.PorcentajeAvance = PorcentajeAvance

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'IdCurso': self.IdCurso,
            'NivelActual': self.NivelActual,
            'PorcentajeAvance': self.PorcentajeAvance,
            'ESTADO': self.ESTADO
        }
