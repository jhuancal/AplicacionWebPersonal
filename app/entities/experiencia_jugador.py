from .base import Entidad

class ExperienciaJugador(Entidad):
    def __init__(self, Id=None, IdJugador=None, TotalExp=None, ExpPorCurso=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.TotalExp = TotalExp
        self.ExpPorCurso = ExpPorCurso

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'TotalExp': self.TotalExp,
            'ExpPorCurso': self.ExpPorCurso,
            'ESTADO': self.ESTADO
        }
