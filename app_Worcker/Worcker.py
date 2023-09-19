import asyncio

from app_rabbitMQ.rabbit_client import RabbitClient




class Worker:

    def __init__(self, queue_name):
        self.is_running = False
        self.queue_name = queue_name
        self._task: list[asyncio.Task] = []

    async def _worker(self):
        while self.is_runing:
            async with RabbitClient() as rabbit:
                await rabbit.receive(self.queue_name)



    async def start(self):
        self.is_runing = True
        async with asyncio.Semaphore(5):
            await asyncio.gather(*[self._worker() for _ in range(5)])




start_worcker = Worker(queue_name='hello')
async def start_worker():
    await start_worcker.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_worker())
    loop.run_forever()

