import os
import sys
from loguru import logger

REQUIRED_ENV_VARS = [
    "GROQ_API_KEY",
    "DATABASE_URL",
    "REDIS_URL",
    "JWT_SECRET"
]

def validate_config():
    """
    Verify that all required environment variables are set.
    Fails the application startup if any are missing.
    """
    missing_vars = []
    
    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if not value or value == "your_key_here" or value == "your_secret_here":
            missing_vars.append(var)
            
    if missing_vars:
        logger.error("CRITICAL CONFIGURATION ERROR: Missing required environment variables.")
        for var in missing_vars:
            logger.error(f"  - {var} is not set or contains the default placeholder.")
            
        logger.info("Please refer to .env.example and create a .env file with valid credentials.")
        sys.exit(1)
        
    logger.info("Configuration validation successful. All required secrets are present.")

if __name__ == "__main__":
    validate_config()
