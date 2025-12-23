from .base import Repository
from entities.rol import Rol

class RolRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Rol, "Seg_Rol")
