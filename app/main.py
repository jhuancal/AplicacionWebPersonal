import os
from flask import Flask, session
from routes.route import admin_bp

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 

app.register_blueprint(admin_bp)

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
    app.run(host="0.0.0.0", port=port, debug=True)
