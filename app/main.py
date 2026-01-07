import os
from flask import Flask, session, request, redirect, url_for
from flask_socketio import SocketIO
from routes import auth_bp, views_bp, api_game_bp, api_entities_bp
import events # Import our new events module

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 

# Async mode eventlet is recommended for production, but threading works for dev
socketio = SocketIO(app, async_mode='eventlet')

app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)
app.register_blueprint(api_game_bp)
app.register_blueprint(api_entities_bp)

# Register Socket Events
events.register_events(socketio)

@app.before_request
def restrict_access():
    allowed_routes = ['auth.login', 'auth.register', 'static']
    if request.endpoint and request.endpoint not in allowed_routes and not session.get('user_data'):
        if request.endpoint == 'static' or (request.path and request.path.startswith('/static')):
             return
        return redirect(url_for('auth.login'))

@app.context_processor
def inject_user():
    return dict(user=session.get('user_data'))

if __name__ == "__main__":
    try:
        from init_db import init_db
        init_db()
    except Exception as e:
        print(f"DB Init failed: {e}")
    port = int(os.environ.get("PORT", 5000))
    # Use socketio.run instead of app.run
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
