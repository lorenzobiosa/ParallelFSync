import asyncio
import os
import tempfile
from config import SOURCE, DEST, BATCH_SIZE, MAX_PARALLEL_RSYNC
from logger import setup_logger

logger = setup_logger()
last_state = {}

def detect_changes(files):
    changed = []
    global last_state

    for path, mtime, size in files:
        rel_path = os.path.relpath(path, SOURCE)
        key = rel_path
        if key not in last_state or last_state[key] != (mtime, size):
            changed.append(rel_path)
            last_state[key] = (mtime, size)

    return changed

async def run_rsync_batch(batch_paths):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        for path in batch_paths:
            tmp.write(f"{path}\n")
        tmp_path = tmp.name

    cmd = [
        "rsync", "-azHAX", "--delete", "--files-from", tmp_path,
        "--relative", SOURCE + "/", DEST
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    async for line in process.stdout:
        logger.info(line.decode().strip())

    await process.wait()
    os.remove(tmp_path)

async def sync_changes(changed_paths):
    if not changed_paths:
        return

    logger.info(f"{len(changed_paths)} file(s) da sincronizzare")
    batches = [changed_paths[i:i + BATCH_SIZE] for i in range(0, len(changed_paths), BATCH_SIZE)]
    tasks = []
    sem = asyncio.Semaphore(MAX_PARALLEL_RSYNC)

    async def limited_rsync(batch):
        async with sem:
            await run_rsync_batch(batch)

    for batch in batches:
        tasks.append(asyncio.create_task(limited_rsync(batch)))

    await asyncio.gather(*tasks)
