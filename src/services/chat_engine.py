"""
Motor de chat com IA para consulta de dados de viagens de motoristas.
Utiliza LangChain e OpenAI para processar perguntas em linguagem natural.
"""

import os
from typing import Dict, List, Any, Optional, Tuple
import json
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class ChatEngine:
    """
    Motor de chat com IA para consulta de dados de viagens de motoristas.
    """
    
    def __init__(self, data_processor):
        """
        Inicializa o motor de chat.
        
        Args:
            data_processor: Instância do processador de dados
        """
        self.data_processor = data_processor
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY", "sk-dummy-key")
        )
        self.setup_chain()
        
    def setup_chain(self):
        """Configura a cadeia de processamento do LangChain."""
        # Template para o sistema
        system_template = """
        Você é um assistente especializado em análise de dados de viagens de motoristas de frota.
        Sua função é responder perguntas sobre os dados com base nas informações disponíveis.
        
        Os dados contêm informações sobre viagens de motoristas, incluindo:
        - Informações sobre motoristas
        - Detalhes de viagens (distâncias, tempos, consumo)
        - Possíveis eventos ou infrações
        
        Metadados dos dados:
        {metadata}
        
        Estatísticas resumidas:
        {summary_stats}
        
        Responda de forma clara e objetiva, fornecendo análises relevantes para gestores de frota e segurança.
        Se não conseguir responder com os dados disponíveis, explique o motivo.
        """
        
        # Template para o usuário
        user_template = """
        Pergunta: {question}
        """
        
        # Criar o prompt completo
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", user_template)
        ])
        
        # Configurar a cadeia
        self.chain = (
            {
                "question": RunnablePassthrough(),
                "metadata": lambda _: json.dumps(self.data_processor.get_metadata(), indent=2),
                "summary_stats": lambda _: json.dumps(self.data_processor.get_summary_stats(), indent=2)
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def process_query(self, query: str) -> Dict:
        """
        Processa uma consulta em linguagem natural.
        
        Args:
            query: Pergunta em linguagem natural
            
        Returns:
            Dict: Resposta processada
        """
        if self.data_processor.data is None:
            return {
                "answer": "Não há dados carregados. Por favor, faça o upload de um arquivo Excel primeiro.",
                "data": None,
                "error": "Dados não carregados"
            }
        
        try:
            # Processar a pergunta com o LLM
            answer = self.chain.invoke(query)
            
            # Tentar extrair dados relevantes com base na pergunta
            relevant_data = self._extract_relevant_data(query)
            
            return {
                "answer": answer,
                "data": relevant_data,
                "error": None
            }
        except Exception as e:
            return {
                "answer": f"Ocorreu um erro ao processar sua pergunta: {str(e)}",
                "data": None,
                "error": str(e)
            }
    
    def _extract_relevant_data(self, query: str) -> Optional[Dict]:
        """
        Extrai dados relevantes com base na consulta.
        
        Args:
            query: Pergunta em linguagem natural
            
        Returns:
            Optional[Dict]: Dados relevantes ou None
        """
        # Palavras-chave para identificar o tipo de consulta
        keywords = {
            'motorista': ['motorista', 'condutor', 'driver'],
            'viagem': ['viagem', 'trajeto', 'percurso', 'trip'],
            'distância': ['distância', 'quilometragem', 'km', 'distance'],
            'tempo': ['tempo', 'duração', 'duration', 'time'],
            'consumo': ['consumo', 'combustível', 'fuel', 'consumption'],
            'evento': ['infração', 'evento', 'violation', 'event'],
            'score': ['score', 'pontuação', 'avaliação', 'rating']
        }
        
        # Identificar tipo de consulta
        query_type = None
        for key, terms in keywords.items():
            if any(term in query.lower() for term in terms):
                query_type = key
                break
        
        # Extrair dados com base no tipo de consulta
        if query_type == 'motorista':
            # Buscar dados de motoristas
            driver_col = self.data_processor._find_column_by_pattern(keywords['motorista'])
            if driver_col:
                drivers = self.data_processor.data[driver_col].unique().tolist()
                return {
                    'type': 'motoristas',
                    'data': drivers[:100]  # Limitar a 100 motoristas
                }
        
        elif query_type == 'score':
            # Calcular scores de motoristas
            scores = self.data_processor.calculate_driver_scores()
            if not scores.empty:
                return {
                    'type': 'scores',
                    'data': scores.to_dict(orient='records')
                }
        
        elif query_type in ['distância', 'tempo', 'consumo']:
            # Buscar métricas agregadas
            metric_col = self.data_processor._find_column_by_pattern(keywords[query_type])
            driver_col = self.data_processor._find_column_by_pattern(keywords['motorista'])
            
            if metric_col and driver_col:
                metrics = self.data_processor.calculate_metrics(driver_col, metric_col, 'mean')
                return {
                    'type': f'métricas_{query_type}',
                    'data': metrics.reset_index().to_dict(orient='records')
                }
        
        # Se não conseguir extrair dados específicos, retornar uma amostra
        return {
            'type': 'amostra',
            'data': self.data_processor.get_data_sample(10).to_dict(orient='records')
        }
    
    def generate_report_data(self, report_type: str) -> Dict:
        """
        Gera dados para relatórios.
        
        Args:
            report_type: Tipo de relatório ('motoristas', 'viagens', 'scores', 'geral')
            
        Returns:
            Dict: Dados para o relatório
        """
        if self.data_processor.data is None:
            return {
                "error": "Não há dados carregados",
                "data": None
            }
        
        try:
            if report_type == 'motoristas':
                # Relatório de motoristas
                driver_col = self.data_processor._find_column_by_pattern(
                    ['motorista', 'condutor', 'driver']
                )
                
                if not driver_col:
                    return {"error": "Coluna de motoristas não encontrada", "data": None}
                
                # Agrupar dados por motorista
                driver_data = self.data_processor.data.groupby(driver_col).agg({
                    col: 'count' if self.data_processor.column_types.get(col) == 'text' else 'mean'
                    for col in self.data_processor.data.columns
                    if col != driver_col and pd.api.types.is_numeric_dtype(self.data_processor.data[col])
                }).reset_index()
                
                return {
                    "error": None,
                    "data": driver_data.to_dict(orient='records'),
                    "columns": driver_data.columns.tolist()
                }
                
            elif report_type == 'scores':
                # Relatório de scores
                scores = self.data_processor.calculate_driver_scores()
                
                if scores.empty:
                    return {"error": "Não foi possível calcular scores", "data": None}
                
                return {
                    "error": None,
                    "data": scores.to_dict(orient='records'),
                    "columns": scores.columns.tolist()
                }
                
            elif report_type == 'viagens':
                # Relatório de viagens
                # Selecionar colunas relevantes
                relevant_cols = []
                
                for pattern in [
                    ['motorista', 'condutor', 'driver'],
                    ['data', 'date'],
                    ['origem', 'partida', 'origin', 'start'],
                    ['destino', 'chegada', 'destination', 'end'],
                    ['distancia', 'km', 'quilometragem', 'distance'],
                    ['tempo', 'duracao', 'duration', 'time'],
                    ['consumo', 'combustivel', 'fuel', 'consumption']
                ]:
                    col = self.data_processor._find_column_by_pattern(pattern)
                    if col:
                        relevant_cols.append(col)
                
                if not relevant_cols:
                    return {"error": "Colunas relevantes não encontradas", "data": None}
                
                # Limitar a 1000 viagens para o relatório
                trips_data = self.data_processor.data[relevant_cols].head(1000)
                
                return {
                    "error": None,
                    "data": trips_data.to_dict(orient='records'),
                    "columns": trips_data.columns.tolist()
                }
                
            elif report_type == 'geral':
                # Relatório geral com estatísticas
                metadata = self.data_processor.get_metadata()
                summary = self.data_processor.get_summary_stats()
                
                # Calcular estatísticas adicionais
                stats = {
                    "metadata": metadata,
                    "summary": summary,
                    "sample": self.data_processor.get_data_sample(5).to_dict(orient='records')
                }
                
                return {
                    "error": None,
                    "data": stats,
                    "type": "general_stats"
                }
                
            else:
                return {
                    "error": f"Tipo de relatório não reconhecido: {report_type}",
                    "data": None
                }
                
        except Exception as e:
            return {
                "error": f"Erro ao gerar dados para relatório: {str(e)}",
                "data": None
            }
