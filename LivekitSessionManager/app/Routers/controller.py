
from app.Components.AgentSession import createAgentSession
from app.Components.UserSession import createUserSession
from app.BrokerUnit.brokerMethods import BrokerMethods
from app.Schemas.Validator import (
    UserSessionRequest,  UserSessionResponce,
    AgentSessionResponce, AgentSessionRequest
)
from app.Config.envConfig import Envar
from aiokafka import AIOKafkaConsumer
from redis.asyncio import Redis
import logging
import asyncio

logger = logging.getLogger("uvicorn")
states: dict = {}


class Workers:

    @staticmethod
    async def userWorker() -> None:

        consumer: AIOKafkaConsumer = states.get("KafkaConsumer")

        if not consumer:
            logger.error("Kafka Consumer Object was not found.")
            return

        await consumer.start()

        try:
            async for message in consumer:
                data = message.value
                logger.info("Evant Handler Trigger with The User Data from Kafka Event.")
                asyncio.create_task(Hendlers.userEventHendler(Data=data))
                await consumer.commit()

        except Exception as e:
            logger.exception(f"Exception occurred during message consuming time {e}")


class Hendlers:

    @staticmethod
    async def userEventHendler(Data: dict):
        producer = states.get('KafkaProducer')
        redis: Redis = states.get('Redis')

        try:
            userData: UserSessionRequest = UserSessionRequest.model_validate(Data)
            
        except Exception as e:
            await BrokerMethods.produceMessage(
                producer=producer,
                topic="val.error.user",
                data=Data
            )
            logger.exception(f"Validation Exception From User Data: {e}")
            return

        res: dict = await createUserSession(req=userData)
        
        try:
            roomInfo: UserSessionResponce = UserSessionResponce.model_validate(res)
        except Exception as e:
            await BrokerMethods.produceMessage(
                producer=producer,
                topic="val.error.user",
                data=Data
            )
            logger.exception(f"Validation Exception From LiveKit Data: {e}")
            return
        
        await BrokerMethods.produceMessage(
            producer=producer,
            topic="room.info.user",
            data=res
        )
            
        await redis.set(name=userData.userid, value=roomInfo.roomname)
        logger.info("User Session Generated Successfully and Kafka Event Publish.")
                
        

    @staticmethod
    async def agentEventHendler(Data: dict):
        pass
