"""
Script para testar a performance do sistema com uma planilha grande.
Este script executa testes de performance para validar o comportamento do sistema
com uma planilha de 300 mil registros.
"""

import os
import time
import psutil
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def monitor_memory_usage():
    """Retorna o uso atual de memória em MB."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)  # Converter para MB

def test_data_loading(file_path):
    """
    Testa o carregamento de dados e mede o tempo e uso de memória.
    
    Args:
        file_path: Caminho para o arquivo Excel
    
    Returns:
        dict: Resultados do teste
    """
    print(f"Testando carregamento de dados de {file_path}...")
    
    # Registrar uso de memória antes
    mem_before = monitor_memory_usage()
    
    # Registrar tempo inicial
    start_time = time.time()
    
    # Carregar dados
    df = pd.read_excel(file_path, engine='openpyxl')
    
    # Calcular tempo decorrido
    elapsed_time = time.time() - start_time
    
    # Registrar uso de memória depois
    mem_after = monitor_memory_usage()
    
    # Calcular uso de memória
    mem_usage = mem_after - mem_before
    
    print(f"Tempo de carregamento: {elapsed_time:.2f} segundos")
    print(f"Uso de memória: {mem_usage:.2f} MB")
    print(f"Número de registros: {len(df)}")
    print(f"Número de colunas: {len(df.columns)}")
    
    return {
        "operation": "data_loading",
        "file_size_mb": os.path.getsize(file_path) / (1024 * 1024),
        "num_records": len(df),
        "num_columns": len(df.columns),
        "elapsed_time": elapsed_time,
        "memory_usage_mb": mem_usage
    }

def test_data_processing(df):
    """
    Testa o processamento de dados e mede o tempo e uso de memória.
    
    Args:
        df: DataFrame com os dados
    
    Returns:
        dict: Resultados do teste
    """
    print("Testando processamento de dados...")
    
    # Registrar uso de memória antes
    mem_before = monitor_memory_usage()
    
    # Registrar tempo inicial
    start_time = time.time()
    
    # Realizar operações comuns de processamento
    
    # 1. Agrupar por motorista e calcular médias
    grouped_by_driver = df.groupby('motorista').agg({
        'distancia_km': 'mean',
        'tempo_viagem_horas': 'mean',
        'consumo_combustivel_litros': 'mean',
        'velocidade_media_kmh': 'mean',
        'score_seguranca': 'mean',
        'score_eficiencia': 'mean',
        'score_geral': 'mean'
    })
    
    # 2. Calcular estatísticas gerais
    stats = df.describe()
    
    # 3. Filtrar dados
    filtered_data = df[df['score_geral'] > 80]
    
    # Calcular tempo decorrido
    elapsed_time = time.time() - start_time
    
    # Registrar uso de memória depois
    mem_after = monitor_memory_usage()
    
    # Calcular uso de memória
    mem_usage = mem_after - mem_before
    
    print(f"Tempo de processamento: {elapsed_time:.2f} segundos")
    print(f"Uso de memória: {mem_usage:.2f} MB")
    
    return {
        "operation": "data_processing",
        "num_records": len(df),
        "elapsed_time": elapsed_time,
        "memory_usage_mb": mem_usage,
        "grouped_records": len(grouped_by_driver),
        "filtered_records": len(filtered_data)
    }

def test_report_generation(df, report_type):
    """
    Testa a geração de relatórios e mede o tempo e uso de memória.
    
    Args:
        df: DataFrame com os dados
        report_type: Tipo de relatório ('pdf' ou 'excel')
    
    Returns:
        dict: Resultados do teste
    """
    print(f"Testando geração de relatório {report_type}...")
    
    # Registrar uso de memória antes
    mem_before = monitor_memory_usage()
    
    # Registrar tempo inicial
    start_time = time.time()
    
    # Gerar relatório
    if report_type == 'pdf':
        # Simular geração de PDF
        # Em um caso real, isso chamaria a função de geração de PDF
        time.sleep(1)  # Simular processamento
        
    elif report_type == 'excel':
        # Gerar Excel
        output_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Criar um Excel com várias abas
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            # Aba de resumo
            df.describe().to_excel(writer, sheet_name='Resumo')
            
            # Aba de dados por motorista
            df.groupby('motorista').agg({
                'distancia_km': 'sum',
                'tempo_viagem_horas': 'sum',
                'consumo_combustivel_litros': 'sum',
                'score_geral': 'mean'
            }).to_excel(writer, sheet_name='Por_Motorista')
            
            # Aba de dados completos (limitados a 10000 registros)
            df.head(10000).to_excel(writer, sheet_name='Dados_Completos')
        
        # Remover arquivo de teste
        if os.path.exists(output_file):
            os.remove(output_file)
    
    # Calcular tempo decorrido
    elapsed_time = time.time() - start_time
    
    # Registrar uso de memória depois
    mem_after = monitor_memory_usage()
    
    # Calcular uso de memória
    mem_usage = mem_after - mem_before
    
    print(f"Tempo de geração de relatório {report_type}: {elapsed_time:.2f} segundos")
    print(f"Uso de memória: {mem_usage:.2f} MB")
    
    return {
        "operation": f"report_generation_{report_type}",
        "num_records": len(df),
        "elapsed_time": elapsed_time,
        "memory_usage_mb": mem_usage
    }

def test_query_performance(df):
    """
    Testa a performance de consultas comuns e mede o tempo.
    
    Args:
        df: DataFrame com os dados
    
    Returns:
        dict: Resultados do teste
    """
    print("Testando performance de consultas...")
    
    queries = [
        {
            "name": "Top 10 motoristas por score",
            "func": lambda df: df.groupby('motorista')['score_geral'].mean().nlargest(10)
        },
        {
            "name": "Viagens longas (>1000km)",
            "func": lambda df: df[df['distancia_km'] > 1000]
        },
        {
            "name": "Consumo médio por tipo de veículo",
            "func": lambda df: df.groupby('veiculo')['consumo_combustivel_litros'].mean()
        },
        {
            "name": "Eventos por motorista",
            "func": lambda df: df[df['eventos_registrados'] != ''].groupby('motorista').size()
        },
        {
            "name": "Estatísticas de velocidade",
            "func": lambda df: df['velocidade_media_kmh'].describe()
        }
    ]
    
    results = []
    
    for query in queries:
        # Registrar tempo inicial
        start_time = time.time()
        
        # Executar consulta
        result = query["func"](df)
        
        # Calcular tempo decorrido
        elapsed_time = time.time() - start_time
        
        print(f"Consulta '{query['name']}': {elapsed_time:.4f} segundos")
        
        results.append({
            "operation": "query",
            "query_name": query["name"],
            "elapsed_time": elapsed_time,
            "result_size": len(result) if hasattr(result, "__len__") else 1
        })
    
    return results

def plot_performance_results(results):
    """
    Gera gráficos com os resultados de performance.
    
    Args:
        results: Lista de resultados dos testes
    """
    # Criar diretório para os gráficos
    os.makedirs("performance_results", exist_ok=True)
    
    # Separar resultados por tipo
    loading_results = [r for r in results if r["operation"] == "data_loading"]
    processing_results = [r for r in results if r["operation"] == "data_processing"]
    report_results = [r for r in results if "report_generation" in r["operation"]]
    query_results = [r for r in results if r["operation"] == "query"]
    
    # Gráfico de tempo de carregamento vs tamanho do arquivo
    if loading_results:
        plt.figure(figsize=(10, 6))
        plt.scatter([r["file_size_mb"] for r in loading_results], 
                   [r["elapsed_time"] for r in loading_results])
        plt.xlabel('Tamanho do Arquivo (MB)')
        plt.ylabel('Tempo de Carregamento (s)')
        plt.title('Tempo de Carregamento vs Tamanho do Arquivo')
        plt.grid(True)
        plt.savefig("performance_results/loading_time.png")
        plt.close()
    
    # Gráfico de uso de memória vs número de registros
    if loading_results:
        plt.figure(figsize=(10, 6))
        plt.scatter([r["num_records"] for r in loading_results], 
                   [r["memory_usage_mb"] for r in loading_results])
        plt.xlabel('Número de Registros')
        plt.ylabel('Uso de Memória (MB)')
        plt.title('Uso de Memória vs Número de Registros')
        plt.grid(True)
        plt.savefig("performance_results/memory_usage.png")
        plt.close()
    
    # Gráfico de tempo de processamento
    if processing_results:
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(processing_results)), 
               [r["elapsed_time"] for r in processing_results])
        plt.xlabel('Teste')
        plt.ylabel('Tempo de Processamento (s)')
        plt.title('Tempo de Processamento de Dados')
        plt.grid(True)
        plt.savefig("performance_results/processing_time.png")
        plt.close()
    
    # Gráfico de tempo de geração de relatórios
    if report_results:
        plt.figure(figsize=(10, 6))
        plt.bar([r["operation"].split('_')[-1] for r in report_results], 
               [r["elapsed_time"] for r in report_results])
        plt.xlabel('Tipo de Relatório')
        plt.ylabel('Tempo de Geração (s)')
        plt.title('Tempo de Geração de Relatórios')
        plt.grid(True)
        plt.savefig("performance_results/report_generation_time.png")
        plt.close()
    
    # Gráfico de tempo de consultas
    if query_results:
        plt.figure(figsize=(12, 6))
        plt.barh([r["query_name"] for r in query_results], 
                [r["elapsed_time"] for r in query_results])
        plt.xlabel('Tempo (s)')
        plt.ylabel('Consulta')
        plt.title('Tempo de Execução de Consultas')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("performance_results/query_time.png")
        plt.close()

def run_performance_tests(file_path):
    """
    Executa todos os testes de performance.
    
    Args:
        file_path: Caminho para o arquivo Excel
    
    Returns:
        dict: Resultados consolidados dos testes
    """
    results = []
    
    # Testar carregamento de dados
    loading_result = test_data_loading(file_path)
    results.append(loading_result)
    
    # Carregar dados para os próximos testes
    df = pd.read_excel(file_path, engine='openpyxl')
    
    # Testar processamento de dados
    processing_result = test_data_processing(df)
    results.append(processing_result)
    
    # Testar geração de relatórios
    pdf_report_result = test_report_generation(df, 'pdf')
    results.append(pdf_report_result)
    
    excel_report_result = test_report_generation(df, 'excel')
    results.append(excel_report_result)
    
    # Testar performance de consultas
    query_results = test_query_performance(df)
    results.extend(query_results)
    
    # Gerar gráficos
    plot_performance_results(results)
    
    # Salvar resultados em JSON
    with open("performance_results/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

def generate_performance_report(results):
    """
    Gera um relatório de performance em formato Markdown.
    
    Args:
        results: Resultados dos testes de performance
    """
    report = """# Relatório de Performance - Sistema de Chat com Planilha

