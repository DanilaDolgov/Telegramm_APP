import asyncio

from app_Worcker.Worcker import Worker
from settings.settings import settings
from app_Poller.Poller import Poller






poller = Poller(settings.TELEGRAM_TOKEN)
start_worcker = Worker(queue_name='hello_1')
async def start_app():
    await poller.start()
    await start_worcker.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_app())
    loop.run_forever()
