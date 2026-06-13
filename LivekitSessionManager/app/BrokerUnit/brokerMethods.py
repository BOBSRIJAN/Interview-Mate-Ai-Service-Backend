
from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
import logging

logger: logging = logging.getLogger("uvicorn")

class BrokerMethods: 
    
    @staticmethod
    async def produceMessage(producer: AIOKafkaProducer, topic: str, data: dict) -> None:
        logger.info("Trying To Produce Kafka Event With New Data.")
        
        if not (topic and data):
            logger.error("Kafka Data And Topic Not Found.")
            return
        
        try:
            await producer.start()
            await producer.send(topic, value=data)
            logger.info("Successfully Publish New Kafka Event.")
        except Exception as e: 
            logger.exception(f"Couldn't Publish New Kafka Event: {e}")


    @staticmethod
    async def shutdownConsumer(states: dict) -> None:
        consumerUser: AIOKafkaConsumer = states.get("KafkaConsumerUser")
        consumerAgent: AIOKafkaConsumer = states.get("KafkaConsumerAgent")
        
        if consumerUser and consumerAgent:
            await consumerUser.stop()
            await consumerAgent.stop()
            logger.info("Kafka Consumer Unit Shutdown Successfully.")


    @staticmethod
    async def shutdownProducer(states: dict) -> None:
        producer: AIOKafkaProducer = states.get("KafkaProducer")
        
        if producer:
            await producer.flush()
            await producer.stop()
            logger.info("Kafka Producer Unit Shutdown Successfully.")