from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
import os
import time
from db import get_db_connection
from repositories.jugador import JugadorRepository
from repositories.persona import PersonaRepository
from entities.jugador import Jugador
from entities.persona import Persona

api_entities_bp = Blueprint('api_entities', __name__)

# Entity-Repository Mapping
def get_repo_and_entity(entity_name, conn):
    if entity_name == 'seg_seguridad_jugador':
        return JugadorRepository(conn), Jugador
    elif entity_name == 'adm_administracion_persona':
        return PersonaRepository(conn), Persona
    return None, None

# Generic CRUD APIs
@api_entities_bp.route("/api/<entity_name>/GetAll", methods=['POST'])
def api_get_all(entity_name):
    conn = get_db_connection()
    repo, _ = get_repo_and_entity(entity_name, conn)
    if not repo:
        conn.close()
        return jsonify({"error": "Entity not found"}), 404
    data = repo.get_all()
    conn.close()
    return jsonify([d.to_dict() for d in data])

@api_entities_bp.route("/api/<entity_name>/CountAll", methods=['POST'])
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

@api_entities_bp.route("/api/<entity_name>/GetPaged", methods=['POST'])
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

@api_entities_bp.route("/api/<entity_name>/Insert", methods=['POST'])
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
    
    data['USER_CREACION'] = session.get('user_data', {}).get('Username', 'SYS')
    data['USER_MODIFICACION'] = session.get('user_data', {}).get('Username', 'SYS')
    
    if request.files:
        file = request.files.get('Imagen')
        if file and file.filename != '':
            filename = secure_filename(f"{data['Id']}_{file.filename}")
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

@api_entities_bp.route("/api/<entity_name>/Update", methods=['PUT'])
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

@api_entities_bp.route("/api/<entity_name>/Delete", methods=['DELETE'])
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
