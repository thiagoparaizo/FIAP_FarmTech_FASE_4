from flask import Flask, render_template
from app.utils.filters import configure_template_filters
from config import Config
from pymongo import MongoClient
from app.services.init_db import inicializar_banco_dados

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar MongoDB
    mongo_client = MongoClient(app.config['MONGO_URI'])
    app.db = mongo_client.get_database()
    
    # Inicializar banco de dados com dados de exemplo (se necessário)
    with app.app_context():
        inicializar_banco_dados(app.config['MONGO_URI'])
    
    # Registrar blueprints
    from app.routes.web_routes import web_bp
    from app.routes.api_routes import api_bp
    
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Configurar tratamento de erros
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    @app.template_filter('number_format')
    def number_format_filter(number):
        """Formata um número com separadores de milhar."""
        return format(int(number), ',').replace(',', '.')
    
    configure_template_filters(app)
    
    return app