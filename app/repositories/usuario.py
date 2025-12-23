from .base import Repository
from entities.usuario import Usuario

class UsuarioRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Usuario, "Seg_Usuario")

    def get_by_username(self, username):
        cursor = self.conn.cursor(dictionary=True)
        query = f"SELECT * FROM {self.table_name} WHERE NombreUsuario = %s AND ESTADO = 1"
        cursor.execute(query, (username,))
        return cursor.fetchone()
