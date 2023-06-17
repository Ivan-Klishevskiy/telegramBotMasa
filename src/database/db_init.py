from aiosqlite import connect
import logging


async def create_db():
    async with connect('data/topics.db') as db:
        cursor = await db.cursor()
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                votes INTEGER NOT NULL DEFAULT 0
            );
        """)
        await db.commit()
        logging.info("data/topics.db created or already exist")

    async with connect('data/users.db') as db:
        cursor = await db.cursor()
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """)
        await db.commit()
        logging.info("users.db created or already exist")

    async with connect('data/votes.db') as db:
        cursor = await db.cursor()
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                telegram_id INTEGER NOT NULL,
                topic_id INTEGER NOT NULL,
                PRIMARY KEY (telegram_id, topic_id)
            );
        """)
        await db.commit()
        logging.info("votes.db created or already exist")

    async with connect('data/requests.db') as db:
        cursor = await db.cursor()
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS urgent_requests (
                username TEXT NOT NULL,
                message TEXT NOT NULL
            );
        """)
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS not_urgent_requests (
                username TEXT NOT NULL,
                message TEXT NOT NULL
            );
        """)
        await db.commit()
        logging.info("requests.db created or already exist")