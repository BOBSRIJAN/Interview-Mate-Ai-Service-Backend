
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
import json
import logging

load_dotenv()
logger: logging = logging.getLogger("python")
CONSUMER_TOPIC: str = os.getenv('CONSUMER_TOPIC')
KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL")

async def initKafkaConsumer() -> KafkaConsumer:
    try:
        consumer: KafkaConsumer = KafkaConsumer(
            CONSUMER_TOPIC,
            bootstrap_servers=KAFKA_BROKER_URL,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='livekit.session.manager.group',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        
        logger.info("Kafka Consumer connected successfully.")
        return consumer
    
    except Exception as e:
        logger.exception(f"Failed to create Kafka consumer: {e}")
