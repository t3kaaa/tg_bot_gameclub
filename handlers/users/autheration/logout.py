from aiogram import Router, F
from aiogram.types import CallbackQuery

from loader import db
from keyboards.inline.buttons import kb
from utils.language import t

router = Router()


@router.callback_query(F.data == "logout")
async def logout_user(call: CallbackQuery):
    telegram_id = call.from_user.id

    await db.delete_token(telegram_id=telegram_id)

    await call.message.edit_caption(caption=await t(telegram_id=telegram_id, key="logout_success" ),reply_markup=await kb(telegram_id=telegram_id))
