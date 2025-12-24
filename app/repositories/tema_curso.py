from .base import Repository
from entities.tema_curso import TemaCurso

class TemaCursoRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, TemaCurso, "Edu_TemaCurso")

    def get_by_curso(self, id_curso):
        cursor = self.conn.cursor(dictionary=True)
        sql = f"SELECT * FROM {self.table_name} WHERE IdCurso = %s"
        cursor.execute(sql, (id_curso,))
        rows = cursor.fetchall()
        cursor.close()
        return [self.entity_class(**row) for row in rows]
