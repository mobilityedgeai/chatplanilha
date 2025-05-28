"""
Gerador de relatórios PDF para dados de viagens de motoristas.
"""

import os
from fpdf2 import FPDF
from datetime import datetime
import json
import pandas as pd
import numpy as np

class ReportPDF(FPDF):
    """Classe personalizada para geração de relatórios PDF."""
    
    def __init__(self, title="Relatório"):
        super().__init__()
        self.title = title
        # Configurar fonte padrão
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Cabeçalho do PDF."""
        # Fonte e cor do cabeçalho
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(66, 133, 244)  # Azul Google
        
        # Título
        self.cell(0, 10, self.title, 0, 1, 'C')
        
        # Data e hora
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1, 'R')
        
        # Linha separadora
        self.ln(5)
        self.set_draw_color(66, 133, 244)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(10)
        
    def footer(self):
        """Rodapé do PDF."""
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')
        
    def chapter_title(self, title):
        """Título de capítulo."""
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(66, 133, 244)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)
        
    def chapter_body(self, text):
        """Corpo de texto."""
        self.set_font('helvetica', '', 11)
        self.set_text_color(0)
        self.multi_cell(0, 5, text)
        self.ln()
        
    def add_table(self, headers, data, col_widths=None):
        """Adiciona uma tabela ao PDF."""
        # Configurar cores
        self.set_fill_color(66, 133, 244)
        self.set_text_color(255)
        self.set_draw_color(66, 133, 244)
        self.set_line_width(0.3)
        self.set_font('helvetica', 'B', 10)
        
        # Calcular larguras das colunas se não fornecidas
        if col_widths is None:
            col_widths = [self.w / len(headers) - 10] * len(headers)
        
        # Cabeçalho da tabela
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, str(header), 1, 0, 'C', 1)
        self.ln()
        
        # Dados da tabela
        self.set_fill_color(224, 235, 255)
        self.set_text_color(0)
        self.set_font('helvetica', '', 10)
        
        fill = False
        for row in data:
            for i, cell in enumerate(row):
                # Formatar valores numéricos
                if isinstance(cell, (int, float)):
                    if isinstance(cell, int):
                        cell_text = str(cell)
                    else:
                        cell_text = f"{cell:.2f}"
                else:
                    cell_text = str(cell)
                
                # Limitar tamanho do texto
                if len(cell_text) > 20:
                    cell_text = cell_text[:17] + "..."
                
                self.cell(col_widths[i], 6, cell_text, 1, 0, 'L', fill)
            self.ln()
            fill = not fill
        
        self.ln(5)
        
    def add_chart_placeholder(self, title, description):
        """Adiciona um espaço para gráfico (placeholder)."""
        self.chapter_title(title)
        self.chapter_body(description)
        
        # Desenhar retângulo como placeholder
        self.set_draw_color(200, 200, 200)
        self.set_fill_color(240, 240, 240)
        self.rect(20, self.get_y(), self.w - 40, 60, 'DF')
        
        # Texto no centro do placeholder
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(128)
        self.set_xy(20, self.get_y() + 25)
        self.cell(self.w - 40, 10, 'Gráfico seria gerado aqui em uma implementação completa', 0, 1, 'C')
        
        self.ln(65)  # Espaço após o placeholder


def generate_pdf(data, report_type, output_path):
    """
    Gera um relatório PDF com base nos dados fornecidos.
    
    Args:
        data: Dados para o relatório
        report_type: Tipo de relatório ('motoristas', 'viagens', 'scores', 'geral')
        output_path: Caminho para salvar o PDF
    """
    # Definir título com base no tipo de relatório
    titles = {
        'motoristas': 'Relatório de Motoristas',
        'viagens': 'Relatório de Viagens',
        'scores': 'Relatório de Scores de Motoristas',
        'geral': 'Relatório Geral de Dados'
    }
    
    title = titles.get(report_type, 'Relatório')
    
    # Criar PDF
    pdf = ReportPDF(title)
    pdf.add_page()
    
    # Adicionar conteúdo com base no tipo de relatório
    if report_type == 'motoristas':
        _generate_drivers_report(pdf, data)
    elif report_type == 'viagens':
        _generate_trips_report(pdf, data)
    elif report_type == 'scores':
        _generate_scores_report(pdf, data)
    elif report_type == 'geral':
        _generate_general_report(pdf, data)
    else:
        pdf.chapter_title('Tipo de relatório não reconhecido')
        pdf.chapter_body(f'O tipo de relatório "{report_type}" não é suportado.')
    
    # Salvar PDF
    pdf.output(output_path)
    
    return output_path


def _generate_drivers_report(pdf, data):
    """Gera relatório de motoristas."""
    # Introdução
    pdf.chapter_title('Análise de Motoristas')
    pdf.chapter_body(
        'Este relatório apresenta uma análise dos motoristas da frota, '
        'incluindo estatísticas de viagens, distâncias percorridas e outros indicadores relevantes.'
    )
    pdf.ln(5)
    
    # Verificar se há dados
    if not data or 'data' not in data or not data['data']:
        pdf.chapter_body('Não há dados disponíveis para este relatório.')
        return
    
    # Extrair dados
    drivers_data = data['data']
    columns = data.get('columns', [])
    
    # Limitar número de motoristas para o relatório
    max_drivers = 20
    if len(drivers_data) > max_drivers:
        pdf.chapter_body(f'Mostrando os primeiros {max_drivers} motoristas de um total de {len(drivers_data)}.')
        drivers_data = drivers_data[:max_drivers]
    
    # Selecionar colunas relevantes
    relevant_cols = []
    for col in columns:
        if any(term in col.lower() for term in ['motorista', 'condutor', 'driver']):
            relevant_cols.append(col)
    
    # Adicionar algumas métricas se disponíveis
    for col in columns:
        if any(term in col.lower() for term in ['viagem', 'trip', 'distancia', 'km', 'tempo', 'time']):
            if len(relevant_cols) < 5:  # Limitar a 5 colunas
                relevant_cols.append(col)
    
    # Se não encontrou colunas relevantes, usar as 5 primeiras
    if not relevant_cols and columns:
        relevant_cols = columns[:min(5, len(columns))]
    
    # Preparar dados para a tabela
    table_headers = relevant_cols
    table_data = []
    for driver in drivers_data:
        row = []
        for col in relevant_cols:
            row.append(driver.get(col, ''))
        table_data.append(row)
    
    # Adicionar tabela
    pdf.chapter_title('Dados dos Motoristas')
    pdf.add_table(table_headers, table_data)
    
    # Adicionar placeholder para gráfico
    pdf.add_chart_placeholder(
        'Distribuição de Viagens por Motorista',
        'Este gráfico mostraria a distribuição do número de viagens realizadas por cada motorista.'
    )


def _generate_trips_report(pdf, data):
    """Gera relatório de viagens."""
    # Introdução
    pdf.chapter_title('Análise de Viagens')
    pdf.chapter_body(
        'Este relatório apresenta uma análise das viagens realizadas pela frota, '
        'incluindo origens, destinos, distâncias, tempos e outros indicadores relevantes.'
    )
    pdf.ln(5)
    
    # Verificar se há dados
    if not data or 'data' not in data or not data['data']:
        pdf.chapter_body('Não há dados disponíveis para este relatório.')
        return
    
    # Extrair dados
    trips_data = data['data']
    columns = data.get('columns', [])
    
    # Limitar número de viagens para o relatório
    max_trips = 20
    if len(trips_data) > max_trips:
        pdf.chapter_body(f'Mostrando as primeiras {max_trips} viagens de um total de {len(trips_data)}.')
        trips_data = trips_data[:max_trips]
    
    # Preparar dados para a tabela
    table_headers = columns[:min(5, len(columns))]  # Limitar a 5 colunas
    table_data = []
    for trip in trips_data:
        row = []
        for col in table_headers:
            row.append(trip.get(col, ''))
        table_data.append(row)
    
    # Adicionar tabela
    pdf.chapter_title('Dados das Viagens')
    pdf.add_table(table_headers, table_data)
    
    # Adicionar placeholder para gráfico
    pdf.add_chart_placeholder(
        'Distribuição de Distâncias de Viagens',
        'Este gráfico mostraria a distribuição das distâncias percorridas nas viagens.'
    )


def _generate_scores_report(pdf, data):
    """Gera relatório de scores de motoristas."""
    # Introdução
    pdf.chapter_title('Análise de Scores de Motoristas')
    pdf.chapter_body(
        'Este relatório apresenta uma análise dos scores de desempenho dos motoristas da frota, '
        'incluindo métricas de segurança, eficiência e outros indicadores relevantes.'
    )
    pdf.ln(5)
    
    # Verificar se há dados
    if not data or 'data' not in data or not data['data']:
        pdf.chapter_body('Não há dados disponíveis para este relatório.')
        return
    
    # Extrair dados
    scores_data = data['data']
    columns = data.get('columns', [])
    
    # Limitar número de motoristas para o relatório
    max_drivers = 20
    if len(scores_data) > max_drivers:
        pdf.chapter_body(f'Mostrando os primeiros {max_drivers} motoristas de um total de {len(scores_data)}.')
        scores_data = scores_data[:max_drivers]
    
    # Selecionar colunas relevantes
    relevant_cols = []
    for col in columns:
        if any(term in col.lower() for term in ['motorista', 'condutor', 'driver']):
            relevant_cols.append(col)
    
    # Adicionar colunas de score
    for col in columns:
        if any(term in col.lower() for term in ['score', 'pontuação', 'rating']):
            if len(relevant_cols) < 5:  # Limitar a 5 colunas
                relevant_cols.append(col)
    
    # Se não encontrou colunas relevantes, usar as 5 primeiras
    if not relevant_cols and columns:
        relevant_cols = columns[:min(5, len(columns))]
    
    # Preparar dados para a tabela
    table_headers = relevant_cols
    table_data = []
    for driver in scores_data:
        row = []
        for col in relevant_cols:
            row.append(driver.get(col, ''))
        table_data.append(row)
    
    # Adicionar tabela
    pdf.chapter_title('Scores dos Motoristas')
    pdf.add_table(table_headers, table_data)
    
    # Adicionar placeholder para gráfico
    pdf.add_chart_placeholder(
        'Distribuição de Scores Gerais',
        'Este gráfico mostraria a distribuição dos scores gerais dos motoristas.'
    )


def _generate_general_report(pdf, data):
    """Gera relatório geral com estatísticas."""
    # Introdução
    pdf.chapter_title('Relatório Geral de Dados')
    pdf.chapter_body(
        'Este relatório apresenta uma visão geral dos dados da frota, '
        'incluindo estatísticas resumidas, distribuições e outros indicadores relevantes.'
    )
    pdf.ln(5)
    
    # Verificar se há dados
    if not data or 'metadata' not in data:
        pdf.chapter_body('Não há dados disponíveis para este relatório.')
        return
    
    # Extrair metadados
    metadata = data['metadata']
    
    # Informações gerais
    pdf.chapter_title('Informações Gerais')
    info_text = f"""
    • Número de registros: {metadata.get('num_rows', 'N/A')}
    • Número de colunas: {metadata.get('num_columns', 'N/A')}
    • Tamanho em memória: {metadata.get('memory_usage', 'N/A'):.2f} MB
    • Arquivo: {metadata.get('file_name', 'N/A')}
    """
    pdf.chapter_body(info_text)
    pdf.ln(5)
    
    # Colunas disponíveis
    pdf.chapter_title('Colunas Disponíveis')
    columns = metadata.get('columns', [])
    column_types = metadata.get('column_types', {})
    
    col_text = ""
    for col in columns:
        col_type = column_types.get(col, 'desconhecido')
        col_text += f"• {col} (tipo: {col_type})\n"
    
    pdf.chapter_body(col_text)
    pdf.ln(5)
    
    # Amostra de dados
    if 'sample' in data:
        pdf.chapter_title('Amostra de Dados')
        sample = data['sample']
        
        if sample:
            # Extrair cabeçalhos
            headers = list(sample[0].keys())[:5]  # Limitar a 5 colunas
            
            # Preparar dados
            table_data = []
            for row in sample:
                table_row = []
                for header in headers:
                    table_row.append(row.get(header, ''))
                table_data.append(table_row)
            
            # Adicionar tabela
            pdf.add_table(headers, table_data)
        else:
            pdf.chapter_body('Não há dados de amostra disponíveis.')
    
    # Estatísticas resumidas
    if 'summary' in data and 'numeric' in data['summary']:
        pdf.chapter_title('Estatísticas Resumidas')
        
        numeric_stats = data['summary']['numeric']
        for col, stats in numeric_stats.items():
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(0, 6, f"Coluna: {col}", 0, 1)
            pdf.set_font('helvetica', '', 10)
            
            stats_text = f"""
            • Média: {stats.get('mean', 'N/A'):.2f}
            • Mínimo: {stats.get('min', 'N/A'):.2f}
            • Máximo: {stats.get('max', 'N/A'):.2f}
            • Desvio Padrão: {stats.get('std', 'N/A'):.2f}
            """
            pdf.multi_cell(0, 5, stats_text)
            pdf.ln(3)
    
    # Adicionar placeholder para gráfico
    pdf.add_chart_placeholder(
        'Visão Geral dos Dados',
        'Este gráfico mostraria uma visão geral das principais métricas dos dados.'
    )