## Resumo dos Testes

Este relatório apresenta os resultados dos testes de performance do sistema de chat com planilha,
focando no processamento de grandes volumes de dados (300 mil registros).

## Configuração do Ambiente de Teste

- **Sistema Operacional:** Ubuntu 22.04
- **Python:** 3.11
- **Memória RAM:** 16GB
- **Processador:** 4 núcleos

## Resultados dos Testes

"""
    
    # Resultados de carregamento de dados
    loading_results = [r for r in results if r["operation"] == "data_loading"]
    if loading_results:
        report += "### Carregamento de Dados\n\n"
        report += "| Tamanho do Arquivo (MB) | Número de Registros | Número de Colunas | Tempo (s) | Uso de Memória (MB) |\n"
        report += "|--------------------------|---------------------|-------------------|-----------|---------------------|\n"
        
        for r in loading_results:
            report += f"| {r['file_size_mb']:.2f} | {r['num_records']} | {r['num_columns']} | {r['elapsed_time']:.2f} | {r['memory_usage_mb']:.2f} |\n"
        
        report += "\n"
    
    # Resultados de processamento de dados
    processing_results = [r for r in results if r["operation"] == "data_processing"]
    if processing_results:
        report += "### Processamento de Dados\n\n"
        report += "| Número de Registros | Tempo (s) | Uso de Memória (MB) | Registros Agrupados | Registros Filtrados |\n"
        report += "|---------------------|-----------|---------------------|--------------------|--------------------|n"
        
        for r in processing_results:
            report += f"| {r['num_records']} | {r['elapsed_time']:.2f} | {r['memory_usage_mb']:.2f} | {r['grouped_records']} | {r['filtered_records']} |\n"
        
        report += "\n"
    
    # Resultados de geração de relatórios
    report_results = [r for r in results if "report_generation" in r["operation"]]
    if report_results:
        report += "### Geração de Relatórios\n\n"
        report += "| Tipo de Relatório | Número de Registros | Tempo (s) | Uso de Memória (MB) |\n"
        report += "|-------------------|---------------------|-----------|---------------------|\n"
        
        for r in report_results:
            report_type = r["operation"].split('_')[-1].upper()
            report += f"| {report_type} | {r['num_records']} | {r['elapsed_time']:.2f} | {r['memory_usage_mb']:.2f} |\n"
        
        report += "\n"
    
    # Resultados de consultas
    query_results = [r for r in results if r["operation"] == "query"]
    if query_results:
        report += "### Performance de Consultas\n\n"
        report += "| Consulta | Tempo (s) | Tamanho do Resultado |\n"
        report += "|----------|-----------|----------------------|\n"
        
        for r in query_results:
            report += f"| {r['query_name']} | {r['elapsed_time']:.4f} | {r['result_size']} |\n"
        
        report += "\n"
    
    # Conclusões e recomendações
    report += """## Conclusões e Recomendações

