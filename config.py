SOURCE = "/mnt"
DEST = "/mnt/target_nfs"
BATCH_SIZE = 500
MAX_PARALLEL_RSYNC = 4
DEBOUNCE_SECONDS = 10
DELETE_INTERVAL_SECONDS = 600
LOG_FILE = "/var/log/parallel_fsync.log"
INCLUDE_PATTERNS = ["*"]
EXCLUDE_PATTERNS = None
EXCLUDE_DIRS = [
    "/mnt/nfs/cache",
    "/mnt/nfs/temp/**"
]