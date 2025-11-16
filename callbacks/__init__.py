"""
Callbacks package for pip-docs application.
"""

import logging

logger = logging.getLogger(__name__)
logger.info("[Callbacks Package] Initializing callbacks package")

# Import all callback modules here to ensure they're registered
from . import chat_callbacks

logger.info("[Callbacks Package] All callbacks imported successfully")