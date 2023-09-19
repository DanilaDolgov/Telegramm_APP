import aiosqlite


class sqllite_DB():
    def __init__(self, DSN: str = ''):
        self.DSN = DSN

    async def insert_records(self, my_tuple):
        async with aiosqlite.connect(self.DSN) as db:
            await db.execute("""INSERT INTO table_id (update_id, chat_id) VALUES (?, ?);""", my_tuple)
            await db.commit()

    async def create_table(self):
        async with aiosqlite.connect(self.DSN) as db:
            await db.execute('''CREATE TABLE table_id (
                                update_id TEXT NOT NULL,
                                chat_id text NOT NULL);''')
            await db.commit()

    async def select_id(self, chat_id):
        async with aiosqlite.connect(self.DSN) as db:
            async with db.execute("SELECT * FROM table_id where chat_id=? order by update_id desc", (chat_id,)) as cursor:
               return await cursor.fetchone()




