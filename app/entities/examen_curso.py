from .base import Entidad

class ExamenCurso(Entidad):
    def __init__(self, Id=None, IdCurso=None, Preguntas=None, NotaMinima=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdCurso = IdCurso
        self.Preguntas = Preguntas
        self.NotaMinima = NotaMinima

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdCurso': self.IdCurso,
            'Preguntas': self.Preguntas,
            'NotaMinima': self.NotaMinima,
            'ESTADO': self.ESTADO
        }
