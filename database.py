# database.py
import aiosqlite



DB_NAME = "referal.db"

# Jadval yaratish
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # Users jadvali
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            invited_by INTEGER,
            referrals INTEGER DEFAULT 0,
            group_link_sent INTEGER DEFAULT 0
        )
        """)

        # Referrals jadvali
        await db.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inviter_id INTEGER,
            new_user_id INTEGER UNIQUE
        )
        """)
        await db.commit()


# Yangi user qo‘shish
async def add_user(user_id: int, username: str = None, invited_by: int = None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT OR IGNORE INTO users (user_id, username, invited_by)
        VALUES (?, ?, ?)
        """, (user_id, username, invited_by))
        await db.commit()


# User mavjudligini tekshirish
async def user_exists(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as cur:
            return await cur.fetchone() is not None


# Referral qo‘shish
async def add_referral(inviter_id: int, new_user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute(
                "INSERT INTO referrals (inviter_id, new_user_id) VALUES (?, ?)",
                (inviter_id, new_user_id)
            )
            await db.execute(
                "UPDATE users SET referrals = referrals + 1 WHERE user_id = ?",
                (inviter_id,)
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


# Referral sonini olish
async def get_referrals_count(user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM referrals WHERE inviter_id = ?",
            (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


# Guruh linkini tekshirish
async def has_received_group_link(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT group_link_sent FROM users WHERE user_id = ?",
            (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return row and row[0] == 1


# Guruh linkini berilgan deb belgilash
async def mark_group_link_sent(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET group_link_sent = 1 WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()


# Eng ko‘p taklif qilganlar
async def get_top_referrers(limit: int = 10):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT inviter_id, COUNT(*) as cnt FROM referrals GROUP BY inviter_id ORDER BY cnt DESC LIMIT ?",
            (limit,)
        ) as cur:
            return await cur.fetchall()

# Referral sonini oshirish users jadvalida
async def increment_referrals(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        UPDATE users SET referrals = referrals + 1 WHERE user_id = ?
        """, (user_id,))
        await db.commit()

# database.py

# user kim tomonidan taklif qilinganini olish
async def get_inviter_id(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT invited_by FROM users WHERE user_id = ?",
            (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row and row[0] else None
