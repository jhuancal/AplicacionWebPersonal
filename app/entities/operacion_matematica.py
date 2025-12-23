from .base import Entidad

class OperacionMatematica(Entidad):
    def __init__(self, Id=None, IdCurso=None, Nombre=None, FuncionSistema=None, Formula=None, Atributos=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdCurso = IdCurso
        self.Nombre = Nombre
        self.FuncionSistema = FuncionSistema
        self.Formula = Formula
        self.Atributos = Atributos

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdCurso': self.IdCurso,
            'Nombre': self.Nombre,
            'FuncionSistema': self.FuncionSistema,
            'Formula': self.Formula,
            'Atributos': self.Atributos,
            'ESTADO': self.ESTADO
        }
