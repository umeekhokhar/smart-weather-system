import os
from flask import Flask
from infrastructure.data import init_db
from web.routes import weather_bp

def create_app():
    # Configure static folder path
    web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')
    static_dir = os.path.join(web_dir, 'static')
    
    app = Flask(__name__, 
                static_folder=static_dir,
                static_url_path='/static')
    app.register_blueprint(weather_bp)
    
    # Ensure DB is created
    init_db()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)