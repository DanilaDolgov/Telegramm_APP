# -*- coding: utf-8 -*-
import contextlib
from contextvars import ContextVar
from threading import Lock

import asyncpg
from asyncpg import Pool


context = ContextVar("pool_context", default={})


class SingletonPool(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ApiPool(object, metaclass=SingletonPool):
    __pool = dict()
    _lock: Lock = Lock()

    @classmethod
    async def create(cls, name, *args, **kwargs):
        if name is None:
            name = 'root'
        if name in cls.__pool:
            raise asyncpg.InterfaceError(
                'this name already exists')
        else:
            pool = await asyncpg.create_pool(*args, **kwargs)
            cls.__pool[name] = pool
            print(cls.__pool)

    @classmethod
    async def close(cls, name):

        if name not in cls.__pool:
            raise KeyError(f'pool with name {name} does not exist')
        pool = cls.get_pool(name)
        await pool.close()
        cls.__pool.pop(name)

    @classmethod
    def get_pool(cls, name=None) -> Pool:
        if name is None:
            name = 'root'
        if name not in cls.__pool:
            raise KeyError(f'pool with name {name} does not exist')
        return cls.__pool.get(name)

    @classmethod
    def get_pool_names(cls):
        return cls.__pool

    @classmethod
    async def init_pools(cls, pool_connections: dict):
        for item in pool_connections:
            await cls.create(item, **pool_connections[item])

    # @classmethod
    # async def close_all(cls):
    #     queue = list(cls.__pool.keys())
    #     for pool in queue:
    #         try:
    #             await cls.close(pool)
    #         except Exception as exc:
    #             logger.error('не удалось корректно закрыть пул')
    #             logger.exception(exc)
    #
    #     for name in cls.__pool.keys():
    #         await cls.close(name)

    @classmethod
    @contextlib.asynccontextmanager
    async def transaction(cls):
        old_context = context.get()
        conn = old_context.get('conn')
        if conn is None:
            async with cls.get_pool().acquire() as conn:
                async with conn.transaction():
                    for _ in cls._bar(old_context, conn):
                        yield conn
        else:
            async with conn.transaction():
                for _ in cls._bar(old_context, conn):
                    yield conn

    @classmethod
    @contextlib.asynccontextmanager
    async def connection(cls):
        old_context = context.get()
        conn = old_context.get('conn')
        if conn is None:
            async with cls.get_pool().acquire() as conn:
                for _ in cls._bar(old_context, conn):
                    yield conn
        else:
            for _ in cls._bar(old_context, conn):
                yield conn


    @classmethod
    def _bar(cls, old_context, conn):
        new_context = {**context.get(), 'conn': conn, "level": old_context.get('level', 0) + 1}
        token = context.set(new_context)
        try:
            yield conn
        finally:
            context.reset(token)
