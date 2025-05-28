# README - Sistema de Chat com Planilha

## Descrição do Projeto

Este sistema permite que gestores de frota e segurança de transporte interajam com dados de planilhas Excel através de um chat com IA. O sistema processa grandes volumes de dados (até 300 mil registros), responde a perguntas em linguagem natural e gera relatórios em PDF e Excel.

## Estrutura do Projeto

```
chatplanilha_app/
├── venv/                      # Ambiente virtual Python
├── src/                       # Código-fonte da aplicação
│   ├── models/                # Modelos de dados
│   ├── routes/                # Rotas da API
│   │   ├── upload.py          # Rotas para upload de arquivos
│   │   ├── chat.py            # Rotas para o chat de IA
│   │   └── reports.py         # Rotas para geração de relatórios
│   ├── services/              # Serviços da aplicação
│   │   ├── data_processor.py  # Processamento de dados
│   │   ├── chat_engine.py     # Motor de chat com IA
│   │   ├── pdf_generator.py   # Gerador de PDF
│   │   ├── excel_generator.py # Gerador de Excel
│   │   └── setup.py           # Configuração de diretórios
│   ├── static/                # Arquivos estáticos
│   │   ├── css/               # Estilos CSS
│   │   ├── js/                # Scripts JavaScript
│   │   └── index.html         # Interface do usuário
│   ├── uploads/               # Diretório para arquivos carregados
│   ├── reports/               # Diretório para relatórios gerados
│   └── main.py                # Ponto de entrada da aplicação
├── test_data_generator.py     # Script para gerar dados de teste
├── performance_test.py        # Script para testar performance
├── manual_do_usuario.md       # Manual do usuário
└── requirements.txt           # Dependências do projeto
```

## Requisitos

- Python 3.11 ou superior
- Pip (gerenciador de pacotes Python)
- Navegador web moderno
- Conexão com a internet
- Servidor com pelo menos 4GB de RAM para processar planilhas grandes

## Instalação

1. Clone o repositório ou extraia os arquivos do sistema em um diretório de sua escolha.

2. Crie e ative um ambiente virtual Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure a chave da API OpenAI:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave da API OpenAI: `OPENAI_API_KEY=sua-chave-aqui`

5. Inicie o servidor:
   ```bash
   python src/main.py
   ```

6. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

## Funcionalidades Principais

- **Upload de Planilhas**: Carregue arquivos Excel com dados de viagens de motoristas.
- **Chat com IA**: Faça perguntas em linguagem natural sobre os dados carregados.
- **Geração de Relatórios**: Crie relatórios em PDF e Excel com diferentes visualizações dos dados.
- **Análise de Dados**: Obtenha insights sobre desempenho de motoristas, viagens, consumo e segurança.

## Scripts Utilitários

### Gerador de Dados de Teste

O script `test_data_generator.py` permite gerar uma planilha Excel com dados simulados de viagens de motoristas para testar o sistema:

```bash
python test_data_generator.py
```

Isso criará um arquivo `dados_teste_frota_300k.xlsx` com 300 mil registros simulados.

### Teste de Performance

O script `performance_test.py` executa testes de performance para validar o comportamento do sistema com uma planilha grande:

```bash
python performance_test.py
```

Os resultados dos testes serão salvos no diretório `performance_results/`.

## Documentação

Para mais informações sobre como usar o sistema, consulte o [Manual do Usuário](manual_do_usuario.md).

## Suporte

Se encontrar problemas ou tiver dúvidas, entre em contato com o suporte técnico:

- Email: suporte@chatplanilha.com
- Telefone: (00) 1234-5678
