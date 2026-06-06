
from kafka import KafkaConsumer
from kafka import KafkaProducer
import logging

logger: logging = logging.getLogger("uvicorn")

class BrokerMethods: 
    
    @staticmethod
    async def produceMessage(producer: KafkaProducer, topic: str, data: dict) -> None:
        logger.info("Trying To Produce Kafka Event With New Data.")
        
        if not all(topic, data):
            logger.error("Kafka Data And Topic Not Found.")
            return
    
        try:
            producer.send(topic, value=data)
            logger.info("Successfully Publish New Kafka Event.")
            
        except Exception as e: 
            logger.exception(f"Couldn't Publish New Kafka Event: {e}")