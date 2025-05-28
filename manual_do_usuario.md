# Manual do Usuário - Sistema de Chat com Planilha

## Visão Geral

O Sistema de Chat com Planilha é uma aplicação web que permite aos gestores de frota e segurança de transporte interagir com dados de viagens de motoristas através de um chat de IA, além de gerar relatórios em PDF e Excel. O sistema foi projetado para processar grandes volumes de dados (até 300 mil registros) e fornecer respostas rápidas e precisas.

## Funcionalidades Principais

1. **Upload de Planilhas**: Carregue arquivos Excel com dados de viagens de motoristas.
2. **Chat com IA**: Faça perguntas em linguagem natural sobre os dados carregados.
3. **Geração de Relatórios**: Crie relatórios em PDF e Excel com diferentes visualizações dos dados.
4. **Análise de Dados**: Obtenha insights sobre desempenho de motoristas, viagens, consumo e segurança.

## Requisitos do Sistema

- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- Conexão com a internet
- Servidor com pelo menos 4GB de RAM para processar planilhas grandes

## Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- Pip (gerenciador de pacotes Python)
- Ambiente virtual Python (recomendado)

### Passos para Instalação

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

## Guia de Uso

### Upload de Planilha

1. Clique na aba "Upload" no menu superior.
2. Arraste e solte seu arquivo Excel na área indicada ou clique para selecionar um arquivo.
3. Aguarde o processamento do arquivo (o tempo varia conforme o tamanho da planilha).
4. Após o carregamento, você verá informações básicas sobre os dados e uma amostra.
5. Clique em "Ir para o Chat" para começar a interagir com os dados.

### Uso do Chat

1. Digite sua pergunta na caixa de texto na parte inferior do chat.
2. Pressione Enter ou clique no botão de envio para enviar sua pergunta.
3. Aguarde a resposta da IA, que pode incluir texto explicativo e tabelas de dados.
4. Você pode usar os exemplos de perguntas sugeridos abaixo do chat para começar.

#### Exemplos de Perguntas

- "Quais são os motoristas com mais viagens?"
- "Qual a distância média percorrida por motorista?"
- "Mostre os scores de segurança dos motoristas"
- "Quais motoristas tiveram eventos de freada brusca?"
- "Qual o consumo médio de combustível por tipo de veículo?"
- "Quais foram as viagens mais longas no último mês?"
- "Gere um relatório geral em PDF"

### Geração de Relatórios

1. Clique na aba "Relatórios" no menu superior.
2. Escolha o tipo de relatório que deseja gerar:
   - **Relatório Geral**: Visão geral dos dados
   - **Relatório de Motoristas**: Análise por motorista
   - **Relatório de Viagens**: Detalhes das viagens
   - **Relatório de Scores**: Pontuação dos motoristas
3. Selecione o formato desejado (PDF ou Excel).
4. Aguarde a geração do relatório.
5. Após a geração, o relatório aparecerá na lista de "Relatórios Gerados".
6. Clique em "Baixar" para salvar o relatório em seu computador.

## Estrutura dos Dados

O sistema espera uma planilha Excel com dados de viagens de motoristas. Embora seja flexível quanto às colunas exatas, o desempenho ideal é obtido quando a planilha contém as seguintes informações:

- **Dados de Motoristas**: Nome, ID, etc.
- **Dados de Viagens**: Origem, destino, data, distância, tempo, etc.
- **Dados de Veículos**: Tipo, placa, etc.
- **Dados de Consumo**: Combustível, custos, etc.
- **Dados de Eventos/Infrações**: Tipos de eventos, quantidade, etc.
- **Scores/Métricas**: Pontuações de segurança, eficiência, etc.

## Considerações de Performance

- **Tamanho da Planilha**: O sistema foi testado com planilhas de até 300 mil registros.
- **Tempo de Carregamento**: Planilhas grandes podem levar alguns minutos para carregar.
- **Uso de Memória**: O processamento de planilhas grandes requer mais memória.
- **Geração de Relatórios**: Relatórios PDF para grandes volumes de dados podem ser mais lentos que relatórios Excel.

## Solução de Problemas

### Problemas Comuns

1. **Erro no Upload de Arquivo**
   - Verifique se o arquivo está no formato .xlsx ou .xls
   - Verifique se o arquivo não está corrompido
   - Tente reduzir o tamanho do arquivo se for muito grande

2. **Respostas Imprecisas do Chat**
   - Formule perguntas mais específicas
   - Verifique se os dados na planilha estão estruturados corretamente
   - Tente reformular a pergunta de maneira diferente

3. **Erro na Geração de Relatórios**
   - Verifique se há dados suficientes para o tipo de relatório solicitado
   - Para planilhas muito grandes, tente gerar relatórios em Excel em vez de PDF
   - Verifique se o servidor tem memória suficiente

4. **Lentidão no Sistema**
   - Considere reduzir o tamanho da planilha
   - Feche outras aplicações que consomem muita memória
   - Verifique a conexão com a internet

### Contato para Suporte

Se encontrar problemas que não consegue resolver, entre em contato com o suporte técnico:

- Email: suporte@chatplanilha.com
- Telefone: (00) 1234-5678

## Limitações Conhecidas

- O sistema tem um limite de processamento para planilhas muito grandes (acima de 500 mil registros).
- Algumas consultas complexas podem levar mais tempo para serem processadas.
- A geração de relatórios PDF para grandes volumes de dados pode ser lenta.
- O sistema requer uma conexão com a internet para funcionar corretamente.

## Atualizações Futuras

Estamos constantemente melhorando o sistema. Algumas funcionalidades planejadas para futuras versões incluem:

- Visualizações gráficas interativas dos dados
- Exportação de dados para outros formatos
- Integração com sistemas de gestão de frota
- Alertas automáticos baseados em padrões nos dados
- Interface mobile otimizada

## Licença e Termos de Uso

Este sistema é fornecido sob licença proprietária. Todos os direitos reservados.
O uso deste software está sujeito aos termos e condições estabelecidos no contrato de licença.
