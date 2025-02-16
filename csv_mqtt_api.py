import csv
import json
import os
from fastapi import FastAPI
import paho.mqtt.client as mqtt
from collections import deque

app = FastAPI()

# Caminhos dos arquivos
CSV_FILE = os.path.join(os.path.dirname(__file__), "../data/dados_fator_potencia.csv")
FILTER_FILE = os.path.join(os.path.dirname(__file__), "../data/colunas_ignoradas.txt")

# Função para carregar as colunas a serem ignoradas
def load_ignored_columns(file_path):
    if not os.path.exists(file_path):
        print(f"Aviso: Arquivo {file_path} não encontrado. Nenhuma coluna será ignorada.")
        return set()
    
    with open(file_path, "r", encoding="utf-8") as f:
        ignored_columns = {line.strip() for line in f if line.strip()}  # Remove espaços e linhas vazias
    return ignored_columns

# Função para carregar o CSV na memória
def load_csv(file_path, ignored_columns):
    if not os.path.exists(file_path):  # Verifica se o arquivo existe
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return deque()

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = deque()

        for row in reader:
            # Remove colunas ignoradas
            filtered_row = {key: row[key] for key in row if key not in ignored_columns}
            
            # Converte valores numéricos corretamente
            for key in filtered_row:
                try:
                    filtered_row[key] = float(filtered_row[key]) if '.' in filtered_row[key] else int(filtered_row[key])
                except ValueError:
                    pass  # Mantém como string se não for número
            
            data.append(filtered_row)

        if not data:
            print(f"Erro: O arquivo {file_path} está vazio ou todas as colunas foram ignoradas.")
        return data

# Carrega as colunas ignoradas e os dados do CSV
ignored_columns = load_ignored_columns(FILTER_FILE)
data_queue = load_csv(CSV_FILE, ignored_columns)

# Configuração MQTT
BROKER = "mqtt.eclipseprojects.io"
TOPIC_REQUEST = "request/line"
TOPIC_RESPONSE = "response/line"

def on_message(client, userdata, message):
    global data_queue
    if message.topic == TOPIC_REQUEST and data_queue:
        next_line = data_queue.popleft()  # Pega a próxima linha do CSV
        client.publish(TOPIC_RESPONSE, json.dumps(next_line))
        print(f"Enviando via MQTT: {next_line}")

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER)
client.subscribe(TOPIC_REQUEST)
client.loop_start()

# Endpoint HTTP para solicitar a próxima linha do CSV
@app.get("/next-line")
def get_next_line():
    if data_queue:
        return data_queue.popleft()
    return {"error": "No more data"}
