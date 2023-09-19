import asyncio
import os
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import aiohttp
import requests

from telegramm.tg import TgClientWithFile
from telegramm.dcs import Message, UpdateObj, Message_castom
from sqlite.sqllite_db import sqllite_DB
from app_rabbitMQ.rabbit_client import RabbitClient
from settings.settings import settings
from postgress_db.Postgress import Postgres


storage = MemoryStorage()
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)


class Poller:

    def __init__(self, token):
        self.tg_client = TgClientWithFile(token)
        self.is_running = False
        self.sql = sqllite_DB(os.path.join(os.getcwd().replace('/app_Poller', ''), 'update_chat_id.db'))
        self._task = asyncio.Task
        # self.postgres = Postgres()

    async def _worker(self):
        while self.is_running:
            res = await self.tg_client.get_updates()
            print(res)
            if res['ok'] == True:
                for x in res['result']:
                    temp = []
                    [temp.append(y) for y in x.keys()]
                    if temp[1] == 'message':
                        r = Message.Schema().load(x['message'])
                        response_id = await self.sql.select_id(r.chat.id)
                        if response_id == None:
                            response_id = (0, 0)
                        if x['update_id'] > int(response_id[0]):
                            await self.sql.insert_records((x['update_id'], r.chat.id))
                            async with RabbitClient() as rabbit:
                                await rabbit.put(message_data=f"{x['message']}", queue_name='hello')
                            # await self.postgres.insert_users(pool, [r.from_.first_name, r.from_.last_name, r.from_.username])


    async def start(self):
        self.is_running = True
        # pool = await self.postgres.get_pool_by_dsn()
        self._task = await asyncio.create_task(self._worker())

poller = Poller(settings.TELEGRAM_TOKEN)

async def start():
    await poller.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()





