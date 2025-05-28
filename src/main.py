"""
Arquivo principal da aplicação Flask.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env, se existir
load_dotenv()

# Configurar logging mais detalhado
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Verificar se a chave da API OpenAI está definida
if not os.getenv("OPENAI_API_KEY"):
    logger.warning("OPENAI_API_KEY não encontrada nas variáveis de ambiente. Algumas funcionalidades podem não funcionar.")

try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

    # Criar diretórios necessários
    os.makedirs(os.path.join(os.path.dirname(__file__), 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'reports'), exist_ok=True)

    # Inicializar aplicação Flask
    from flask import Flask, render_template, jsonify, request, send_from_directory
    app = Flask(__name__)
    
    logger.info("Inicializando componentes da aplicação...")
    
    try:
        from src.services.data_processor import DataProcessor
        from src.services.chat_engine import ChatEngine
        from src.routes.upload import upload_bp
        from src.routes.chat import chat_bp
        from src.routes.reports import reports_bp

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
        
        logger.info("Componentes da aplicação inicializados com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar componentes da aplicação: {str(e)}")
        # Continuar mesmo com erro, para permitir diagnóstico via interface

    # Rota principal
    @app.route('/')
    def index():
        try:
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Erro ao renderizar template index.html: {str(e)}")
            return jsonify({"error": "Erro ao carregar a página inicial", "details": str(e)}), 500

    # Rota para arquivos estáticos
    @app.route('/static/<path:path>')
    def serve_static(path):
        try:
            return send_from_directory('static', path)
        except Exception as e:
            logger.error(f"Erro ao servir arquivo estático {path}: {str(e)}")
            return jsonify({"error": "Arquivo não encontrado"}), 404

    # Rota de status da API
    @app.route('/api/status')
    def api_status():
        try:
            return jsonify({
                'status': 'online',
                'data_loaded': hasattr(data_processor, 'data') and data_processor.data is not None,
                'metadata': data_processor.get_metadata() if hasattr(data_processor, 'data') and data_processor.data is not None else None
            })
        except Exception as e:
            logger.error(f"Erro ao verificar status da API: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

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
        logger.error(f"Erro interno do servidor: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor',
            'details': str(error) if app.debug else None
        }), 500

    # Rota de diagnóstico
    @app.route('/debug')
    def debug_info():
        return jsonify({
            'environment': dict(os.environ),
            'python_version': sys.version,
            'sys_path': sys.path,
            'app_config': {k: str(v) for k, v in app.config.items() if k not in ('DATA_PROCESSOR', 'CHAT_ENGINE')}
        })

except Exception as e:
    logger.critical(f"Erro fatal durante inicialização da aplicação: {str(e)}")
    # Criar uma aplicação mínima para mostrar o erro
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error_index():
        return jsonify({"status": "error", "message": f"Erro fatal durante inicialização: {str(e)}"}), 500

# Executar aplicação
if __name__ == '__main__':
    # Definir host como 0.0.0.0 para permitir acesso externo
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
