import os
import json
import logging
from datetime import datetime
from sqlalchemy import create_engine, text
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

# MQTT
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
TOPIC = 'ECOPLUS/EX-001/dados'

# PostgreSQL
DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DB_URL)
print(DB_URL)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def on_connect(client, userdata, flags, rc):
    logging.info(f"Conectado MQTT ({rc})")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        # Campos esperados
        id_maquina = payload['id_maquina']
        datahora = datetime.fromisoformat(payload['datahora'])
        ligada = payload['ligada']
        operacao = payload['operacao']
        manut_cor = payload['manutencao_corretiva']
        manut_prev = payload['manutencao_preventiva']
        p_boas = payload['pecas_produzidas']
        p_refugo = payload['pecas_defeituosas']

        insert = text("""
            INSERT INTO dados_maquina(
              id_maquina, datahora, ligada, operacao,
              manutencao_corretiva, manutencao_preventiva,
              pecas_produzidas, pecas_defeituosas
            ) VALUES (
              :id_maquina, :datahora, :ligada, :operacao,
              :manut_cor, :manut_prev,
              :p_boas, :p_refugo
            )
        """)
        with engine.begin() as conn:
            conn.execute(insert, {
                'id_maquina': id_maquina,
                'datahora': datahora,
                'ligada': ligada,
                'operacao': operacao,
                'manut_cor': manut_cor,
                'manut_prev': manut_prev,
                'p_boas': p_boas,
                'p_refugo': p_refugo
            })
        logging.info(f"Inserido: máquina {id_maquina} @ {datahora}")
    except Exception as e:
        logging.error(f"Erro ao inserir: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if __name__ == '__main__':
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()