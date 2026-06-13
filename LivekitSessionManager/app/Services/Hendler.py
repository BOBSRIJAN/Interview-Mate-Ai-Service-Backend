
from app.Components.AgentSession import createAgentSession
from app.Components.UserSession import createUserSession
from app.BrokerUnit.brokerMethods import BrokerMethods
from app.Schemas.Validator import UserSessionRequest, UserSessionResponce
from redis.asyncio import Redis
from aiokafka import AIOKafkaProducer
import logging
import json

logger = logging.getLogger("uvicorn")

class Hendlers:

    @staticmethod
    async def userEventHendler(Data: dict, states: dict):
        producer: AIOKafkaProducer = states.get('KafkaProducer')
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
        res.update(userData)
        
        await BrokerMethods.produceMessage(
            producer=producer,
            topic="room.info.user",
            data=res
        )

        await redis.set(name=userData.userid, value=json.dumps(res), exat=900)
        logger.info("User Session Generated Successfully and Kafka Event Publish.")


    @staticmethod
    async def agentEventHendler(Data: dict, states: dict):
        producer: AIOKafkaProducer = states.get('KafkaProducer')

        try:
            userData: UserSessionResponce = UserSessionResponce.model_validate(Data)
            
        except Exception as e:
            await BrokerMethods.produceMessage(
                producer=producer,
                topic="val.error.agent",
                data=Data
            )
            logger.exception(f"Validation Exception From Agent Data: {e}")
            return

        res: dict = await createAgentSession(req=userData)
        
        await BrokerMethods.produceMessage(
            producer=producer,
            topic="room.info.agent",
            data=res
        )
        
        logger.info("Agent Session Generated Successfully and Kafka Event Publish.")