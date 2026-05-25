
from app.Config.GlobalEnv import EnvApiEndPoint, EnvApiKey
import asyncio
import httpx
import time 
import logging

logger = logging.getLogger("uvicorn")
APIKEY: str = EnvApiKey.GroqApiKeyTwo
ENDPOINT: str = EnvApiEndPoint.GroqApiEndPoint

async def NativeOpenaiGptOssModel120B(SystemInstruction: str) -> str:
    """
        This function is responsible for making the API call to the Groq endpoint and return the response from the model.
        It takes the system instruction as input and returns the response from the model as a string.
            Args:
                SystemInstruction (str): The system instruction to be sent to the model.
            Returns:
                str: The response from the model.
    """
    logger.info("Native Openai Gpt Oss 120B Model Triggered with the system instruction.")
    client = httpx.AsyncClient(timeout=60)
    
    payload: dict = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "user",
                "content": SystemInstruction
            }
        ]
    }

    try: 
        response = await client.post(
            ENDPOINT,
            headers={
                "Authorization": f"Bearer {APIKEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        data: dict  = response.json()
    except Exception as e:
        logger.error(f"Error: {e}")
        return "Error occurred while processing the request."
    logger.info("Model return the Expected response.")
    return data.get('choices')[0].get("message").get("content")


# Remove this in production, this is just for testing the latency of the model response
# if __name__ == "__main__":
#     start = time.time()
#     res =  asyncio.run(NativeOpenaiGptOssModel120B(SystemInstruction="what is python"))
#     end = time.time()
#     print(f"time taken: {end-start}")
#     print(res)