
from app.Services.Hendler import Hendlers
from aiokafka import AIOKafkaConsumer
import logging
import asyncio

logger = logging.getLogger("uvicorn")
states: dict = {}


class Workers:

    @staticmethod
    async def userWorker() -> None:
        consumer: AIOKafkaConsumer = states.get("KafkaConsumerUser")

        if not consumer:
            logger.error("Kafka User Consumer Object was not Found.")
            return

        await consumer.start()

        try:
            async for message in consumer:
                data = message.value
                logger.info("Event Handler Trigger with The User Data from Kafka Event.")
                asyncio.create_task(Hendlers.userEventHendler(Data=data, states=states))
                await consumer.commit()

        except Exception as e:
            logger.exception(f"Exception occurred during message consuming time: {e}")


    @staticmethod
    async def agentWorker() -> None:
        consumer: AIOKafkaConsumer = states.get("KafkaConsumerAgent")

        if not consumer:
            logger.error("Kafka Agent Consumer Object was not Found.")
            return

        await consumer.start()

        try:
            async for message in consumer:
                data = message.value
                logger.info("Event Handler Trigger with The Agent Data from Kafka Event.")
                asyncio.create_task(Hendlers.agentEventHendler(Data=data, states=states))
                await consumer.commit()

        except Exception as e:
            logger.exception(f"Exception occurred during message consuming time: {e}")