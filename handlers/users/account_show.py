from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
import httpx
from loader import db
from keyboards.inline.buttons import kb,account_kb
from utils.language import t  
from aiogram.types import FSInputFile

router = Router()

@router.callback_query(F.data == "account")
async def account_show(call: CallbackQuery):
    telegram_id = call.from_user.id

    token = await db.get_token(telegram_id=telegram_id)
    if not token:
        await call.message.answer(text=await t(telegram_id, 'account_not_logged'), reply_markup=kb(telegram_id=telegram_id))
        return

    access = token["access"]
    lang = await db.get_language(telegram_id=telegram_id)
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://127.0.0.1:8000/{lang}/api/account/",headers={"Authorization": f"Bearer {access}"},timeout=10)


    
    data = resp.json()
    photo = FSInputFile('media/logo.jpg')
    await call.message.edit_media(InputMediaPhoto(
        media=photo,caption=await t(telegram_id,'account_info',username=data['username'],balance=data['balance'],)
    ),reply_markup=await account_kb(telegram_id=telegram_id)
        
    )