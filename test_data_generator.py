"""
Script para gerar dados de teste para validação de performance.
Este script cria uma planilha Excel com dados simulados de viagens de motoristas
para testar o sistema com um grande volume de dados (300 mil registros).
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_test_data(num_records=300000, output_file='dados_teste_frota.xlsx'):
    """
    Gera dados de teste para validação de performance.
    
    Args:
        num_records: Número de registros a serem gerados
        output_file: Nome do arquivo de saída
    
    Returns:
        str: Caminho do arquivo gerado
    """
    print(f"Gerando {num_records} registros de teste...")
    
    # Definir nomes de motoristas
    nomes = [
        "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa", "Carlos Pereira",
        "Luiza Fernandes", "Ricardo Almeida", "Juliana Martins", "Fernando Souza", 
        "Mariana Lima", "Antônio Rodrigues", "Patrícia Gomes", "Lucas Ribeiro", 
        "Camila Carvalho", "Roberto Barbosa", "Daniela Nascimento", "Marcos Alves",
        "Cristina Mendes", "Paulo Castro", "Beatriz Cardoso", "José Correia",
        "Amanda Teixeira", "Gustavo Ferreira", "Larissa Moreira", "Eduardo Nunes",
        "Vanessa Rocha", "Marcelo Dias", "Bianca Ramos", "Fábio Freitas", "Letícia Vieira"
    ]
    
    # Definir cidades
    cidades = [
        "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", "Salvador",
        "Fortaleza", "Recife", "Porto Alegre", "Curitiba", "Manaus", "Belém",
        "Goiânia", "Guarulhos", "Campinas", "São Luís", "São Gonçalo", "Maceió",
        "Duque de Caxias", "Natal", "Teresina", "São Bernardo do Campo", "Campo Grande",
        "Osasco", "Santo André", "João Pessoa", "Jaboatão dos Guararapes", "Contagem"
    ]
    
    # Definir tipos de veículos
    veiculos = [
        "Caminhão Baú", "Caminhão Tanque", "Caminhão Frigorífico", "Van de Carga",
        "Caminhão Graneleiro", "Caminhão Basculante", "Caminhão Guincho", "Caminhão Plataforma",
        "Caminhão Compactador", "Caminhão Betoneira"
    ]
    
    # Definir placas de veículos
    def gerar_placa():
        letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        numeros = ''.join(random.choices('0123456789', k=4))
        return f"{letras}-{numeros}"
    
    placas = [gerar_placa() for _ in range(100)]
    
    # Definir tipos de eventos
    eventos = [
        "Freada Brusca", "Excesso de Velocidade", "Desvio de Rota", "Parada Não Autorizada",
        "Tempo de Descanso Insuficiente", "Uso Indevido do Veículo", "Aceleração Brusca",
        "Curva Acentuada", "Condução Noturna Prolongada", "Manutenção Atrasada"
    ]
    
    # Gerar data inicial (1 ano atrás)
    data_inicial = datetime.now() - timedelta(days=365)
    
    # Criar listas para armazenar os dados
    dados = {
        'id_viagem': range(1, num_records + 1),
        'motorista': [random.choice(nomes) for _ in range(num_records)],
        'data_saida': [],
        'data_chegada': [],
        'origem': [],
        'destino': [],
        'veiculo': [random.choice(veiculos) for _ in range(num_records)],
        'placa': [random.choice(placas) for _ in range(num_records)],
        'distancia_km': [],
        'tempo_viagem_horas': [],
        'consumo_combustivel_litros': [],
        'custo_combustivel': [],
        'velocidade_media_kmh': [],
        'carga_kg': [],
        'tipo_carga': ['Alimentos', 'Eletrônicos', 'Vestuário', 'Construção', 'Químicos'],
        'eventos_registrados': [],
        'num_paradas': [],
        'tempo_paradas_horas': [],
        'score_seguranca': [],
        'score_eficiencia': [],
        'score_geral': []
    }
    
    # Gerar dados aleatórios
    for i in range(num_records):
        # Gerar datas de saída e chegada
        dias_aleatorios = random.randint(0, 364)
        data_saida = data_inicial + timedelta(days=dias_aleatorios)
        duracao_horas = random.uniform(1, 72)  # Entre 1 hora e 3 dias
        data_chegada = data_saida + timedelta(hours=duracao_horas)
        
        dados['data_saida'].append(data_saida)
        dados['data_chegada'].append(data_chegada)
        
        # Origem e destino
        origem = random.choice(cidades)
        destino = random.choice([c for c in cidades if c != origem])
        dados['origem'].append(origem)
        dados['destino'].append(destino)
        
        # Distância e tempo
        distancia = random.uniform(50, 2000)  # Entre 50 e 2000 km
        dados['distancia_km'].append(distancia)
        dados['tempo_viagem_horas'].append(duracao_horas)
        
        # Velocidade média
        velocidade_media = distancia / duracao_horas
        dados['velocidade_media_kmh'].append(velocidade_media)
        
        # Consumo e custo de combustível
        consumo_medio = random.uniform(2.5, 5.0)  # Litros por km
        consumo_total = distancia * consumo_medio
        dados['consumo_combustivel_litros'].append(consumo_total)
        
        preco_combustivel = random.uniform(4.5, 6.5)  # Preço por litro
        custo_combustivel = consumo_total * preco_combustivel
        dados['custo_combustivel'].append(custo_combustivel)
        
        # Carga
        dados['carga_kg'].append(random.uniform(500, 25000))
        dados['tipo_carga'].append(random.choice(['Alimentos', 'Eletrônicos', 'Vestuário', 'Construção', 'Químicos']))
        
        # Eventos
        num_eventos = random.choices([0, 1, 2, 3, 4, 5], weights=[0.6, 0.2, 0.1, 0.05, 0.03, 0.02])[0]
        if num_eventos > 0:
            eventos_viagem = random.sample(eventos, num_eventos)
            dados['eventos_registrados'].append(', '.join(eventos_viagem))
        else:
            dados['eventos_registrados'].append('')
        
        # Paradas
        num_paradas = int(duracao_horas / 4) + random.randint(0, 3)
        dados['num_paradas'].append(num_paradas)
        
        tempo_paradas = random.uniform(0.25, 0.5) * num_paradas
        dados['tempo_paradas_horas'].append(tempo_paradas)
        
        # Scores
        # Quanto menos eventos, melhor o score de segurança
        score_seguranca = 100 - (num_eventos * 15) + random.uniform(-5, 5)
        score_seguranca = max(0, min(100, score_seguranca))
        dados['score_seguranca'].append(score_seguranca)
        
        # Eficiência baseada em consumo e velocidade
        score_eficiencia = 100 - (consumo_medio - 2.5) * 20 + (velocidade_media / 10) + random.uniform(-10, 10)
        score_eficiencia = max(0, min(100, score_eficiencia))
        dados['score_eficiencia'].append(score_eficiencia)
        
        # Score geral
        score_geral = (score_seguranca * 0.6) + (score_eficiencia * 0.4) + random.uniform(-5, 5)
        score_geral = max(0, min(100, score_geral))
        dados['score_geral'].append(score_geral)
        
        # Mostrar progresso
        if (i + 1) % 50000 == 0 or i + 1 == num_records:
            print(f"Gerados {i + 1} de {num_records} registros ({((i + 1) / num_records) * 100:.1f}%)")
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Salvar em Excel
    print(f"Salvando dados em {output_file}...")
    df.to_excel(output_file, index=False)
    
    print(f"Arquivo gerado com sucesso: {output_file}")
    print(f"Tamanho do arquivo: {os.path.getsize(output_file) / (1024 * 1024):.2f} MB")
    
    return output_file

if __name__ == "__main__":
    # Gerar dados de teste com 300 mil registros
    generate_test_data(300000, 'dados_teste_frota_300k.xlsx')
