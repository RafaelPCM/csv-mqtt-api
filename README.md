# CSV MQTT API

Este projeto fornece uma API para ler um arquivo CSV e responder com a próxima linha disponível via HTTP e MQTT.

## 📌 Pré-requisitos

Antes de começar, certifique-se de ter instalado:
- Python 3.8+
- pip (gerenciador de pacotes do Python)
- MQTT Broker (opcional, pode usar o gratuito `mqtt.eclipseprojects.io`)
- Docker (para rodar em containers)

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/csv-mqtt-api.git
   cd csv-mqtt-api
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Executando a API

1. **Adicione um arquivo CSV** chamado `data.csv` no diretório do projeto.
   - O arquivo deve conter cabeçalhos na primeira linha, como:
     ```csv
     id,nome,idade
     1,Ana,25
     2,Beto,30
     ```

2. **Inicie a API**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Faça uma requisição HTTP para obter a próxima linha**:
   ```bash
   curl http://127.0.0.1:8000/next-line
   ```

4. **Configurar MQTT** (Opcional):
   - O código já se conecta ao broker `mqtt.eclipseprojects.io`
   - Para solicitar uma linha via MQTT, publique uma mensagem no tópico `request/line`
   - A resposta será enviada no tópico `response/line`

## 🐳 Executando com Docker

1. **Instale o Docker** (caso não tenha instalado):
   - [Guia oficial de instalação](https://docs.docker.com/get-docker/)

2. **Construa a imagem Docker:**
   ```bash
   docker build -t csv-mqtt-api .
   ```

3. **Execute o container:**
   ```bash
   docker run -p 8000:8000 -v $(pwd)/data.csv:/app/data.csv csv-mqtt-api
   ```
   > No Windows (PowerShell), use: `-v ${PWD}/data.csv:/app/data.csv`

4. **Verifique se a API está rodando:**
   ```bash
   curl http://127.0.0.1:8000/next-line
   ```

Agora sua API estará rodando e disponível para atender requisições! 🚀

