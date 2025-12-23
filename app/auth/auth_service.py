from repositories.jugador import JugadorRepository
from repositories.persona import PersonaRepository
from db import get_db_connection

class AuthService:
    @staticmethod
    def validate_user(username, password):
        conn = get_db_connection()
        try:
            repo = JugadorRepository(conn)
            user = repo.get_by_username(username) # Returns dict from cursor (fetch_one)
            if user and user['PasswordHash'] == password:
                return True
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_details(username):
        conn = get_db_connection()
        try:
            # 1. Get Base User to get IDs
            user_repo = JugadorRepository(conn)
            base_user = user_repo.get_by_username(username)
            
            if not base_user:
                return None
            
            user_data = base_user # Dict
            
            # 2. Get Persona Data
            if base_user.get('IdPersona'):
                cursor = conn.cursor(dictionary=True)
                query = "SELECT Nombres, Apellidos, Dni, Email FROM Adm_Persona WHERE Id = %s"
                cursor.execute(query, (base_user['IdPersona'],))
                persona_data = cursor.fetchone()
                if persona_data:
                    user_data.update(persona_data)
            
            return user_data
            
        finally:
            conn.close()
