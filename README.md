Aqui está o **README** ajustado com as informações detalhadas sobre a instalação e uso do Mosquitto no Windows, bem como o código ajustado para ler e responder com a próxima linha de um arquivo CSV via HTTP e MQTT:

---

# CSV MQTT API

Este projeto fornece uma API para ler um arquivo CSV e responder com a próxima linha disponível via HTTP e MQTT.

## 📌 Pré-requisitos

Antes de começar, certifique-se de ter instalado:
- Python 3.8+
- pip (gerenciador de pacotes do Python)
- MQTT Broker (opcional, pode usar o gratuito `mqtt.eclipseprojects.io`)
- Docker (para rodar em containers)
- **Mosquitto** (cliente MQTT, se você for testar via terminal)

### **Como instalar o Mosquitto no Windows:**

1. **Baixar e instalar o Mosquitto:**
   - Acesse o site oficial do Mosquitto: [https://mosquitto.org/download/](https://mosquitto.org/download/)
   - Baixe a versão do Windows (geralmente em `.exe` ou `.zip`).
   - Siga o assistente de instalação para configurar o Mosquitto no seu sistema.

2. **Adicionar o Mosquitto ao PATH do sistema:**
   - Após a instalação, se o comando `mosquitto_sub` e `mosquitto_pub` não forem reconhecidos, você precisará adicionar o diretório do Mosquitto ao PATH do seu sistema.
   - Navegue até a pasta onde o Mosquitto foi instalado (por exemplo, `C:\Program Files\mosquitto\bin`).
   - Copie o caminho completo da pasta.
   - No Windows:
     - Abra o **Menu Iniciar** e digite "variáveis de ambiente".
     - Selecione "Editar variáveis de ambiente do sistema".
     - Na janela "Propriedades do Sistema", clique em "Variáveis de Ambiente".
     - Em "Variáveis de Sistema", encontre a variável chamada `Path` e clique em "Editar".
     - Clique em "Novo" e cole o caminho que você copiou.
     - Clique em "OK" para fechar todas as janelas.

3. **Verificar se o Mosquitto está funcionando:**
   - Abra um novo terminal (cmd ou PowerShell) e digite o comando:
     ```bash
     mosquitto_sub -h mqtt.eclipseprojects.io -t "response/line"
     ```
   - Em outro terminal, envie uma mensagem com o comando:
     ```bash
     mosquitto_pub -h mqtt.eclipseprojects.io -t "request/line" -m "next"
     ```

Após seguir esses passos, você conseguirá testar a comunicação MQTT entre o cliente e o servidor. Se precisar de mais ajuda durante a instalação ou testes, fique à vontade para perguntar!

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/RafaelPCM/csv-mqtt-api.git
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

1. **Adicionando o arquivo CSV** chamado `dados_fator_potencia.csv`.
   - Rode o arquivo fator_potencia.py
      ``` bash
      python fator_potencia.py
      ```

   - O arquivo deve conter cabeçalhos na primeira linha, como:
     ```csv
     corrente_1,corrente_2,corrente_3,corrente_4,corrente_5,corrente_6,corrente_7,corrente_8,fator_potencia_1,fator_potencia_2,fator_potencia_3,fator_potencia_4,fator_potencia_5,fator_potencia_6,fator_potencia_7,fator_potencia_8,corrente_central,fator_potencia_central,classe
     9.42,11.26,5.77,8.11,16.69,7.26,18.67,9.24,0.75,0.97,0.86,0.94,0.91,0.92,0.96,0.78,86.42,0.90,MEDIDOR1
     13.84,12.48,0.53,5.05,10.43,10.80,16.44,12.13,0.92,0.63,0.93,0.95,0.91,0.97,0.95,0.97,81.70,0.90,MEDIDOR2
     ```

2. **Inicie a API**:
   ```bash
   uvicorn csv_mqtt_api:app --reload
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
   docker run -p 8000:8000 -v $(pwd)/dados_fator_potencia.csv:/app/dados_fator_potencia.csv csv-mqtt-api
   ```
   > No Windows (PowerShell), use: `-v ${PWD}/dados_fator_potencia.csv:/app/dados_fator_potencia.csv`

4. **Verifique se a API está rodando:**
   ```bash
   curl http://127.0.0.1:8000/next-line
   ```

Agora sua API estará rodando e disponível para atender requisições via HTTP e MQTT! 🚀

---