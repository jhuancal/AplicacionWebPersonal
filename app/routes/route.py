import os
import time
import uuid
import json
from functools import wraps
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from db import get_db_connection
from auth.decorators import login_required

from repositories.jugador import JugadorRepository
from repositories.persona import PersonaRepository

from entities.jugador import Jugador
from entities.persona import Persona

from repositories.experiencia_jugador import ExperienciaJugadorRepository
from repositories.racha_jugador import RachaJugadorRepository
from repositories.desafio_jugador import DesafioJugadorRepository
from repositories.rango_jugador_temporada import RangoJugadorTemporadaRepository
from repositories.avance_curso_jugador import AvanceCursoJugadorRepository
from repositories.curso import CursoRepository
from repositories.tema_curso import TemaCursoRepository
from repositories.ejercicio import EjercicioRepository
from repositories.examen_curso import ExamenCursoRepository

from auth.auth_service import AuthService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/")
def index():
    return redirect(url_for('admin.login'))

@admin_bp.before_request
def restrict_access():
    """Confirms user is logged in before allowing access to any route."""
    allowed_routes = ['admin.login', 'admin.register', 'static']
    if request.endpoint and request.endpoint not in allowed_routes and not session.get('user_data'):
        # Allow static files even if endpoint name is not exactly 'static' (e.g. blueprints)
        if request.endpoint == 'static' or request.path.startswith('/static'):
             return
        return redirect(url_for('admin.login'))

@admin_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if AuthService.validate_user(username, password):
            user_data = AuthService.get_user_details(username)
            session['user_data'] = user_data
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template("auth/login.html", error="Invalid Credentials. Access Denied.")
    
    # GET request
    if session.get('user_data'):
        return redirect(url_for('admin.dashboard'))
    return render_template("auth/login.html")

@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('admin.login'))

@admin_bp.route("/register")
def register():
    return render_template("auth/register.html")

@admin_bp.route("/admin/dashboard")
@login_required 
def dashboard():
    user = session.get('user_data')
    return render_template("game/inicio.html", user=user)

@admin_bp.route("/admin/cursos")
@login_required 
def cursos():
    user = session.get('user_data')
    return render_template("game/cursos.html", user=user)

@admin_bp.route("/admin/arenas")
@login_required 
def arenas():
    user = session.get('user_data')
    return render_template("game/arenas.html", user=user)

@admin_bp.route("/admin/ranking")
@login_required 
def ranking():
    user = session.get('user_data')
    return render_template("game/ranking.html", user=user)

@admin_bp.route("/admin/perfil")
@login_required 
def perfil():
    user = session.get('user_data')
    return render_template("game/perfil.html", user=user)

@admin_bp.route("/admin/seguridad/usuario")
@login_required
def admin_usuario():
    user = session.get('user_data')
    return render_template("admin/Seguridad/usuario.html", user=user)

@admin_bp.route("/admin/administracion/persona")
@login_required
def admin_persona():
    user = session.get('user_data')
    return render_template("admin/Administracion/persona.html", user=user)

@admin_bp.route("/admin/curso/<id>")
@login_required
def curso_detalle(id):
    user = session.get('user_data')
    conn = get_db_connection()
    
    # 1. Get Course Info
    curso_repo = CursoRepository(conn)
    curso = curso_repo.get_by_id(id)
    
    if not curso:
        conn.close()
        return "Course not found", 404
        
    # 2. Get Themes
    tema_repo = TemaCursoRepository(conn)
    temas = tema_repo.get_by_curso(id)
    
    # 3. Get Exercises for each Theme
    ejercicio_repo = EjercicioRepository(conn)
    # Convert themes to dicts to attach exercises or strict object usage?
    # Let's use a list of data structs
    temas_data = []
    for tema in temas:
        exs = ejercicio_repo.get_by_tema(tema.Id)
        temas_data.append({
            'tema': tema,
            'ejercicios': exs
        })
        
    # 4. Get Exam
    examen_repo = ExamenCursoRepository(conn)
    examen = examen_repo.get_by_curso(id)
    
    # Parse JSON questions if string
    if examen and examen.Preguntas and isinstance(examen.Preguntas, str):
        try:
            examen.Preguntas = json.loads(examen.Preguntas)
        except:
            examen.Preguntas = []

    conn.close()
    
    return render_template("game/curso_detalle.html", 
                           user=user, 
                           curso=curso, 
                           temas_data=temas_data, 
                           examen=examen)

# ==========================================
# DASHBOARD APIs
# ==========================================

@admin_bp.route("/api/user/hud", methods=['GET'])
@login_required
def api_user_hud():
    user = session.get('user_data')
    # Mocking Points/Rank for now or fetching from DB
    return jsonify({
        "username": user.get('Username', 'Player'),
        "rank": "GOLD III", # Todo: fetch real rank
        "points": 1250,      # Todo: fetch real points
        "profile_pic": "/static/img/default_avatar.png"
    })

@admin_bp.route("/api/dashboard/stats", methods=['GET'])
@login_required
def api_dashboard_stats():
    user = session.get('user_data')
    user_id = user.get('Id')
    conn = get_db_connection()
    
    # 1. Get Rank
    rank_repo = RangoJugadorTemporadaRepository(conn)
    # Assuming get_all returns list, we filter (ideal would be get_by_user)
    # For now, simplistic approach:
    ranks = rank_repo.get_all() 
    my_rank = next((r for r in ranks if r.IdJugador == user_id), None)
    
    # 2. Get XP
    exp_repo = ExperienciaJugadorRepository(conn)
    exps = exp_repo.get_all()
    my_exp = next((e for e in exps if e.IdJugador == user_id), None)
    
    # 3. Get Streak
    streak_repo = RachaJugadorRepository(conn)
    streaks = streak_repo.get_all()
    my_streak = next((s for s in streaks if s.IdJugador == user_id), None)
    
    conn.close()
    
    return jsonify({
        "rank": my_rank.Rango if my_rank else "UNRANKED",
        "xp": my_exp.TotalExp if my_exp else 0,
        "streak": my_streak.RachaActual if my_streak else 0
    })

