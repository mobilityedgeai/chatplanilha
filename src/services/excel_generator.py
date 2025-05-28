"""
Gerador de relatórios Excel para dados de viagens de motoristas.
"""

import os
import xlsxwriter
from datetime import datetime
import json
import pandas as pd
import numpy as np

def generate_excel(data, report_type, output_path):
    """
    Gera um relatório Excel com base nos dados fornecidos.
    
    Args:
        data: Dados para o relatório
        report_type: Tipo de relatório ('motoristas', 'viagens', 'scores', 'geral')
        output_path: Caminho para salvar o Excel
    """
    # Criar workbook e adicionar worksheets com base no tipo de relatório
    workbook = xlsxwriter.Workbook(output_path)
    
    # Definir formatos
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4285F4',  # Azul Google
        'font_color': 'white',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })
    
    cell_format = workbook.add_format({
        'border': 1
    })
    
    number_format = workbook.add_format({
        'border': 1,
        'num_format': '#,##0.00'
    })
    
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'font_color': '#4285F4'
    })
    
    subtitle_format = workbook.add_format({
        'bold': True,
        'font_size': 12
    })
    
    # Adicionar conteúdo com base no tipo de relatório
    if report_type == 'motoristas':
        _generate_drivers_excel(workbook, data, header_format, cell_format, number_format, title_format, subtitle_format)
    elif report_type == 'viagens':
        _generate_trips_excel(workbook, data, header_format, cell_format, number_format, title_format, subtitle_format)
    elif report_type == 'scores':
        _generate_scores_excel(workbook, data, header_format, cell_format, number_format, title_format, subtitle_format)
    elif report_type == 'geral':
        _generate_general_excel(workbook, data, header_format, cell_format, number_format, title_format, subtitle_format)
    else:
        # Relatório padrão
        worksheet = workbook.add_worksheet('Relatório')
        worksheet.write(0, 0, f'Tipo de relatório não reconhecido: {report_type}', title_format)
    
    # Fechar workbook
    workbook.close()
    
    return output_path


