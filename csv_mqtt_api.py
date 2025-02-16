import csv
import json
import os
from fastapi import FastAPI
import paho.mqtt.client as mqtt
from collections import deque

app = FastAPI()

# Caminho correto do CSV gerado pelo fator_potencia.py
CSV_FILE = os.path.join(os.path.dirname(__file__), "../data/dados_fator_potencia.csv")

# Função para carregar o CSV na memória
def load_csv(file_path):
    if not os.path.exists(file_path):  # Verifica se o arquivo existe
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return deque()

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = deque()

        for row in reader:
            # Converte valores numéricos corretamente
            for key in row:
                try:
                    row[key] = float(row[key]) if '.' in row[key] else int(row[key])
                except ValueError:
                    pass  # Mantém como string se não for número
            
            data.append(row)

        if not data:
            print(f"Erro: O arquivo {file_path} está vazio.")
        return data

# Carrega os dados do CSV para a memória
data_queue = load_csv(CSV_FILE)

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
