import csv
import json
from fastapi import FastAPI
import paho.mqtt.client as mqtt
from collections import deque

app = FastAPI()

# Carregar CSV na memória
def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return deque(reader)  # Usa deque para fácil remoção da primeira linha

csv_file = "data.csv"
data_queue = load_csv(csv_file)

# Configuração MQTT
BROKER = "mqtt.eclipseprojects.io"
TOPIC_REQUEST = "request/line"
TOPIC_RESPONSE = "response/line"

def on_message(client, userdata, message):
    global data_queue
    if message.topic == TOPIC_REQUEST and data_queue:
        next_line = data_queue.popleft()  # Pega a próxima linha
        client.publish(TOPIC_RESPONSE, json.dumps(next_line))

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER)
client.subscribe(TOPIC_REQUEST)
client.loop_start()

# Endpoint HTTP para solicitar a próxima linha
@app.get("/next-line")
def get_next_line():
    if data_queue:
        return data_queue.popleft()
    return {"error": "No more data"}
