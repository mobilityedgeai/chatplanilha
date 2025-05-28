"""
Rotas para upload de arquivos Excel.
"""

from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
import uuid

# Criar blueprint
upload_bp = Blueprint('upload', __name__)

# Configurações de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Garantir que o diretório de uploads existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Endpoint para upload de arquivos Excel.
    """
    # Verificar se há arquivo na requisição
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'Nenhum arquivo enviado'
        }), 400
    
    file = request.files['file']
    
    # Verificar se o usuário selecionou um arquivo
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'Nenhum arquivo selecionado'
        }), 400
    
    # Verificar se o arquivo tem extensão permitida
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'Formato de arquivo não permitido. Use: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # Gerar nome de arquivo seguro e único
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Salvar o arquivo
        file.save(filepath)
        
        # Carregar o arquivo no processador de dados
        data_processor = current_app.config['DATA_PROCESSOR']
        success = data_processor.load_data(filepath)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Erro ao processar o arquivo'
            }), 500
        
        # Obter metadados
        metadata = data_processor.get_metadata()
        
        return jsonify({
            'success': True,
            'message': 'Arquivo carregado com sucesso',
            'filename': file.filename,
            'metadata': metadata
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar o arquivo: {str(e)}'
        }), 500
