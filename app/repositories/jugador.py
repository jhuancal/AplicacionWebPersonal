from .base import Repository
from entities.jugador import Jugador

class JugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Jugador, "Seg_Jugador")

    def get_by_username(self, username):
        cursor = self.conn.cursor(dictionary=True)
        # Using self.table_name provided by base Repository
        sql = f"SELECT * FROM {self.table_name} WHERE Username = %s AND ESTADO = 1"
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        cursor.close()
        return row
