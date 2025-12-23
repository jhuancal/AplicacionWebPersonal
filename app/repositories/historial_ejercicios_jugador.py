from .base import Repository
from entities.historial_ejercicios_jugador import HistorialEjerciciosJugador

class HistorialEjerciciosJugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, HistorialEjerciciosJugador, "Gam_HistorialEjerciciosJugador")
