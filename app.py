import logging
import subprocess
from aiokafka import AIOKafkaConsumer
import asyncio
from configurator.utility import get_config


async def run_rsyncs():
    await asyncio.sleep(1)
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


async def consume():
    consumer = AIOKafkaConsumer(
        get_config('KAFKA_TOPIC'),
        bootstrap_servers=get_config('KAFKA_BOOSTRAP_SERVER'),
        group_id="nas-backup-runner")
    # Get cluster layout and join group `nas-backup-runner`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            await run_rsyncs()
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting")
    asyncio.run(consume())
