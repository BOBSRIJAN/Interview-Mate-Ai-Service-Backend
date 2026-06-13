from dotenv import load_dotenv
import os 

load_dotenv()

class Envar:
    CONSUMER_TOPIC_USER: str = os.getenv('CONSUMER_TOPIC_USER')
    CONSUMER_TOPIC_AGENT: str = os.getenv('CONSUMER_TOPIC_AGENT')
    KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    LIVEKIT_URL = os.getenv("LIVEKIT_URL")
    LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
    LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
    GLOBAL_HOST: str = os.getenv('GLOBAL_HOST')