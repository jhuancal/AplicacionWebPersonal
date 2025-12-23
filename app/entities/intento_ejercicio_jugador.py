from .base import Entidad

class IntentoEjercicioJugador(Entidad):
    def __init__(self, Id=None, IdJugador=None, IdEjercicio=None, RespuestaJugador=None, EsCorrecto=None, PuntosGanados=None, FechaIntento=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdJugador = IdJugador
        self.IdEjercicio = IdEjercicio
        self.RespuestaJugador = RespuestaJugador
        self.EsCorrecto = EsCorrecto
        self.PuntosGanados = PuntosGanados
        self.FechaIntento = FechaIntento

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdJugador': self.IdJugador,
            'IdEjercicio': self.IdEjercicio,
            'RespuestaJugador': self.RespuestaJugador,
            'EsCorrecto': self.EsCorrecto,
            'PuntosGanados': self.PuntosGanados,
            'FechaIntento': self.FechaIntento,
            'ESTADO': self.ESTADO
        }
