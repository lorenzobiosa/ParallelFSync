import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import os

def run_rsync(line):
    source, dest = line.split(',', 1)

    command = [
        'rsync', '-azHAXv', '--delete', source, dest
    ]

    with open('rsync.log', 'a', encoding='utf-8', errors='surrogateescape') as log_file:
        log_file.write(f'{datetime.now()} - Start: {source} -> {dest}\n')
        subprocess.run(command, stdout=log_file, stderr=log_file)
        log_file.write(f'{datetime.now()} - End: {source} -> {dest}\n')

def main():
    with open('rsync.log', 'a') as log_file:
        log_file.write(f'{datetime.now()} - Start of sync process\n')

    with open('files.txt', 'r', encoding='utf-8', errors='surrogateescape') as file:
        lines = file.readlines()

    with ProcessPoolExecutor(max_workers=os.cpu_count()*4) as executor:
        futures = [executor.submit(run_rsync, line.strip('\n\r\t\f\v')) for line in lines]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Errore: {e}')

    with open('rsync.log', 'a') as log_file:
        log_file.write(f'{datetime.now()} - End of sync process\n')

if __name__ == '__main__':
    main()
