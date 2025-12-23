from .base import Repository
from entities.intento_ejercicio_jugador import IntentoEjercicioJugador

class IntentoEjercicioJugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, IntentoEjercicioJugador, "Gam_IntentoEjercicioJugador")
