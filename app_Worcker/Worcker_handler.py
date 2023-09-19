from postgress_db.Postgress import Postgres
from telegramm.tg import TgClientWithFile
from telegramm.dcs import Message
from s3_MINIO.s3 import S3Client
from settings.settings import settings
import datetime






class Worker_handler:

    def __init__(self):
        self.token = settings.TELEGRAM_TOKEN
        self.s3 = S3Client(
            endpoint_url=settings.DSN_MINIO,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY
        )
        self.tg_client = TgClientWithFile(token=self.token)
        self.postgres = Postgres()





    async def handler(self, message):
        pool = await self.postgres.get_pool_by_dsn()
        r = Message.Schema().load(message)
        async with TgClientWithFile(settings.TELEGRAM_TOKEN) as tg_cli:
            if r.text != None:
                print(r.text)
                now = datetime.datetime.now()
                await self.postgres.insert_users(pool, [now, r.from_.first_name, r.from_.last_name,
                                                        r.from_.username, r.chat.id,
                                                        r.from_.id, None, r.text])
            elif r.photo != None:
                for k in r.photo:
                    now = datetime.datetime.now()
                    res_path = await tg_cli.get_file(k['file_id'])
                    print(res_path.file_path)
                    await self.s3.fetch_and_upload('tests', f'{res_path.file_path[7:]}',
                                                 f'{tg_cli.API_FILE_PATH}{tg_cli.token}/{res_path.file_path}')
                    await self.postgres.insert_users(pool, [now, r.from_.first_name, r.from_.last_name,
                                                                 r.from_.username, r.chat.id,
                                                            r.from_.id, res_path.file_path, r.text])
            elif r.document !=None:
                    res_path = await tg_cli.get_file(r.document['file_id'])
                    await self.s3.fetch_and_upload('tests', f'{r.document["file_name"]}',
                                                 f'{tg_cli.API_FILE_PATH}{tg_cli.token}/{res_path.file_path}')