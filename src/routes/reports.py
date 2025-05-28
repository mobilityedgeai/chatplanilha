"""
Rotas para geração de relatórios em PDF e Excel.
"""

from flask import Blueprint, request, jsonify, current_app, send_file
import os
import uuid
from datetime import datetime

# Criar blueprint
reports_bp = Blueprint('reports', __name__)

# Configurações de relatórios
REPORTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')

# Garantir que o diretório de relatórios existe
os.makedirs(REPORTS_FOLDER, exist_ok=True)

@reports_bp.route('/api/reports/generate', methods=['POST'])
def generate_report():
    """
    Endpoint para gerar relatórios em PDF ou Excel.
    """
    # Verificar se há dados na requisição
    if not request.json:
        return jsonify({
            'success': False,
            'error': 'Dados não fornecidos'
        }), 400
    
    # Obter parâmetros
    report_type = request.json.get('type', 'geral')  # geral, motoristas, viagens, scores
    format_type = request.json.get('format', 'pdf')  # pdf, excel
    
    try:
        # Obter o motor de chat e processador de dados
        chat_engine = current_app.config['CHAT_ENGINE']
        data_processor = current_app.config['DATA_PROCESSOR']
        
        # Verificar se há dados carregados
        if data_processor.data is None:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado carregado'
            }), 404
        
        # Gerar dados para o relatório
        report_data = chat_engine.generate_report_data(report_type)
        
        if report_data['error']:
            return jsonify({
                'success': False,
                'error': report_data['error']
            }), 500
        
        # Gerar nome de arquivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{report_type}_{timestamp}"
        
        # Gerar relatório no formato solicitado
        if format_type.lower() == 'pdf':
            # Importar gerador de PDF
            from src.services.pdf_generator import generate_pdf
            
            # Gerar PDF
            pdf_path = os.path.join(REPORTS_FOLDER, f"{filename}.pdf")
            generate_pdf(report_data['data'], report_type, pdf_path)
            
            return jsonify({
                'success': True,
                'message': 'Relatório PDF gerado com sucesso',
                'filename': f"{filename}.pdf",
                'path': f"/api/reports/download/{filename}.pdf"
            }), 200
            
        elif format_type.lower() == 'excel':
            # Importar gerador de Excel
            from src.services.excel_generator import generate_excel
            
            # Gerar Excel
            excel_path = os.path.join(REPORTS_FOLDER, f"{filename}.xlsx")
            generate_excel(report_data['data'], report_type, excel_path)
            
            return jsonify({
                'success': True,
                'message': 'Relatório Excel gerado com sucesso',
                'filename': f"{filename}.xlsx",
                'path': f"/api/reports/download/{filename}.xlsx"
            }), 200
            
        else:
            return jsonify({
                'success': False,
                'error': f'Formato de relatório não suportado: {format_type}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao gerar relatório: {str(e)}'
        }), 500

@reports_bp.route('/api/reports/download/<filename>', methods=['GET'])
def download_report(filename):
    """
    Endpoint para download de relatórios gerados.
    """
    try:
        file_path = os.path.join(REPORTS_FOLDER, filename)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'Arquivo não encontrado'
            }), 404
        
        # Determinar o tipo de conteúdo
        if filename.endswith('.pdf'):
            mimetype = 'application/pdf'
        elif filename.endswith('.xlsx'):
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        else:
            mimetype = 'application/octet-stream'
        
        # Enviar o arquivo
        return send_file(
            file_path,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao baixar relatório: {str(e)}'
        }), 500

@reports_bp.route('/api/reports/list', methods=['GET'])
def list_reports():
    """
    Endpoint para listar relatórios disponíveis.
    """
    try:
        # Listar arquivos no diretório de relatórios
        files = []
        for filename in os.listdir(REPORTS_FOLDER):
            if filename.endswith('.pdf') or filename.endswith('.xlsx'):
                file_path = os.path.join(REPORTS_FOLDER, filename)
                file_stats = os.stat(file_path)
                
                files.append({
                    'filename': filename,
                    'path': f"/api/reports/download/{filename}",
                    'size': file_stats.st_size,
                    'created': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                    'type': 'PDF' if filename.endswith('.pdf') else 'Excel'
                })
        
        # Ordenar por data de criação (mais recente primeiro)
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'reports': files
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao listar relatórios: {str(e)}'
        }), 500
