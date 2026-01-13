from flask import Flask
from infrastructure.data import init_db
from web.routes import weather_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(weather_bp)
    init_db()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
