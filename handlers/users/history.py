from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.services.api import fetch_history
from utils.text import history_text
from keyboards.inline.buttons import history_kb
from loader import db

router = Router()



@router.callback_query(F.data == "history")
async def history_start(call: CallbackQuery):
    telegram_id = call.from_user.id
    access = (await db.get_token(telegram_id))["access"]

    data = await fetch_history(telegram_id, access, page=1)

    items = data["results"]
    text = history_text(items)

    await call.message.edit_caption(
        caption=text,
        reply_markup=await history_kb(
            telegram_id=telegram_id,
            page=1,
            has_next=data.get("next") is not None,
            has_prev=False
        )
    )

@router.callback_query(F.data.startswith("history_page_"))
async def history_paginate(call: CallbackQuery):
    telegram_id = call.from_user.id
    page = int(call.data.split("_")[-1])

    access = (await db.get_token(telegram_id))["access"]
    data = await fetch_history(telegram_id, access, page)

    items = data["results"]
    text = history_text(items)

    await call.message.edit_caption(
        caption=text,
        reply_markup=await history_kb(
            telegram_id=telegram_id,
            page=page,
            has_next=data.get("next") is not None,
            has_prev=data.get("previous") is not None
        )
    )