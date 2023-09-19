import asyncio
import datetime
from typing import Type
from types import TracebackType
import asyncpg

from settings.settings import settings


class Postgres:

    def __init__(self):
        self.dsn = settings.POSTGRES_DSN




    async def get_pool_by_dsn(self):
        return await asyncpg.create_pool(self.dsn)



    async def insert_users(self, pool, user_list):
        async with pool.acquire() as conn:
            query = await conn.fetchrow(
                "insert into users (date_time, first_name, last_name, username, chat_id, telegramm_id, filepath, text_data) values ($1, $2, $3, $4, $5, $6, $7, $8) returning *",
                user_list[0], user_list[1], user_list[2], user_list[3], user_list[4], user_list[5], user_list[6], user_list[7]
            )
        return print(query)








