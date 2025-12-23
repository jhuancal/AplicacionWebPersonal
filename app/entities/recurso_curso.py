from .base import Entidad

class RecursoCurso(Entidad):
    def __init__(self, Id=None, IdCurso=None, Tipo=None, Contenido=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdCurso = IdCurso
        self.Tipo = Tipo
        self.Contenido = Contenido

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdCurso': self.IdCurso,
            'Tipo': self.Tipo,
            'Contenido': self.Contenido,
            'ESTADO': self.ESTADO
        }
