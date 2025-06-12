import asyncpg
import os

DB_URL = os.getenv("DATABASE_URL")  # Pon esto en Render y en tu .env local

async def init_db():
    conn = await asyncpg.connect(DB_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS exp (
            user_id TEXT PRIMARY KEY,
            experience INTEGER NOT NULL DEFAULT 0,
            level INTEGER NOT NULL DEFAULT 1
        );
    ''')
    await conn.close()

async def get_user_exp(user_id: str):
    conn = await asyncpg.connect(DB_URL)
    row = await conn.fetchrow('SELECT experience, level FROM exp WHERE user_id = $1', user_id)
    await conn.close()
    if row:
        return {'exp': row['experience'], 'level': row['level']}
    else:
        return {'exp': 0, 'level': 1}

async def set_user_exp(user_id: str, exp: int, level: int):
    conn = await asyncpg.connect(DB_URL)
    await conn.execute('''
        INSERT INTO exp (user_id, experience, level)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id) DO UPDATE SET experience = $2, level = $3
    ''', user_id, exp, level)
    await conn.close()

async def add_experience(user_id: str, amount: int):
    data = await get_user_exp(user_id)
    new_exp = data['exp'] + amount
    await set_user_exp(user_id, new_exp, data['level'])

async def get_experience(user_id: str):
    data = await get_user_exp(user_id)
    return data['exp']
