from repositories.usuario import UsuarioRepository
from repositories.cliente import ClienteRepository
from repositories.colaborador import ColaboradorRepository
from repositories.persona import PersonaRepository
from db import get_db_connection

class AuthService:
    @staticmethod
    def validate_user(username, password):
        conn = get_db_connection()
        try:
            repo = UsuarioRepository(conn)
            user = repo.get_by_username(username) # Returns dict from cursor (fetch_one)
            if user and user['Contrasena'] == password:
                return True
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_details(username):
        conn = get_db_connection()
        try:
            # 1. Get Base User to get IDs
            user_repo = UsuarioRepository(conn)
            base_user = user_repo.get_by_username(username)
            
            if not base_user:
                return None
            
            user_data = base_user # Dict
            
            is_collaborator = username.startswith('ws_')
            
            # 2. Get Extended Data
            if is_collaborator:
                # Fetch Colaborador Data
                # Custom query or repo method. 
                # Doing raw query here to keep Repos simple if they don't have get_by_id_joined
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT C.IdRol, C.EsActivo, C.FechaContratacion, R.Nombre as RolNombre
                    FROM Seg_Colaborador C
                    LEFT JOIN Seg_Rol R ON C.IdRol = R.Id
                    WHERE C.Id = %s
                """
                cursor.execute(query, (base_user['Id'],))
                collab_data = cursor.fetchone()
                if collab_data:
                    user_data.update(collab_data)
                    user_data['Tipo'] = 'Colaborador'
            else:
                # Fetch Cliente Data
                cursor = conn.cursor(dictionary=True)
                query = "SELECT NumeroCuenta FROM Seg_Cliente WHERE Id = %s"
                cursor.execute(query, (base_user['Id'],))
                client_data = cursor.fetchone()
                if client_data:
                    user_data.update(client_data)
                    user_data['Tipo'] = 'Cliente'
            
            # 3. Get Persona Data
            if base_user.get('IdPersona'):
                cursor = conn.cursor(dictionary=True)
                query = "SELECT Nombres, Apellidos, DNI, Correo FROM Adm_Persona WHERE Id = %s"
                cursor.execute(query, (base_user['IdPersona'],))
                persona_data = cursor.fetchone()
                if persona_data:
                    user_data.update(persona_data)
            
            return user_data
            
        finally:
            conn.close()
