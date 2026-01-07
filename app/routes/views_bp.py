from flask import Blueprint, render_template, request, session, redirect, url_for
import json
from db import get_db_connection
from auth.decorators import login_required

from repositories.avance_curso_jugador import AvanceCursoJugadorRepository
from repositories.curso import CursoRepository
from repositories.tema_curso import TemaCursoRepository
from repositories.ejercicio import EjercicioRepository
from repositories.examen_curso import ExamenCursoRepository

# Keeping 'admin' name for backward compatibility with existing templates
views_bp = Blueprint('admin', __name__)

@views_bp.route("/")
def index():
    return redirect(url_for('auth.login'))

@views_bp.route("/admin/dashboard")
@login_required 
def dashboard():
    user = session.get('user_data')
    return render_template("game/inicio.html", user=user)

@views_bp.route("/admin/cursos")
@login_required 
def cursos():
    user = session.get('user_data')
    return render_template("game/cursos.html", user=user)

@views_bp.route("/admin/arenas")
@login_required 
def arenas():
    user = session.get('user_data')
    conn = get_db_connection()
    
    prog_repo = AvanceCursoJugadorRepository(conn)
    all_progs = prog_repo.get_all()
    user_progs = [p for p in all_progs if p.IdJugador == user.get('Id') and p.PorcentajeAvance == 100.00]
    
    curso_repo = CursoRepository(conn)
    completed_courses = []
    for p in user_progs:
        c = curso_repo.get_by_id(p.IdCurso)
        if c:
            completed_courses.append(c)
            
    conn.close()
    return render_template("game/arenas.html", user=user, courses=completed_courses)

@views_bp.route("/admin/arena/play")
@login_required
def arena_play():
    user = session.get('user_data')
    mode = request.args.get('mode', 'TRAINING')
    course_id = request.args.get('courseId')
    
    conn = get_db_connection()
    curso_repo = CursoRepository(conn)
    course = curso_repo.get_by_id(course_id) if course_id else None
    conn.close()
    
    if not course and mode == 'TRAINING':
        return redirect(url_for('admin.arenas'))
        
    return render_template("game/arena_game.html", user=user, mode=mode, course=course)

@views_bp.route("/admin/arena/pvp")
@login_required
def arena_pvp():
    user = session.get('user_data')
    return render_template("game/arena_pvp.html", user=user)

@views_bp.route("/admin/ranking")
@login_required 
def ranking():
    user = session.get('user_data')
    return render_template("game/ranking.html", user=user)

@views_bp.route("/admin/perfil")
@login_required 
def perfil():
    user = session.get('user_data')
    return render_template("game/perfil.html", user=user)

@views_bp.route("/admin/seguridad/usuario")
@login_required
def admin_usuario():
    user = session.get('user_data')
    return render_template("admin/Seguridad/usuario.html", user=user)

@views_bp.route("/admin/administracion/persona")
@login_required
def admin_persona():
    user = session.get('user_data')
    return render_template("admin/Administracion/persona.html", user=user)

@views_bp.route("/admin/curso/<id>")
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
