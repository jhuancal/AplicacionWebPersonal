from .base import Entidad

class DesafioJugador(Entidad):
    def __init__(self, Id=None, IdJugador=None, FocoPrincipal=None, Contenido=None, Estado=None, FechaAsignacion=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.FocoPrincipal = FocoPrincipal
        self.Contenido = Contenido
        self.Estado = Estado
        self.FechaAsignacion = FechaAsignacion

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'FocoPrincipal': self.FocoPrincipal,
            'Contenido': self.Contenido,
            'Estado': self.Estado,
            'FechaAsignacion': self.FechaAsignacion,
            'ESTADO': self.ESTADO
        }
