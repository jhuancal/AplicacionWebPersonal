import os
import time
import uuid
from functools import wraps
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from db import get_db_connection
from auth.decorators import login_required

from repositories.producto import ProductoRepository
from repositories.producto import ProductoRepository
from repositories.jugador import JugadorRepository
from repositories.persona import PersonaRepository

from entities.jugador import Jugador
from entities.producto import Producto
from entities.persona import Persona

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

# Admin Pages Routes
@admin_bp.route("/admin/administracion/producto")
@login_required
def admin_producto():
    user = session.get('user_data')
    return render_template("admin/Administracion/producto.html", user=user)

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


@admin_bp.route("/edit_product/<string:id>")
@login_required
def edit_product(id):
    conn = get_db_connection()
    repo = ProductoRepository(conn)
    product = repo.get_by_id(id)
    conn.close()
    if product:
        return render_template("admin/edit_product.html", product=product)
    return "Product not found", 404

@admin_bp.route("/update_product/<string:id>", methods=['POST'])
@login_required
def update_product(id):
    name = request.form['name']
    description = request.form['description']
    price_regular = request.form['price_regular']
    price_sale = request.form['price_sale']
    discount = request.form['discount']
    arrival_day = request.form['arrival_day']
    image_url = request.form['image_url']

    conn = get_db_connection()
    repo = ProductoRepository(conn)
    repo.update(id, 
                Nombre=name, 
                Descripcion=description, 
                PrecioRegular=price_regular, 
                PrecioVenta=price_sale, 
                Descuento=discount, 
                DiaLlegada=arrival_day, 
                UrlImagen=image_url)
    conn.close()
    return redirect(url_for('admin.dashboard')) # Updated url_for

# Entity-Repository Mapping
def get_repo_and_entity(entity_name, conn):
    if entity_name == 'adm_administracion_producto':
        return ProductoRepository(conn), Producto
    elif entity_name == 'seg_seguridad_jugador':
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
