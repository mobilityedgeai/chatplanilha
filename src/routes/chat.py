"""
Rotas para o chat de IA para consulta de dados.
"""

from flask import Blueprint, request, jsonify, current_app
import json

# Criar blueprint
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def process_chat():
    """
    Endpoint para processar perguntas do chat.
    """
    # Verificar se há dados na requisição
    if not request.json or 'message' not in request.json:
        return jsonify({
            'success': False,
            'error': 'Mensagem não fornecida'
        }), 400
    
    message = request.json['message']
    
    try:
        # Obter o motor de chat
        chat_engine = current_app.config['CHAT_ENGINE']
        
        # Processar a pergunta
        response = chat_engine.process_query(message)
        
        return jsonify({
            'success': True,
            'answer': response['answer'],
            'data': response['data']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar a pergunta: {str(e)}'
        }), 500

@chat_bp.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """
    Endpoint para obter o histórico de chat.
    """
    try:
        # Em uma implementação real, isso viria de um banco de dados
        # Por enquanto, retornamos um histórico vazio
        return jsonify({
            'success': True,
            'history': []
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter histórico: {str(e)}'
        }), 500

@chat_bp.route('/api/data/summary', methods=['GET'])
def get_data_summary():
    """
    Endpoint para obter um resumo dos dados carregados.
    """
    try:
        # Obter o processador de dados
        data_processor = current_app.config['DATA_PROCESSOR']
        
        # Verificar se há dados carregados
        if data_processor.data is None:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado carregado'
            }), 404
        
        # Obter metadados e estatísticas
        metadata = data_processor.get_metadata()
        summary_stats = data_processor.get_summary_stats()
        
        return jsonify({
            'success': True,
            'metadata': metadata,
            'summary': summary_stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter resumo dos dados: {str(e)}'
        }), 500

@chat_bp.route('/api/data/sample', methods=['GET'])
def get_data_sample():
    """
    Endpoint para obter uma amostra dos dados carregados.
    """
    try:
        # Obter o processador de dados
        data_processor = current_app.config['DATA_PROCESSOR']
        
        # Verificar se há dados carregados
        if data_processor.data is None:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado carregado'
            }), 404
        
        # Obter tamanho da amostra da query string (padrão: 5)
        sample_size = request.args.get('size', default=5, type=int)
        
        # Limitar tamanho da amostra
        if sample_size > 100:
            sample_size = 100
        
        # Obter amostra
        sample = data_processor.get_data_sample(sample_size)
        
        return jsonify({
            'success': True,
            'sample': sample.to_dict(orient='records'),
            'columns': sample.columns.tolist()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter amostra dos dados: {str(e)}'
        }), 500
