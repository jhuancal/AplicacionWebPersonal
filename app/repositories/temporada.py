from .base import Repository
from entities.temporada import Temporada

class TemporadaRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Temporada, "Gam_Temporada")
