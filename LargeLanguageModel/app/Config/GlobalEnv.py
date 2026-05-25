import dotenv
import os 

dotenv.load_dotenv()

class EnvApiKey:
    GroqApiKeyOne: str = os.getenv('groqapikeyone')
    GroqApiKeyTwo: str = os.getenv('groqapikeytwo')
    GroqApiKeyThree: str = os.getenv('groqapikeythree')
    
class EnvApiEndPoint:
    GroqApiEndPoint: str = os.getenv('groqendpoint')

    