@admin_bp.route("/api/dashboard/challenge", methods=['GET'])
@login_required
def api_dashboard_challenge():
    user = session.get('user_data')
    user_id = user.get('Id')
    conn = get_db_connection()
    
    repo = DesafioJugadorRepository(conn)
    challenges = repo.get_all()
    my_challenge = next((c for c in challenges if c.IdJugador == user_id and c.Estado == 'PENDIENTE'), None)
    
    conn.close()
    
    if my_challenge:
        return jsonify(my_challenge.to_dict())
    return jsonify(None)

@admin_bp.route("/api/dashboard/progress", methods=['GET'])
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

# Entity-Repository Mapping
def get_repo_and_entity(entity_name, conn):
    if entity_name == 'seg_seguridad_jugador':
        return JugadorRepository(conn), Jugador
    elif entity_name == 'adm_administracion_persona':
        return PersonaRepository(conn), Persona
    return None, None

# Generic CRUD APIs
@admin_bp.route("/api/<entity_name>/GetAll", methods=['POST'])
def api_get_all(entity_name):
    conn = get_db_connection()
    repo, _ = get_repo_and_entity(entity_name, conn)
    if not repo:
        conn.close()
        return jsonify({"error": "Entity not found"}), 404
    data = repo.get_all()
    conn.close()
    return jsonify([d.to_dict() for d in data])

@admin_bp.route("/api/<entity_name>/CountAll", methods=['POST'])
def api_count_all(entity_name):
    data = request.get_json()
    filters = data if isinstance(data, list) else None
    
    conn = get_db_connection()
    repo, _ = get_repo_and_entity(entity_name, conn)
    if not repo:
        conn.close()
        return jsonify({"error": "Entity not found"}), 404
    count = repo.count_all(filters)
    conn.close()
    return jsonify([count])

@admin_bp.route("/api/<entity_name>/GetPaged", methods=['POST'])
def api_get_paged(entity_name):
    data = request.get_json()
    start_index = data.get('startIndex', 0)
    length = data.get('length', 10)
    filters = data.get('filtros')
    order = data.get('orden')

    conn = get_db_connection()
    repo, _ = get_repo_and_entity(entity_name, conn)
    if not repo:
        conn.close()
        return jsonify({"error": "Entity not found"}), 404
    
    try:
        start_index = int(start_index)
        length = int(length)
    except:
        start_index = 0
        length = 10

    data = repo.get_paged(start_index, length, filters, order)
    conn.close()
    return jsonify(data)

@admin_bp.route("/api/<entity_name>/Insert", methods=['POST'])
def api_insert(entity_name):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
        
    conn = get_db_connection()
    repo, entity_class = get_repo_and_entity(entity_name, conn)
    if not repo:
        conn.close()
        return jsonify({"error": "Entity not found"}), 404
    
    # Add System Fields
    data['Id'] = str(uuid.uuid4())
    data['ESTADO'] = 1
    data['DISPONIBILIDAD'] = 1
    data['FECHA_CREACION'] = int(time.time() * 1000)
    data['FECHA_MODIFICACION'] = int(time.time() * 1000)
    data['USER_CREACION'] = session.get('user_data', {}).get('Username', 'SYS')
    data['USER_MODIFICACION'] = session.get('user_data', {}).get('Username', 'SYS')
    
    # Handle File Upload
    if request.files:
        file = request.files.get('Imagen')
        if file and file.filename != '':
            filename = secure_filename(f"{data['Id']}_{file.filename}")
            # Use current_app.config
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            data['UrlImagen'] = f"/static/uploads/{filename}"
    
    try:
        repo.add(**data)
        conn.close()
        return jsonify({"id": data['Id']})
    except Exception as e:
        conn.close()
        print(e)
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/api/<entity_name>/Update", methods=['PUT'])
def api_update(entity_name):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
        
    id = data.get('Id')
    if not id:
        return jsonify({"error": "Id required"}), 400
        
    conn = get_db_connection()
    repo, _ = get_repo_and_entity(entity_name, conn)
    if not repo:
        conn.close()
        return jsonify({"error": "Entity not found"}), 404
    
    data['FECHA_MODIFICACION'] = int(time.time() * 1000)
    data['USER_MODIFICACION'] = session.get('user_data', {}).get('Username', 'SYS')

    if request.files:
         file = request.files.get('Imagen')
         if file and file.filename != '':
            filename = secure_filename(f"{id}_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            data['UrlImagen'] = f"/static/uploads/{filename}"

    data_to_update = {k: v for k, v in data.items() if k != 'Id'}

    try:
        repo.update(id, **data_to_update)
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        conn.close()
        print(e)
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/api/<entity_name>/Delete", methods=['DELETE'])
def api_delete(entity_name):
    data = request.get_json()
    id = data.get('Id')
    if not id:
        return jsonify({"error": "Id required"}), 400
    
    conn = get_db_connection()
    repo, _ = get_repo_and_entity(entity_name, conn)
    if not repo:
        conn.close()
        return jsonify({"error": "Entity not found"}), 404

    try:
        repo.delete(id)
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        conn.close()
        print(e)
        return jsonify({"error": str(e)}), 500
