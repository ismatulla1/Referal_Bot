# utils.py
def generate_ref_link(bot_username: str, user_id: int) -> str:
    """Referal link yaratadi"""
    return f"https://t.me/{bot_username}?start={user_id}"
