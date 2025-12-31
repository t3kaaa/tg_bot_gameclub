from loader import db
from datetime import datetime, timedelta

ACCESS_EXPIRE_MINUTES = 15  

async def get_valid_access(telegram_id: int):
    
    token_data = await db.get_token(telegram_id)
    if not token_data:
        return None

    access, refresh, expires_at = token_data['access'], token_data['refresh'], token_data['expires_at']

    # agar access hali ham amal qilsa
    if expires_at > datetime.now():
        return access

    # access muddati tugagan, refresh orqali yangilash
    new_access, new_expires_at = await refresh_access(refresh)
    if not new_access:
        return None

    # bazaga yangilangan token va expires_at ni saqlash
    await db.update_access(telegram_id, new_access, new_expires_at)
    return new_access

async def refresh_access(refresh_token: str):

    new_access = f"access_{refresh_token[-4:]}_{int(datetime.utcnow().timestamp())}"
    new_expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    return new_access, new_expires_at