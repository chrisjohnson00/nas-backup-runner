import logging
import subprocess


def main():
    rsyncs = [
        'rsync -a --progress /data/files/ chris@192.168.1.132:/data/files/ >> /var/log/backup_files.log 2>&1',  # noqa: E501
        'rsync -ar --ignore-errors --progress --delete-before /data/video/ chris@192.168.1.132:/data/video/ >> /var/log/backup_videos.log 2>&1',  # noqa: E501
        'rsync -ar --ignore-errors --progress --delete-before /data/k8s/ chris@192.168.1.132:/data/k8s/ >> /var/log/backup_k8s.log 2>&1',  # noqa: E501
        'rsync -a --progress --delete-before /docker/ chris@192.168.1.132:/data/docker/ >> /var/log/backup_docker.log 2>&1',  # noqa: E501
        'rsync -a --progress --delete-before --delete-before /data/smb/ chris@192.168.1.132:/data/smb/ >> /var/log/backup_smb.log 2>&1'  # noqa: E501
    ]
    for rsync in rsyncs:
        logging.info(f"Running: {rsync}")
        subprocess.run(rsync, check=True)
        logging.info(f"Completed: {rsync}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting")
    main()
