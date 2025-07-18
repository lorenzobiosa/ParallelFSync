import asyncio
import time
from scanner import list_all_files
from syncer import detect_changes, sync_changes
from deleter import delete_missing_files
from config import DEBOUNCE_SECONDS, DELETE_INTERVAL_SECONDS
from logger import setup_logger

logger = setup_logger()

async def run_sync_loop():
    delete_timer = time.time()

    while True:
        files = list_all_files()
        changed = detect_changes(files)
        await sync_changes(changed)

        if time.time() - delete_timer > DELETE_INTERVAL_SECONDS:
            delete_missing_files()
            delete_timer = time.time()

        await asyncio.sleep(DEBOUNCE_SECONDS)

if __name__ == "__main__":
    try:
        logger.info("Avvio servizio ParallelFSync...")
        asyncio.run(run_sync_loop())
    except KeyboardInterrupt:
        logger.warning("ParallelFSync interrotto manualmente.")
