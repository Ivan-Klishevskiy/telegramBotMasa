from aiosqlite import connect


class TopicRep:

    @staticmethod
    async def get_all_topics():
        async with connect('data/topics.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM topics")
            return await cursor.fetchall()

    @staticmethod
    async def create_topic(username, message):
        async with connect('data/topics.db') as db:
            cursor = await db.cursor()
            await cursor.execute("INSERT INTO topics (username, topic, votes) VALUES (?, ?, 0)", (username, message))
            await db.commit()

    @staticmethod
    async def check_user_voted(telegram_id: int, topic_id: int) -> bool:
        async with connect('data/votes.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM votes WHERE telegram_id = ? AND topic_id = ?", (telegram_id, topic_id))
            vote = await cursor.fetchone()

        return vote is not None

    @staticmethod
    async def update_topic_count_voice(topic_id):
        async with connect('data/topics.db') as db:
            cursor = await db.cursor()
            await cursor.execute("UPDATE topics SET votes = votes + 1 WHERE id = ?", (topic_id,))
            await db.commit()

    @staticmethod
    async def create_voice(telegram_id, topic_id):
        async with connect('data/votes.db') as db:
            cursor = await db.cursor()
            await cursor.execute("INSERT INTO votes (telegram_id, topic_id) VALUES (?, ?)",
                                 (telegram_id, topic_id))
            await db.commit()

    @staticmethod
    async def delete_topic(topic_id):
        async with connect('data/topics.db') as db:
            cursor = await db.cursor()
            await cursor.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
            await db.commit()
