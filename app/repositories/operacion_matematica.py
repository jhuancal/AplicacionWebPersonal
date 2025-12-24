from .base import Repository
from entities.operacion_matematica import OperacionMatematica

class OperacionMatematicaRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, OperacionMatematica, "Edu_OperacionMatematica")

    def get_by_curso(self, id_curso):
        # OperacionMatematica doesn't have ESTADO column in schema, so custom query
        cursor = self.conn.cursor(dictionary=True)
        sql = f"SELECT * FROM {self.table_name} WHERE IdCurso = %s"
        cursor.execute(sql, (id_curso,))
        rows = cursor.fetchall()
        cursor.close()
        return [self.entity_class(**row) for row in rows]
