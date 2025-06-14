import os
import asyncpg

DB_URL = os.getenv("DATABASE_URL")  # Pon esto en Render y en tu .env local

async def init_db():
    conn = await asyncpg.connect(DB_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS exp (
            user_id TEXT PRIMARY KEY,
            experience INTEGER NOT NULL,
            level INTEGER NOT NULL
        )
    ''')
    await conn.close()

async def get_user_exp(user_id: str):
    conn = await asyncpg.connect(DB_URL)
    row = await conn.fetchrow(
        'SELECT experience, level, username, avatar_url FROM exp WHERE user_id = $1', user_id
    )
    await conn.close()
    if row:
        return {
            "experience": row["experience"],
            "level": row["level"],
            "username": row["username"],
            "avatar_url": row["avatar_url"]
        }
    else:
        return {"experience": 0, "level": 1, "username": None, "avatar_url": None}

async def set_user_exp(user_id: str, exp: int, level: int, username: str, avatar_url: str):
    conn = await asyncpg.connect(DB_URL)
    await conn.execute(
        '''
        INSERT INTO exp (user_id, experience, level, username, avatar_url)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (user_id) DO UPDATE SET
            experience = $2,
            level = $3,
            username = $4,
            avatar_url = $5
        ''',
        user_id, exp, level, username, avatar_url
    )
    await conn.close()

async def add_experience(user_id: str, amount: int):
    user = await get_user_exp(user_id)
    new_exp = user["experience"] + amount
    level = user["level"]
    exp_needed = level * 100
    if new_exp >= exp_needed:
        level += 1
        new_exp = new_exp - exp_needed
    await set_user_exp(user_id, new_exp, level)

async def get_experience(user_id: str):
    user = await get_user_exp(user_id)
    return user["experience"]

async def get_full_ranking():
    conn = await asyncpg.connect(DB_URL)
    rows = await conn.fetch(
        'SELECT user_id, experience, level, username, avatar_url FROM exp ORDER BY level DESC, experience DESC'
    )
    await conn.close()
    return rows
