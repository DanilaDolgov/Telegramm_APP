from typing import Type, Any
from types import TracebackType
from aio_pika import connect, Message

from app_Worcker.Worcker_handler import Worker_handler
from settings.settings import settings


print(settings.rabbit_dsn)



class RabbitClient():

    def __init__(self):
        self.connect_rabbit: connect = connect(url=settings.rabbit_dsn)


    async def put(self, message_data: Any, queue_name: str):
        # Creating a channel
        connection = await self.connect_rabbit
        channel = await connection.channel()
        # Declaring queue
        callback_queue = await channel.declare_queue(queue_name)
        # Sending the message
        await channel.default_exchange.publish(
            Message(str(message_data).encode(), reply_to=callback_queue.name),
            routing_key=queue_name,
        )

    # @classmethod
    # async def on_message(cls, message: IncomingMessage):
    #     async with message.process():
    #         result = message.body.decode()
    #         # await cls.handler(result)



    async def receive(self, queue_name: str):
        # channel = await connection.channel()
        # await channel.set_qos(prefetch_count=1)
        # queue = await channel.declare_queue(queue_name)
        # await queue.consume(cls.on_message, no_ack=False)
        connection = await self.connect_rabbit
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    result = message.body.decode()
                    print(eval(result))
                    await Worker_handler().handler(eval(result))



    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: None, exc: None, tb: None):
        self.connect_rabbit.close()
