import os
from config import SOURCE, DEST
from logger import setup_logger

logger = setup_logger()

def build_file_set(base_path):
    file_set = set()
    for root, _, files in os.walk(base_path):
        for name in files:
            rel_path = os.path.relpath(os.path.join(root, name), base_path)
            file_set.add(rel_path)
    return file_set

def delete_missing_files():
    logger.info("Controllo file eliminati...")
    source_files = build_file_set(SOURCE)
    dest_files = build_file_set(DEST)
    to_delete = dest_files - source_files

    for rel_path in to_delete:
        full_path = os.path.join(DEST, rel_path)
        try:
            os.remove(full_path)
            logger.info(f"Eliminato: {full_path}")
        except FileNotFoundError:
            pass
        except Exception as e:
            logger.error(f"Errore eliminando {full_path}: {e}")
