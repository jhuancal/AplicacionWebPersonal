from db import get_db_connection
import uuid
import time
import json
from services.exercise_generator import ExerciseGeneratorService
from repositories.operacion_matematica import OperacionMatematicaRepository
import random

class MatchmakingService:
    @staticmethod
    def find_match(user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 1. Look for waiting rooms (waiting for player 2)
            cursor.execute("SELECT * FROM Gam_MatchPvP WHERE Estado = 'ESPERANDO' AND IdJugador1 != %s LIMIT 1", (user_id,))
            room = cursor.fetchone()
            
            if room:
                # Join existing room
                room_id = room['Id']
                cursor.execute("UPDATE Gam_MatchPvP SET IdJugador2 = %s, Estado = 'EN_CURSO' WHERE Id = %s", (user_id, room_id))
                conn.commit()
                return {"id": room_id, "status": "MATCH_FOUND", "opponent": room['IdJugador1'], "role": "PLAYER_2"}
            else:
                # Create new room
                # Generate a set of questions for this match
                questions = MatchmakingService._generate_match_questions(conn)
                
                room_id = f"ROOM-{str(uuid.uuid4())[:8]}"
                cursor.execute("""
                    INSERT INTO Gam_MatchPvP (Id, IdJugador1, Estado, DatosPartida, FECHA_CREACION)
                    VALUES (%s, %s, 'ESPERANDO', %s, %s)
                """, (room_id, user_id, json.dumps(questions), int(time.time() * 1000)))
                conn.commit()
                return {"id": room_id, "status": "WAITING", "role": "PLAYER_1"}
                
        finally:
            conn.close()

    @staticmethod
    def _generate_match_questions(conn):
        # Generate 5 questions (Level 1 to 5)
        # Assuming Algebra course for now or generic math
        # Ideally we pick a course, but let's default to Algebra generators for PvP
        
        op_repo = OperacionMatematicaRepository(conn)
        generators = op_repo.get_all() # Get all known generators
        if not generators:
            return []
            
        questions = []
        for i in range(1, 6): # 5 Rounds
            gen = random.choice(generators)
            # We can vary difficulty if generator supports it, for now random
            q = ExerciseGeneratorService.generate(gen)
            q['round'] = i
            questions.append(q)
            
        return questions

    @staticmethod
    def get_room_state(room_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Gam_MatchPvP WHERE Id = %s", (room_id,))
            room = cursor.fetchone()
            
            if room and room['DatosPartida']:
                room['DatosPartida'] = json.loads(room['DatosPartida'])
            return room
        finally:
            conn.close()

    @staticmethod
    def submit_round_result(room_id, player_role, is_correct):
        # Update score/lives logic if needed
        # For Sudden Death, if is_correct is False, game might end
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            if player_role == 'PLAYER_1':
                cursor.execute("UPDATE Gam_MatchPvP SET PuntuacionJ1 = PuntuacionJ1 + %s WHERE Id = %s", (1 if is_correct else 0, room_id))
            else:
                cursor.execute("UPDATE Gam_MatchPvP SET PuntuacionJ2 = PuntuacionJ2 + %s WHERE Id = %s", (1 if is_correct else 0, room_id))
            conn.commit()
        finally:
            conn.close()
