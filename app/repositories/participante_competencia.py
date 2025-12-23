from .base import Repository
from entities.participante_competencia import ParticipanteCompetencia

class ParticipanteCompetenciaRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, ParticipanteCompetencia, "Gam_ParticipanteCompetencia")
