"""
Módulo para processamento de dados de planilhas Excel.
Responsável por carregar, processar e fornecer acesso aos dados de viagens de motoristas.
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List, Any, Optional, Tuple
import json

class DataProcessor:
    """
    Classe para processamento de dados de planilhas Excel com informações de viagens de motoristas.
    """
    
    def __init__(self):
        """Inicializa o processador de dados."""
        self.data = None
        self.file_path = None
        self.summary_stats = {}
        self.column_types = {}
        self.metadata = {}
    
    def load_data(self, file_path: str) -> bool:
        """
        Carrega dados de um arquivo Excel.
        
        Args:
            file_path: Caminho para o arquivo Excel
            
        Returns:
            bool: True se o carregamento foi bem-sucedido, False caso contrário
        """
        try:
            self.file_path = file_path
            # Usar engine openpyxl para arquivos .xlsx
            self.data = pd.read_excel(file_path, engine='openpyxl')
            
            # Processar metadados e estatísticas básicas
            self._process_metadata()
            self._calculate_summary_stats()
            
            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            return False
    
    def _process_metadata(self):
        """Processa metadados do DataFrame."""
        if self.data is not None:
            self.metadata = {
                'num_rows': len(self.data),
                'num_columns': len(self.data.columns),
                'columns': list(self.data.columns),
                'memory_usage': self.data.memory_usage(deep=True).sum() / (1024 * 1024),  # MB
                'file_name': os.path.basename(self.file_path) if self.file_path else None
            }
            
            # Identificar tipos de colunas
            self.column_types = {}
            for col in self.data.columns:
                if pd.api.types.is_numeric_dtype(self.data[col]):
                    if pd.api.types.is_integer_dtype(self.data[col]):
                        self.column_types[col] = 'integer'
                    else:
                        self.column_types[col] = 'float'
                elif pd.api.types.is_datetime64_dtype(self.data[col]):
                    self.column_types[col] = 'datetime'
                else:
                    self.column_types[col] = 'text'
            
            self.metadata['column_types'] = self.column_types
    
    def _calculate_summary_stats(self):
        """Calcula estatísticas resumidas dos dados."""
        if self.data is not None:
            # Estatísticas básicas para colunas numéricas
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if not numeric_cols.empty:
                self.summary_stats['numeric'] = self.data[numeric_cols].describe().to_dict()
            
            # Contagens para colunas categóricas (limitado a 20 valores mais comuns)
            categorical_cols = [col for col in self.data.columns 
                               if col not in numeric_cols and self.data[col].nunique() < 100]
            
            self.summary_stats['categorical'] = {}
            for col in categorical_cols:
                self.summary_stats['categorical'][col] = self.data[col].value_counts().head(20).to_dict()
            
            # Informações sobre valores ausentes
            self.summary_stats['missing_values'] = self.data.isna().sum().to_dict()
    
    def get_metadata(self) -> Dict:
        """
        Retorna metadados sobre os dados carregados.
        
        Returns:
            Dict: Metadados dos dados
        """
        return self.metadata
    
    def get_summary_stats(self) -> Dict:
        """
        Retorna estatísticas resumidas dos dados.
        
        Returns:
            Dict: Estatísticas resumidas
        """
        return self.summary_stats
    
    def query_data(self, query: str) -> pd.DataFrame:
        """
        Executa uma consulta nos dados usando a sintaxe do pandas query.
        
        Args:
            query: String de consulta no formato pandas query
            
        Returns:
            pd.DataFrame: Resultado da consulta
        """
        if self.data is None:
            return pd.DataFrame()
        
        try:
            return self.data.query(query)
        except Exception as e:
            print(f"Erro na consulta: {str(e)}")
            return pd.DataFrame()
    
    def get_column_data(self, column_name: str) -> List:
        """
        Retorna os dados de uma coluna específica.
        
        Args:
            column_name: Nome da coluna
            
        Returns:
            List: Dados da coluna
        """
        if self.data is None or column_name not in self.data.columns:
            return []
        
        return self.data[column_name].tolist()
    
    def get_data_sample(self, n: int = 5) -> pd.DataFrame:
        """
        Retorna uma amostra dos dados.
        
        Args:
            n: Número de linhas na amostra
            
        Returns:
            pd.DataFrame: Amostra dos dados
        """
        if self.data is None:
            return pd.DataFrame()
        
        return self.data.head(n)
    
    def calculate_metrics(self, group_by: str, metric_col: str, 
                         agg_func: str = 'mean') -> pd.DataFrame:
        """
        Calcula métricas agregadas agrupando por uma coluna.
        
        Args:
            group_by: Coluna para agrupar
            metric_col: Coluna para calcular métrica
            agg_func: Função de agregação ('mean', 'sum', 'count', 'min', 'max')
            
        Returns:
            pd.DataFrame: Resultado da agregação
        """
        if self.data is None:
            return pd.DataFrame()
        
        if group_by not in self.data.columns or metric_col not in self.data.columns:
            return pd.DataFrame()
        
        try:
            return self.data.groupby(group_by).agg({metric_col: agg_func})
        except Exception as e:
            print(f"Erro ao calcular métricas: {str(e)}")
            return pd.DataFrame()
    
    def calculate_driver_scores(self) -> pd.DataFrame:
        """
        Calcula scores de motoristas com base nos dados disponíveis.
        Esta é uma função específica para o caso de uso de gestão de frota.
        
        Returns:
            pd.DataFrame: DataFrame com scores de motoristas
        """
        if self.data is None:
            return pd.DataFrame()
        
        # Verificar se existem colunas necessárias para calcular scores
        # Esta implementação é genérica e deve ser adaptada aos dados reais
        driver_col = self._find_column_by_pattern(['motorista', 'condutor', 'driver'])
        if not driver_col:
            return pd.DataFrame({'erro': ['Coluna de motorista não encontrada']})
        
        # Criar DataFrame de scores
        scores_df = pd.DataFrame()
        scores_df['motorista'] = self.data[driver_col].unique()
        
        # Calcular métricas por motorista (exemplo genérico)
        # Estas métricas devem ser adaptadas aos dados reais
        
        # Número de viagens
        scores_df['total_viagens'] = scores_df['motorista'].apply(
            lambda x: len(self.data[self.data[driver_col] == x])
        )
        
        # Se houver coluna de distância
        dist_col = self._find_column_by_pattern(['distancia', 'km', 'quilometragem', 'distance'])
        if dist_col:
            scores_df['distancia_total'] = scores_df['motorista'].apply(
                lambda x: self.data[self.data[driver_col] == x][dist_col].sum()
            )
            scores_df['distancia_media'] = scores_df['motorista'].apply(
                lambda x: self.data[self.data[driver_col] == x][dist_col].mean()
            )
        
        # Se houver coluna de tempo
        time_col = self._find_column_by_pattern(['tempo', 'duracao', 'duration', 'time'])
        if time_col:
            scores_df['tempo_total'] = scores_df['motorista'].apply(
                lambda x: self.data[self.data[driver_col] == x][time_col].sum()
            )
            scores_df['tempo_medio'] = scores_df['motorista'].apply(
                lambda x: self.data[self.data[driver_col] == x][time_col].mean()
            )
        
        # Se houver coluna de consumo/combustível
        fuel_col = self._find_column_by_pattern(['consumo', 'combustivel', 'fuel', 'consumption'])
        if fuel_col:
            scores_df['consumo_total'] = scores_df['motorista'].apply(
                lambda x: self.data[self.data[driver_col] == x][fuel_col].sum()
            )
            scores_df['consumo_medio'] = scores_df['motorista'].apply(
                lambda x: self.data[self.data[driver_col] == x][fuel_col].mean()
            )
        
        # Se houver coluna de infrações/eventos
        event_col = self._find_column_by_pattern(['infracoes', 'eventos', 'violations', 'events'])
        if event_col:
            scores_df['total_eventos'] = scores_df['motorista'].apply(
                lambda x: self.data[self.data[driver_col] == x][event_col].sum()
            )
        
        # Calcular score geral (exemplo simplificado)
        # Na prática, este cálculo seria mais complexo e baseado em pesos específicos
        score_columns = []
        
        if 'distancia_total' in scores_df.columns:
            score_columns.append('distancia_total')
        
        if 'total_viagens' in scores_df.columns:
            score_columns.append('total_viagens')
        
        if 'total_eventos' in scores_df.columns:
            # Eventos são negativos para o score
            scores_df['eventos_norm'] = 100 - (scores_df['total_eventos'] / scores_df['total_eventos'].max() * 100)
            score_columns.append('eventos_norm')
        
        if score_columns:
            # Normalizar colunas para escala 0-100
            for col in score_columns:
                if col != 'eventos_norm':  # eventos já estão normalizados
                    max_val = scores_df[col].max()
                    if max_val > 0:
                        scores_df[f'{col}_norm'] = scores_df[col] / max_val * 100
                        score_columns[score_columns.index(col)] = f'{col}_norm'
            
            # Calcular média das colunas normalizadas
            scores_df['score_geral'] = scores_df[score_columns].mean(axis=1)
        
        return scores_df
    
    def _find_column_by_pattern(self, patterns: List[str]) -> Optional[str]:
        """
        Encontra uma coluna que corresponda a um dos padrões fornecidos.
        
        Args:
            patterns: Lista de padrões para procurar nos nomes das colunas
            
        Returns:
            Optional[str]: Nome da coluna encontrada ou None
        """
        if self.data is None:
            return None
        
        for pattern in patterns:
            for col in self.data.columns:
                if pattern.lower() in col.lower():
                    return col
        
        return None
    
    def to_json(self) -> str:
        """
        Converte os dados para formato JSON.
        
        Returns:
            str: Dados em formato JSON
        """
        if self.data is None:
            return json.dumps({})
        
        return self.data.to_json(orient='records')
    
    def to_dict(self) -> List[Dict]:
        """
        Converte os dados para uma lista de dicionários.
        
        Returns:
            List[Dict]: Dados como lista de dicionários
        """
        if self.data is None:
            return []
        
        return self.data.to_dict(orient='records')
