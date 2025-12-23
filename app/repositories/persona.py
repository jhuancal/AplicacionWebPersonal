from .base import Repository
from entities.persona import Persona

class PersonaRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Persona, "Adm_Persona")
        self.table_name = "Adm_Persona"
