from flask import Flask
from controllers.cita_controller import cita_bp

app = Flask(__name__)
app.register_blueprint(cita_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