def _generate_drivers_excel(workbook, data, header_format, cell_format, number_format, title_format, subtitle_format):
    """Gera relatório Excel de motoristas."""
    # Criar worksheet
    worksheet = workbook.add_worksheet('Motoristas')
    
    # Verificar se há dados
    if not data or 'data' not in data or not data['data']:
        worksheet.write(0, 0, 'Não há dados disponíveis para este relatório.', title_format)
        return
    
    # Extrair dados
    drivers_data = data['data']
    columns = data.get('columns', [])
    
    # Título
    worksheet.write(0, 0, 'Relatório de Motoristas', title_format)
    worksheet.write(1, 0, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    worksheet.write(3, 0, 'Análise de Motoristas', subtitle_format)
    
    # Escrever cabeçalhos
    for col_idx, column in enumerate(columns):
        worksheet.write(5, col_idx, column, header_format)
    
    # Escrever dados
    for row_idx, driver in enumerate(drivers_data):
        for col_idx, column in enumerate(columns):
            value = driver.get(column, '')
            
            # Formatar valores numéricos
            if isinstance(value, (int, float)):
                worksheet.write(row_idx + 6, col_idx, value, number_format)
            else:
                worksheet.write(row_idx + 6, col_idx, value, cell_format)
    
    # Ajustar largura das colunas
    for col_idx, column in enumerate(columns):
        worksheet.set_column(col_idx, col_idx, max(len(column) + 2, 12))
    
    # Adicionar filtros
    worksheet.autofilter(5, 0, 5 + len(drivers_data), len(columns) - 1)
    
    # Adicionar gráfico (exemplo)
    if len(drivers_data) > 0 and len(columns) > 1:
        chart = workbook.add_chart({'type': 'column'})
        
        # Encontrar coluna numérica para o gráfico
        numeric_col = None
        for col_idx, column in enumerate(columns):
            if col_idx > 0:  # Pular a primeira coluna (nome do motorista)
                sample_value = drivers_data[0].get(column, '')
                if isinstance(sample_value, (int, float)):
                    numeric_col = col_idx
                    break
        
        if numeric_col is not None:
            chart.add_series({
                'name': f'={worksheet.name}!${chr(65 + numeric_col)}$6',
                'categories': f'={worksheet.name}!$A$7:$A${6 + min(10, len(drivers_data))}',
                'values': f'={worksheet.name}!${chr(65 + numeric_col)}$7:${chr(65 + numeric_col)}${6 + min(10, len(drivers_data))}',
            })
            
            chart.set_title({'name': f'Top 10 Motoristas por {columns[numeric_col]}'})
            chart.set_x_axis({'name': 'Motorista'})
            chart.set_y_axis({'name': columns[numeric_col]})
            
            worksheet.insert_chart('A20', chart, {'x_scale': 1.5, 'y_scale': 1})


def _generate_trips_excel(workbook, data, header_format, cell_format, number_format, title_format, subtitle_format):
    """Gera relatório Excel de viagens."""
    # Criar worksheet
    worksheet = workbook.add_worksheet('Viagens')
    
    # Verificar se há dados
    if not data or 'data' not in data or not data['data']:
        worksheet.write(0, 0, 'Não há dados disponíveis para este relatório.', title_format)
        return
    
    # Extrair dados
    trips_data = data['data']
    columns = data.get('columns', [])
    
    # Título
    worksheet.write(0, 0, 'Relatório de Viagens', title_format)
    worksheet.write(1, 0, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    worksheet.write(3, 0, 'Análise de Viagens', subtitle_format)
    
    # Escrever cabeçalhos
    for col_idx, column in enumerate(columns):
        worksheet.write(5, col_idx, column, header_format)
    
    # Escrever dados
    for row_idx, trip in enumerate(trips_data):
        for col_idx, column in enumerate(columns):
            value = trip.get(column, '')
            
            # Formatar valores numéricos
            if isinstance(value, (int, float)):
                worksheet.write(row_idx + 6, col_idx, value, number_format)
            else:
                worksheet.write(row_idx + 6, col_idx, value, cell_format)
    
    # Ajustar largura das colunas
    for col_idx, column in enumerate(columns):
        worksheet.set_column(col_idx, col_idx, max(len(column) + 2, 12))
    
    # Adicionar filtros
    worksheet.autofilter(5, 0, 5 + len(trips_data), len(columns) - 1)


def _generate_scores_excel(workbook, data, header_format, cell_format, number_format, title_format, subtitle_format):
    """Gera relatório Excel de scores de motoristas."""
    # Criar worksheet
    worksheet = workbook.add_worksheet('Scores')
    
    # Verificar se há dados
    if not data or 'data' not in data or not data['data']:
        worksheet.write(0, 0, 'Não há dados disponíveis para este relatório.', title_format)
        return
    
    # Extrair dados
    scores_data = data['data']
    columns = data.get('columns', [])
    
    # Título
    worksheet.write(0, 0, 'Relatório de Scores de Motoristas', title_format)
    worksheet.write(1, 0, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    worksheet.write(3, 0, 'Análise de Scores', subtitle_format)
    
    # Escrever cabeçalhos
    for col_idx, column in enumerate(columns):
        worksheet.write(5, col_idx, column, header_format)
    
    # Escrever dados
    for row_idx, score in enumerate(scores_data):
        for col_idx, column in enumerate(columns):
            value = score.get(column, '')
            
            # Formatar valores numéricos
            if isinstance(value, (int, float)):
                worksheet.write(row_idx + 6, col_idx, value, number_format)
            else:
                worksheet.write(row_idx + 6, col_idx, value, cell_format)
    
    # Ajustar largura das colunas
    for col_idx, column in enumerate(columns):
        worksheet.set_column(col_idx, col_idx, max(len(column) + 2, 12))
    
    # Adicionar filtros
    worksheet.autofilter(5, 0, 5 + len(scores_data), len(columns) - 1)
    
    # Adicionar gráfico de scores (se houver coluna de score)
    score_col = None
    for col_idx, column in enumerate(columns):
        if 'score' in column.lower():
            score_col = col_idx
            break
    
    if score_col is not None and len(scores_data) > 0:
        chart = workbook.add_chart({'type': 'bar'})
        
        chart.add_series({
            'name': f'={worksheet.name}!${chr(65 + score_col)}$6',
            'categories': f'={worksheet.name}!$A$7:$A${6 + min(10, len(scores_data))}',
            'values': f'={worksheet.name}!${chr(65 + score_col)}$7:${chr(65 + score_col)}${6 + min(10, len(scores_data))}',
        })
        
        chart.set_title({'name': f'Top 10 Motoristas por {columns[score_col]}'})
        chart.set_x_axis({'name': 'Motorista'})
        chart.set_y_axis({'name': columns[score_col]})
        
        worksheet.insert_chart('A20', chart, {'x_scale': 1.5, 'y_scale': 1})


def _generate_general_excel(workbook, data, header_format, cell_format, number_format, title_format, subtitle_format):
    """Gera relatório Excel geral com estatísticas."""
    # Criar worksheets
    info_sheet = workbook.add_worksheet('Informações Gerais')
    stats_sheet = workbook.add_worksheet('Estatísticas')
    sample_sheet = workbook.add_worksheet('Amostra')
    
    # Verificar se há dados
    if not data or 'metadata' not in data:
        info_sheet.write(0, 0, 'Não há dados disponíveis para este relatório.', title_format)
        return
    
    # Extrair metadados
    metadata = data['metadata']
    
    # === Informações Gerais ===
    info_sheet.write(0, 0, 'Relatório Geral de Dados', title_format)
    info_sheet.write(1, 0, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    
    # Informações básicas
    info_sheet.write(3, 0, 'Informações Básicas', subtitle_format)
    
    info_rows = [
        ('Número de registros', metadata.get('num_rows', 'N/A')),
        ('Número de colunas', metadata.get('num_columns', 'N/A')),
        ('Tamanho em memória (MB)', metadata.get('memory_usage', 'N/A')),
        ('Arquivo', metadata.get('file_name', 'N/A'))
    ]
    
    for row_idx, (label, value) in enumerate(info_rows):
        info_sheet.write(row_idx + 5, 0, label, cell_format)
        
        if isinstance(value, (int, float)):
            info_sheet.write(row_idx + 5, 1, value, number_format)
        else:
            info_sheet.write(row_idx + 5, 1, value, cell_format)
    
    # Colunas disponíveis
    info_sheet.write(10, 0, 'Colunas Disponíveis', subtitle_format)
    
    columns = metadata.get('columns', [])
    column_types = metadata.get('column_types', {})
    
    info_sheet.write(12, 0, 'Nome da Coluna', header_format)
    info_sheet.write(12, 1, 'Tipo de Dados', header_format)
    
    for row_idx, column in enumerate(columns):
        col_type = column_types.get(column, 'desconhecido')
        info_sheet.write(row_idx + 13, 0, column, cell_format)
        info_sheet.write(row_idx + 13, 1, col_type, cell_format)
    
    # Ajustar largura das colunas
    info_sheet.set_column(0, 0, 30)
    info_sheet.set_column(1, 1, 20)
    
    # === Estatísticas ===
    stats_sheet.write(0, 0, 'Estatísticas Resumidas', title_format)
    
    if 'summary' in data and 'numeric' in data['summary']:
        numeric_stats = data['summary']['numeric']
        
        # Cabeçalhos
        stats_sheet.write(2, 0, 'Coluna', header_format)
        stats_sheet.write(2, 1, 'Média', header_format)
        stats_sheet.write(2, 2, 'Mínimo', header_format)
        stats_sheet.write(2, 3, 'Máximo', header_format)
        stats_sheet.write(2, 4, 'Desvio Padrão', header_format)
        
        # Dados
        row_idx = 3
        for col, stats in numeric_stats.items():
            stats_sheet.write(row_idx, 0, col, cell_format)
            stats_sheet.write(row_idx, 1, stats.get('mean', 'N/A'), number_format)
            stats_sheet.write(row_idx, 2, stats.get('min', 'N/A'), number_format)
            stats_sheet.write(row_idx, 3, stats.get('max', 'N/A'), number_format)
            stats_sheet.write(row_idx, 4, stats.get('std', 'N/A'), number_format)
            row_idx += 1
        
        # Ajustar largura das colunas
        stats_sheet.set_column(0, 0, 30)
        stats_sheet.set_column(1, 4, 15)
        
        # Adicionar gráfico de estatísticas
        if row_idx > 3:  # Se houver pelo menos uma linha de dados
            chart = workbook.add_chart({'type': 'column'})
            
            chart.add_series({
                'name': 'Média',
                'categories': f'=Estatísticas!$A$4:$A${row_idx - 1}',
                'values': f'=Estatísticas!$B$4:$B${row_idx - 1}',
            })
            
            chart.set_title({'name': 'Médias por Coluna'})
            chart.set_x_axis({'name': 'Coluna'})
            chart.set_y_axis({'name': 'Valor'})
            
            stats_sheet.insert_chart('G3', chart, {'x_scale': 1.5, 'y_scale': 1})
    
    # === Amostra ===
    sample_sheet.write(0, 0, 'Amostra de Dados', title_format)
    
    if 'sample' in data and data['sample']:
        sample = data['sample']
        
        # Extrair cabeçalhos
        headers = list(sample[0].keys())
        
        # Escrever cabeçalhos
        for col_idx, header in enumerate(headers):
            sample_sheet.write(2, col_idx, header, header_format)
        
        # Escrever dados
        for row_idx, row in enumerate(sample):
            for col_idx, header in enumerate(headers):
                value = row.get(header, '')
                
                # Formatar valores numéricos
                if isinstance(value, (int, float)):
                    sample_sheet.write(row_idx + 3, col_idx, value, number_format)
                else:
                    sample_sheet.write(row_idx + 3, col_idx, value, cell_format)
        
        # Ajustar largura das colunas
        for col_idx, header in enumerate(headers):
            sample_sheet.set_column(col_idx, col_idx, max(len(header) + 2, 12))
        
        # Adicionar filtros
        sample_sheet.autofilter(2, 0, 2 + len(sample), len(headers) - 1)
