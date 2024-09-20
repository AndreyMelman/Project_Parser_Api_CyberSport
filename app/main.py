import logging
import asyncio
from contextlib import asynccontextmanager

from task.collector import collector
from task.used_bot import tg_bot
from task.spamer import spammer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def main():
    task1 = asyncio.create_task(collector())
    # Запускаем бота
    task2 = asyncio.create_task(tg_bot())

    task3 = asyncio.create_task(spammer())

    await asyncio.gather(task1, task2, task3)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(f"Выход из бота")
