from aiosqlite import connect


class RequestRep:

    @staticmethod
    async def save_not_urgent_request(username: str, message: str):
        async with connect('data/requests.db') as db:
            cursor = await db.cursor()
            await cursor.execute("INSERT INTO not_urgent_requests (username, message) VALUES (?, ?)",
                                 (username, message,))
            await db.commit()

    @staticmethod
    async def save_urgent_request(username: str, message: str):
        async with connect('data/requests.db') as db:
            cursor = await db.cursor()
            await cursor.execute("INSERT INTO urgent_requests (username, message) VALUES (?, ?)", (username, message,))
            await db.commit()

    @staticmethod
    async def fetch_user_requests_by_username(username: str):
        async with connect('data/requests.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM urgent_requests WHERE username = ?", (username,))
            urgent_requests = await cursor.fetchall()
            await cursor.execute("SELECT * FROM not_urgent_requests WHERE username = ?", (username,))
            not_urgent_requests = await cursor.fetchall()
        return urgent_requests, not_urgent_requests

    @staticmethod
    async def get_all_urgent_requests():
        async with connect('data/requests.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM urgent_requests")
            urgent_requests = await cursor.fetchall()
        return urgent_requests

    @staticmethod
    async def get_all_not_urgent_requests():
        async with connect('data/requests.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM not_urgent_requests")
            not_urgent_requests = await cursor.fetchall()
        return not_urgent_requests

    @staticmethod
    async def delete_request(username: str, message: str, urgent: bool):
        async with connect('data/requests.db') as db:
            cursor = await db.cursor()
            table = "urgent_requests" if urgent else "not_urgent_requests"
            await cursor.execute(f"DELETE FROM {table} WHERE username = ? AND message = ?", (username, message))
            await db.commit()

    @staticmethod
    async def delete_request_madrih(message: str, urgent: bool):
        async with connect('data/requests.db') as db:
            cursor = await db.cursor()
            table = "urgent_requests" if urgent else "not_urgent_requests"
            await cursor.execute(f"DELETE FROM {table} WHERE AND message = ?", (message,))
            await db.commit()
