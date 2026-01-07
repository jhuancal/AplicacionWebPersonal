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

    @staticmethod
    def register_user(username, password, email):
        import uuid
        import time
        
        conn = get_db_connection()
        try:
            user_repo = JugadorRepository(conn)
            existing = user_repo.get_by_username(username)
            if existing:
                return False, "Username already exists"
                
            # Create Persona
            persona_repo = PersonaRepository(conn)
            persona_id = f"P-{str(uuid.uuid4())[:8]}"
            persona_data = {
                "Id": persona_id,
                "Nombres": username, # Defaulting to username
                "Apellidos": "User",
                "Email": email,
                "ESTADO": 1,
                "FECHA_CREACION": int(time.time() * 1000)
            }
            persona_repo.add(**persona_data)
            
            # Create Jugador
            jugador_id = f"J-{str(uuid.uuid4())[:8]}"
            jugador_data = {
                "Id": jugador_id,
                "IdPersona": persona_id,
                "Username": username,
                "PasswordHash": password, # Plain text for dev
                "FechaRegistro": int(time.time() * 1000),
                "EstadoCuenta": "ACTIVO",
                "ESTADO": 1,
                "FECHA_CREACION": int(time.time() * 1000)
            }
            user_repo.add(**jugador_data)
            
            return True, "User created successfully"
            
        except Exception as e:
            print(f"Registration Error: {e}")
            return False, str(e)
        finally:
            conn.close()
