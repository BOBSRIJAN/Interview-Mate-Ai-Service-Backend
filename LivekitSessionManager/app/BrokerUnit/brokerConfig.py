
from app.Config.envConfig import Envar
from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
import logging
import json

logger: logging = logging.getLogger("uvicorn")


class BrokerConf:

    @staticmethod
    async def initKafkaConsumer() -> AIOKafkaConsumer:
        logger.info("Initializing Kafka Consumer Module.")
        try:
            consumer: AIOKafkaConsumer = AIOKafkaConsumer(
                Envar.CONSUMER_TOPIC,
                bootstrap_servers=Envar.KAFKA_BROKER_URL,
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                group_id='livekit.session.manager.group',
                value_deserializer=lambda v: json.loads(v.decode('utf-8'))
            )

            logger.info("Kafka consumer connected successfully.")
            return consumer

        except Exception as e:
            logger.exception(f"Failed to create Kafka consumer: {e}")


    @staticmethod
    async def initKafkaProducer() -> AIOKafkaProducer:
        logger.info("Initializing Kafka Producer Module.")
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=Envar.KAFKA_BROKER_URL,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

            logger.info("Kafka producer connected successfully.")
            return producer

        except Exception as e:
            logger.exception(f"Failed to create Kafka producer: {e}")