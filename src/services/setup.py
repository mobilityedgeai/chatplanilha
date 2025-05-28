"""
Módulo para criar diretórios necessários e renderizar templates.
"""

import os
from flask import render_template, send_from_directory

def setup_directories():
    """
    Cria os diretórios necessários para a aplicação.
    """
    # Diretório base da aplicação
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Diretórios necessários
    directories = [
        os.path.join(base_dir, 'uploads'),
        os.path.join(base_dir, 'reports'),
        os.path.join(base_dir, 'static', 'css'),
        os.path.join(base_dir, 'static', 'js'),
        os.path.join(base_dir, 'templates')
    ]
    
    # Criar diretórios
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    return True

def render_index():
    """
    Renderiza o template index.html ou retorna o arquivo estático.
    """
    # Verificar se existe o template
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'index.html')
    
    if os.path.exists(template_path):
        return render_template('index.html')
    else:
        # Se não existir o template, usar o arquivo estático
        return send_from_directory('static', 'index.html')
