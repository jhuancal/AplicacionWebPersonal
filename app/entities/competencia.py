from .base import Entidad

class Competencia(Entidad):
    def __init__(self, Id=None, Tipo=None, Fecha=None, DuracionMinutos=None, RamasIncluidas=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Tipo = Tipo
        self.Fecha = Fecha
        self.DuracionMinutos = DuracionMinutos
        self.RamasIncluidas = RamasIncluidas

    def to_dict(self):
        return {
            'Id': self.Id,
            'Tipo': self.Tipo,
            'Fecha': self.Fecha,
            'DuracionMinutos': self.DuracionMinutos,
            'RamasIncluidas': self.RamasIncluidas,
            'ESTADO': self.ESTADO
        }
