"""
    MongoDB Atlas Configuration File for Main Server 
"""
# Import Headers
import mongoengine as me 
import dotenv
import logging
import os

# program configurations
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

host = os.getenv('MongoDbUrl')
if host:
    logger.info("Success: Mongodb Configurations Set Successfully.")
else:
    logger.error("Error: Mongodb Configurations Not Found")
    
# function portion
def establishConnection() -> None:
    """ Establish Connection with MongoDB Atlas """
    try:
        me.connect(db="InterviewService", host=host, alias="default")
        logger.info("Status: MongoDB Atlas Connection Established Successfully.")
    except Exception as e:
        logger.error(f"Error: Unexpected error occurs{e}")
    
def terminatedConnection() -> None: 
    """ Terminate Connection with MongoDB Atlas """
    try:
        me.disconnect(alias="default")
        logger.info("MongoDB Atlas Connection Terminated with Atlas.")
    except Exception as e:
        logger.error(f"Error: Unexpected Error Occurs{e}")