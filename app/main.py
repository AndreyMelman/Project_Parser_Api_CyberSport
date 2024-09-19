import logging
import asyncio

from task.collector import collector

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")



async def main():
    await collector()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(f'Выход из бота')
