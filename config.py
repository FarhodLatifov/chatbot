"""Configuration module for the Hashtag Generator Bot."""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Hashtag block settings
BLOCK_SIZE = 30  # Number of hashtags per block

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
