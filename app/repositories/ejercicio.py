from .base import Repository
from entities.ejercicio import Ejercicio

class EjercicioRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Ejercicio, "Edu_Ejercicio")

    def get_by_tema(self, id_tema):
        cursor = self.conn.cursor(dictionary=True)
        # Assuming Ejercicio has soft delete logic via relationship or direct state
        # But Ejercicio table doesn't have ESTADO in my init.sql? 
        # Let's check init.sql again. Edu_Ejercicio definition does NOT have ESTADO.
        # But base class assumes ESTADO=1. This might be a problem if base.get_all is used.
        # Here we write custom query so we are safe.
        sql = f"SELECT * FROM {self.table_name} WHERE IdTema = %s"
        cursor.execute(sql, (id_tema,))
        rows = cursor.fetchall()
        cursor.close()
        return [self.entity_class(**row) for row in rows]
