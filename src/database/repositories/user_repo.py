from aiosqlite import connect


class UserRep:

    @staticmethod
    async def get_user_by_username(username: str):
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = await cursor.fetchone()
            return user

    @staticmethod
    async def get_user_by_id(telegram_id: int):
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT username FROM users WHERE telegram_id = ?", (telegram_id,))
            username = await cursor.fetchone()
        return username

    @staticmethod
    async def get_user_by_login_pass(login: str, password: str):
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (login, password))
            user = await cursor.fetchone()
            return user

    @staticmethod
    async def update_user(telegram_id, username, password):
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("UPDATE users SET telegram_id = ? WHERE username = ? AND password = ?",
                                 (telegram_id, username, password))
            await db.commit()

    @staticmethod
    async def registr_user(telegram_id, username, password, last_name, apartment_number) -> bool:
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = await cursor.fetchone()

            if user is None:
                await cursor.execute("INSERT INTO users (telegram_id, username, password, last_name, apartment_number) "
                                     "VALUES (?, ?, ?, ?, ?)",
                                     (telegram_id, username, password, last_name, apartment_number))
                await db.commit()
                return True
            else:
                return False

    @staticmethod
    async def logout_user(telegram_id: int):
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("UPDATE users SET telegram_id = NULL WHERE telegram_id = ?", (telegram_id,))
            await db.commit()

    @staticmethod
    async def get_user_info_by_id(telegram_id: int):
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT last_name, apartment_number FROM users WHERE telegram_id = ?", (telegram_id,))
            user_info = await cursor.fetchone()
            return user_info

    @staticmethod
    async def get_user_info_by_username(username: str):
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT last_name, apartment_number FROM users WHERE username = ?", (username,))
            user_info = await cursor.fetchone()
            return user_info

    @staticmethod
    async def remove_telegram_id(telegram_id: int):
        async with connect('data/users.db') as db:
            cursor = await db.cursor()
            await cursor.execute("UPDATE users SET telegram_id = NULL WHERE telegram_id = ?", (telegram_id,))
            await db.commit()

