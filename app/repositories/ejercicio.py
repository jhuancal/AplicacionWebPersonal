from .base import Repository
from entities.ejercicio import Ejercicio

class EjercicioRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Ejercicio, "Edu_Ejercicio")
