from .base import Repository
from entities.rango_jugador_temporada import RangoJugadorTemporada

class RangoJugadorTemporadaRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, RangoJugadorTemporada, "Gam_RangoJugadorTemporada")
