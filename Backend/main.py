from flask import Flask
from controllers.cita_controller import cita_bp
from controllers.users_controller import users_bp
from flask_cors import CORS

# Servir archivos estáticos desde la carpeta frontend
app = Flask(__name__, static_folder='frontend', static_url_path='')
# Habilitar CORS para llamadas desde el frontend en desarrollo
CORS(app)
app.register_blueprint(cita_bp)
app.register_blueprint(users_bp)


@app.route('/')
def index():
    # Devuelve frontend/index.html
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
