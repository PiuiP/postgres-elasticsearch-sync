import os
from dotenv import load_dotenv
load_dotenv()

import time
import logging

from app.config import SYNC_INTERVAL_SECONDS
from app.sync import SyncService

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)  #не ошибка, если уже есть

log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    try:
        sync_service = SyncService("articles")
        while True:
            try:
                logger.info(f'Sync is starting')
                sync_service.sync_articles()
                
                logger.info(f'Sync completed, sleeping for {SYNC_INTERVAL_SECONDS} seconds')
                time.sleep(SYNC_INTERVAL_SECONDS)
                
            except KeyboardInterrupt:
                logger.info("Received stop signal, shutting down gracefully...")
                break
            except Exception as e:
                logger.error(f'Sync error: {e}')
                logger.info(f'Waiting {SYNC_INTERVAL_SECONDS} seconds before retry...')
                time.sleep(SYNC_INTERVAL_SECONDS)
    except Exception as e:
        logger.error(f"Failed to initialize sync service: {e}")
        raise

if __name__ == '__main__':
    main()