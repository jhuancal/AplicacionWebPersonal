from .base import Repository
from entities.examen_curso import ExamenCurso

class ExamenCursoRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, ExamenCurso, "Edu_ExamenCurso")
    
    def get_by_curso(self, id_curso):
        cursor = self.conn.cursor(dictionary=True)
        sql = f"SELECT * FROM {self.table_name} WHERE IdCurso = %s"
        cursor.execute(sql, (id_curso,))
        row = cursor.fetchone()
        cursor.close()
        return self.entity_class(**row) if row else None
