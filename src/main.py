"""
Arquivo principal da aplicação Flask.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, jsonify, request, send_from_directory
from src.services.data_processor import DataProcessor
from src.services.chat_engine import ChatEngine
from src.routes.upload import upload_bp
from src.routes.chat import chat_bp
from src.routes.reports import reports_bp
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar diretórios necessários
os.makedirs(os.path.join(os.path.dirname(__file__), 'uploads'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'reports'), exist_ok=True)

# Inicializar aplicação Flask
app = Flask(__name__)

# Configurar processador de dados e motor de chat
data_processor = DataProcessor()
chat_engine = ChatEngine(data_processor)

# Adicionar ao contexto da aplicação
app.config['DATA_PROCESSOR'] = data_processor
app.config['CHAT_ENGINE'] = chat_engine

# Registrar blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(reports_bp)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para arquivos estáticos
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Rota de status da API
@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'online',
        'data_loaded': data_processor.data is not None,
        'metadata': data_processor.get_metadata() if data_processor.data is not None else None
    })

# Manipulador de erros para rotas não encontradas
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint não encontrado'
    }), 404

# Manipulador de erros para erros internos
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 'Erro interno do servidor'
    }), 500

# Executar aplicação
if __name__ == '__main__':
    # Definir host como 0.0.0.0 para permitir acesso externo
    app.run(host='0.0.0.0', port=5000, debug=True)
