"""
Módulo para processamento de dados de planilhas.
"""

import os
import pandas as pd
import numpy as np
import json
import math
from datetime import datetime

class DataProcessor:
    """
    Classe para processamento de dados de planilhas.
    """
    
    def __init__(self):
        """
        Inicializa o processador de dados.
        """
        self.data = None
        self.metadata = None
        self.file_path = None
    
    def load_excel(self, file_path):
        """
        Carrega dados de um arquivo Excel.
        
        Args:
            file_path (str): Caminho para o arquivo Excel.
            
        Returns:
            bool: True se o carregamento foi bem-sucedido, False caso contrário.
        """
        try:
            self.file_path = file_path
            self.data = pd.read_excel(file_path)
            self.extract_metadata()
            return True
        except Exception as e:
            print(f"Erro ao carregar arquivo Excel: {str(e)}")
            return False
    
    def extract_metadata(self):
        """
        Extrai metadados dos dados carregados.
        """
        if self.data is None:
            self.metadata = None
            return
        
        self.metadata = {
            'num_rows': len(self.data),
            'num_columns': len(self.data.columns),
            'columns': list(self.data.columns),
            'file_name': os.path.basename(self.file_path) if self.file_path else None,
            'load_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_metadata(self):
        """
        Retorna os metadados dos dados carregados.
        
        Returns:
            dict: Metadados ou None se não houver dados carregados.
        """
        return self.metadata
    
    def sanitize_data(self, data):
        """
        Sanitiza os dados para garantir compatibilidade com JSON.
        
        Args:
            data: Dados a serem sanitizados (pode ser dict, list, DataFrame, Series, etc.)
            
        Returns:
            Dados sanitizados com valores NaN e Infinity substituídos por None
        """
        if isinstance(data, float) and (math.isnan(data) or math.isinf(data)):
            return None
        elif isinstance(data, dict):
            return {k: self.sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_data(v) for v in data]
        elif isinstance(data, pd.DataFrame):
            # Converte o DataFrame para dicionário e sanitiza
            return self.sanitize_data(data.to_dict(orient='records'))
        elif isinstance(data, pd.Series):
            # Converte a Series para dicionário e sanitiza
            return self.sanitize_data(data.to_dict())
        elif isinstance(data, np.ndarray):
            # Converte arrays numpy para lista e sanitiza
            return self.sanitize_data(data.tolist())
        elif isinstance(data, np.integer):
            return int(data)
        elif isinstance(data, np.floating):
            return None if math.isnan(data) or math.isinf(data) else float(data)
        else:
            return data
    
    def get_data_for_query(self, query=None):
        """
        Retorna os dados para consulta, opcionalmente filtrados.
        
        Args:
            query (str, optional): Consulta para filtrar os dados.
            
        Returns:
            dict: Dados sanitizados para consulta ou None se não houver dados carregados.
        """
        if self.data is None:
            return None
        
        if query:
            # Implementar lógica de filtragem baseada na consulta
            # Por enquanto, retorna todos os dados
            filtered_data = self.data
        else:
            filtered_data = self.data
        
        # Sanitizar os dados antes de retornar
        return self.sanitize_data(filtered_data)
    
    def to_json(self):
        """
        Converte os dados para formato JSON.
        
        Returns:
            str: Dados em formato JSON ou "{}" se não houver dados carregados.
        """
        if self.data is None:
            return json.dumps({})
        
        # Sanitizar os dados antes de converter para JSON
        sanitized_data = self.sanitize_data(self.data)
        return json.dumps(sanitized_data)
    
    def get_summary_stats(self):
        """
        Calcula estatísticas resumidas dos dados.
        
        Returns:
            dict: Estatísticas resumidas ou None se não houver dados carregados.
        """
        if self.data is None:
            return None
        
        numeric_columns = self.data.select_dtypes(include=['number']).columns
        
        stats = {}
        for col in numeric_columns:
            stats[col] = {
                'mean': self.data[col].mean(),
                'median': self.data[col].median(),
                'min': self.data[col].min(),
                'max': self.data[col].max(),
                'std': self.data[col].std()
            }
        
        # Sanitizar as estatísticas antes de retornar
        return self.sanitize_data(stats)
    
    def filter_data(self, filters):
        """
        Filtra os dados com base em critérios específicos.
        
        Args:
            filters (dict): Critérios de filtragem no formato {coluna: valor}.
            
        Returns:
            pandas.DataFrame: Dados filtrados ou None se não houver dados carregados.
        """
        if self.data is None:
            return None
        
        filtered_data = self.data.copy()
        
        for column, value in filters.items():
            if column in filtered_data.columns:
                filtered_data = filtered_data[filtered_data[column] == value]
        
        return filtered_data
    
    def get_column_values(self, column):
        """
        Retorna valores únicos de uma coluna específica.
        
        Args:
            column (str): Nome da coluna.
            
        Returns:
            list: Valores únicos da coluna ou None se a coluna não existir.
        """
        if self.data is None or column not in self.data.columns:
            return None
        
        values = self.data[column].unique().tolist()
        
        # Sanitizar os valores antes de retornar
        return self.sanitize_data(values)
