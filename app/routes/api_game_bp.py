from flask import Blueprint, request, jsonify, session
import random
from db import get_db_connection
from auth.decorators import login_required

from repositories.experiencia_jugador import ExperienciaJugadorRepository
from repositories.racha_jugador import RachaJugadorRepository
from repositories.desafio_jugador import DesafioJugadorRepository
from repositories.rango_jugador_temporada import RangoJugadorTemporadaRepository
from repositories.avance_curso_jugador import AvanceCursoJugadorRepository
from repositories.curso import CursoRepository
from repositories.operacion_matematica import OperacionMatematicaRepository
from services.exercise_generator import ExerciseGeneratorService

api_game_bp = Blueprint('api_game', __name__)

@api_game_bp.route("/api/user/hud", methods=['GET'])
@login_required
def api_user_hud():
    user = session.get('user_data')
    return jsonify({
        "username": user.get('Username', 'Player'),
        "rank": "GOLD III", 
        "points": 1250,      
        "profile_pic": "/static/img/default_avatar.png"
    })

@api_game_bp.route("/api/dashboard/stats", methods=['GET'])
@login_required
def api_dashboard_stats():
    user = session.get('user_data')
    user_id = user.get('Id')
    conn = get_db_connection()
    
    rank_repo = RangoJugadorTemporadaRepository(conn)
    ranks = rank_repo.get_all() 
    my_rank = next((r for r in ranks if r.IdJugador == user_id), None)
    
    exp_repo = ExperienciaJugadorRepository(conn)
    exps = exp_repo.get_all()
    my_exp = next((e for e in exps if e.IdJugador == user_id), None)
    
    streak_repo = RachaJugadorRepository(conn)
    streaks = streak_repo.get_all()
    my_streak = next((s for s in streaks if s.IdJugador == user_id), None)
    
    conn.close()
    
    return jsonify({
        "rank": my_rank.Rango if my_rank else "UNRANKED",
        "xp": my_exp.TotalExp if my_exp else 0,
        "streak": my_streak.RachaActual if my_streak else 0
    })

@api_game_bp.route("/api/dashboard/challenge", methods=['GET'])
@login_required
def api_dashboard_challenge():
    user = session.get('user_data')
    user_id = user.get('Id')
    conn = get_db_connection()
    
    repo = DesafioJugadorRepository(conn)
    challenges = repo.get_all()
    my_challenge = next((c for c in challenges if c.IdJugador == user_id and c.EstadoDesafio == 'PENDIENTE'), None)
    
    conn.close()
    
    if my_challenge:
        return jsonify(my_challenge.to_dict())
    return jsonify(None)

@api_game_bp.route("/api/dashboard/progress", methods=['GET'])
@login_required
def api_dashboard_progress():
    user = session.get('user_data')
    user_id = user.get('Id')
    conn = get_db_connection()
    
    # Get active progress
    prog_repo = AvanceCursoJugadorRepository(conn)
    progs = prog_repo.get_all()
    my_prog = next((p for p in progs if p.IdJugador == user_id), None)
    
    result = None
    if my_prog:
        # Get Course Name
        course_repo = CursoRepository(conn)
        course = course_repo.get_by_id(my_prog.IdCurso)
        result = {
            "courseName": course.Nombre if course else "Unknown Course",
            "percent": float(my_prog.PorcentajeAvance)
        }
        
    conn.close()
    return jsonify(result)

@api_game_bp.route("/api/arena/generate", methods=['POST'])
@login_required
def api_arena_generate():
    data = request.get_json()
    course_id = data.get('courseId')
    
    if not course_id:
        return jsonify({"error": "Course ID required"}), 400
        
    conn = get_db_connection()
    op_repo = OperacionMatematicaRepository(conn)
    ops = op_repo.get_by_curso(course_id)
    conn.close()
    
    if not ops:
        return jsonify({"error": "No generators found for this course"}), 404
        
    op = random.choice(ops)
    
    problem = ExerciseGeneratorService.generate(op)
    return jsonify(problem)

