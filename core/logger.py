# ========================================
# Nexus Manager - Logger
# Desenvolvido por @079byfael • Frost Applications • UDO
# github.com/NextStore992/Bot-Manager---Beta-test
# ========================================

import logging
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/manager.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

def get_logger():
    return logging.getLogger("NexusManager")