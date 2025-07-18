import os
import threading
from queue import Queue
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
from config import SOURCE, INCLUDE_PATTERNS, EXCLUDE_PATTERNS, EXCLUDE_DIRS

def should_include(path):
    path = Path(path)
    if INCLUDE_PATTERNS:
        return any(path.match(p) for p in INCLUDE_PATTERNS)
    if EXCLUDE_PATTERNS:
        return not any(path.match(p) for p in EXCLUDE_PATTERNS)
    return True

def should_exclude_dir(path):
    path = Path(path)
    return any(path.match(pattern) for pattern in EXCLUDE_DIRS)

def list_all_files():
    files = []
    lock = threading.Lock()
    dir_queue = Queue()
    dir_queue.put(SOURCE)

    stats = {
        "files": 0,
        "dirs": 0,
        "size": 0
    }

    def reporter():
        while not done_event.is_set():
            with lock:
                print(
                    f"\rScansionate: {stats['dirs']} dir | {stats['files']} file | {stats['size'] / (1024**3):.2f} GB size",
                    end="", flush=True
                )
            time.sleep(5)

    def worker():
        while True:
            try:
                current_dir = dir_queue.get(timeout=2)
            except:
                return
            if should_exclude_dir(current_dir):
                dir_queue.task_done()
                continue
            with lock:
                stats["dirs"] += 1
            try:
                for entry in os.scandir(current_dir):
                    if entry.is_file(follow_symlinks=False):
                        if should_include(entry.path):
                            try:
                                stat = entry.stat(follow_symlinks=False)
                                with lock:
                                    stats["files"] += 1
                                    stats["size"] += stat.st_size
                                    files.append((entry.path))
                            except FileNotFoundError:
                                continue
                    elif entry.is_dir(follow_symlinks=False):
                        if not should_exclude_dir(entry.path):
                            dir_queue.put(entry.path)
            except (PermissionError, FileNotFoundError):
                pass
            finally:
                dir_queue.task_done()

    num_threads = os.cpu_count() * 4
    done_event = threading.Event()

    reporter_thread = threading.Thread(target=reporter, daemon=True)
    reporter_thread.start()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(worker)
        dir_queue.join()

    done_event.set()
    print()

    return files

if __name__ == "__main__":
    print("Start date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Scanning files from:", SOURCE)
    all_files = list_all_files()
    print(f"\nFound {len(all_files)} files.")
    print("End date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Salva su file
    output_file = "file_list.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for path in all_files:
            f.write(f"{path}\n")
    print(f"File list written to {output_file}")