@api_game_bp.route("/api/arena/xp", methods=['POST'])
@login_required
def api_arena_xp():
    data = request.get_json()
    amount = data.get('amount', 0)
    
    if amount <= 0:
        return jsonify({"success": False, "message": "Invalid amount"}), 400
        
    user = session.get('user_data')
    user_id = user.get('Id')
    
    conn = get_db_connection()
    exp_repo = ExperienciaJugadorRepository(conn)
    
    # Get current experience
    exps = exp_repo.get_all()
    my_exp = next((e for e in exps if e.IdJugador == user_id), None)
    
    if my_exp:
        new_total = my_exp.TotalExp + amount
        exp_repo.update(my_exp.Id, TotalExp=new_total)
    else:
        # Create new record if somehow missing (unlikely since init data exists)
        import uuid
        new_id = f"EXP-{str(uuid.uuid4())[:8]}"
        exp_repo.add(Id=new_id, IdJugador=user_id, TotalExp=amount)
        
    conn.close()
    return jsonify({"success": True, "new_total": my_exp.TotalExp + amount if my_exp else amount})
    conn.close()
    return jsonify({"success": True, "new_total": my_exp.TotalExp + amount if my_exp else amount})

@api_game_bp.route("/api/course/exam/submit", methods=['POST'])
@login_required
def api_course_exam_submit():
    import json
    data = request.get_json()
    course_id = data.get('courseId')
    answers = data.get('answers', {}) # Dict { "1": "Option A" }
    
    user = session.get('user_data')
    user_id = user.get('Id')
    
    conn = get_db_connection()
    try:
        from repositories.examen_curso import ExamenCursoRepository
        
        # 1. Get Exam
        exam_repo = ExamenCursoRepository(conn)
        exam = exam_repo.get_by_curso(course_id)
        
        if not exam:
             return jsonify({"error": "Exam not found"}), 404
             
        # 2. Grade It
        questions = []
        if exam.Preguntas and isinstance(exam.Preguntas, str):
             try:
                 questions = json.loads(exam.Preguntas)
             except:
                 questions = []
        
        total_q = len(questions)
        correct_count = 0
        
        for q in questions:
            q_id = str(q.get('id'))
            correct_ans = q.get('answer')
            user_ans = answers.get(q_id)
            if user_ans == correct_ans:
                correct_count += 1
                
        score = int((correct_count / total_q) * 100) if total_q > 0 else 0
        passed = score >= exam.NotaMinima
        
        if passed:
            # 3. Mark Course Complete (Update Avance)
            prog_repo = AvanceCursoJugadorRepository(conn)
            all_progs = prog_repo.get_all()
            # Check existing
            existing_prog = next((p for p in all_progs if p.IdJugador == user_id and p.IdCurso == course_id), None)
            
            if existing_prog:
                prog_repo.update(existing_prog.Id, PorcentajeAvance=100.00, NivelActual=10) # Max level
            else:
                # Create if not exists (rare)
                import uuid
                import time
                new_id = f"PROG-{str(uuid.uuid4())[:8]}"
                prog_repo.add(Id=new_id, IdJugador=user_id, IdCurso=course_id, NivelActual=10, PorcentajeAvance=100.00, ESTADO=1)
                
            # 4. Award XP (500 XP for Exam)
            exp_repo = ExperienciaJugadorRepository(conn)
            exps = exp_repo.get_all()
            my_exp = next((e for e in exps if e.IdJugador == user_id), None)
            
            if my_exp:
                new_exp = my_exp.TotalExp + 500
                exp_repo.update(my_exp.Id, TotalExp=new_exp)
            else:
                import uuid
                new_id = f"EXP-{str(uuid.uuid4())[:8]}"
                exp_repo.add(Id=new_id, IdJugador=user_id, TotalExp=500)
        
        return jsonify({
            "passed": passed,
            "score": score,
            "required": exam.NotaMinima
        })
        
    finally:
        conn.close()
