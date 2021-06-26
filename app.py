import logging
import subprocess


def main():
    rsyncs = [
        'rsync -a --progress /data/files/ chris@192.168.1.132:/data/files/',
        'rsync -ar --ignore-errors --progress --delete-before /data/video/ chris@192.168.1.132:/data/video/',
        'rsync -ar --ignore-errors --progress --delete-before /data/k8s/ chris@192.168.1.132:/data/k8s/',
        'rsync -a --progress --delete-before /docker/ chris@192.168.1.132:/data/docker/',
        'rsync -a --progress --delete-before --delete-before /data/smb/ chris@192.168.1.132:/data/smb/'
    ]
    for rsync in rsyncs:
        logging.info(f"Running: {rsync}")
        subprocess_completed = subprocess.run(rsync, check=True, capture_output=True, text=True, shell=True)
        logging.info(f"{subprocess_completed.stdout}")
        if subprocess_completed.stderr:
            logging.error(f"{subprocess_completed.stderr}")
        logging.info(f"Completed: {rsync}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting")
    main()
