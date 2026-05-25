
# from AI_Agent_X.Config.GlobalEnv import EnvApiKey, EnvApiEndPoint
import asyncio
import httpx
import time 
import logging
import json

logger = logging.getLogger("uvicorn")
APIKEY: str = 'AIzaSyDAscjrMx-N36ypycnMRtufrLpIAfvGICI'
ENDPOINT: str = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-4-26b-a4b-it:generateContent"

async def NativeGemini2_5Flash(SystemInstruction: str) -> str:
    logger.info("Native OpenAi Gpt Oss 120B Model Triggered with the system instruction.")
    client = httpx.AsyncClient(timeout=60)
    
    payload: dict = {
        "contents": [
            {
                "parts": [
                    {
                        "text": SystemInstruction
                    }
                ]
            }
        ]
    }

    try: 
        response = await client.post(
            ENDPOINT,
            params={"key": APIKEY},
            data=json.dumps(payload)
        )

        data: dict  = response.json()
    except Exception as e:
        logger.error(f"Error: {e}")
        return "Error occurred while processing the request."
    logger.info("Model return the Expected response.")
    return data.get('candidates')[0].get('content').get('parts')[0].get('text')


# Remove this in production, this is just for testing the latency of the model response
if __name__ == "__main__":
    start = time.time()
    res =  asyncio.run(NativeGemini2_5Flash(SystemInstruction="what is python?"))
    end = time.time()
    print(f"time taken: {end-start}")
    print(res)