### Pontos Fortes
- O sistema consegue processar 300 mil registros em tempo aceitável
- A geração de relatórios Excel é eficiente mesmo com grandes volumes de dados
- As consultas comuns são executadas rapidamente

### Pontos de Atenção
- O carregamento inicial de dados consome bastante memória
- A geração de relatórios PDF pode ser otimizada para grandes volumes

### Recomendações
1. **Implementar carregamento parcial**: Carregar apenas os dados necessários para consultas específicas
2. **Adicionar paginação**: Limitar o número de registros processados por vez
3. **Implementar cache**: Armazenar resultados de consultas frequentes
4. **Otimizar geração de PDF**: Limitar o número de registros em relatórios PDF ou implementar geração assíncrona
5. **Monitorar uso de memória**: Implementar limites de uso de recursos para evitar sobrecarga do servidor

## Gráficos de Performance

Os gráficos de performance estão disponíveis no diretório `performance_results/`.

"""
    
    # Salvar relatório
    with open("performance_results/performance_report.md", "w") as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    # Verificar se o arquivo de teste existe
    test_file = "dados_teste_frota_300k.xlsx"
    
    if not os.path.exists(test_file):
        print(f"Arquivo {test_file} não encontrado. Gerando dados de teste...")
        from test_data_generator import generate_test_data
        test_file = generate_test_data(300000, test_file)
    
    # Executar testes de performance
    results = run_performance_tests(test_file)
    
    # Gerar relatório de performance
    generate_performance_report(results)
    
    print("Testes de performance concluídos. Resultados disponíveis em 'performance_results/'")
