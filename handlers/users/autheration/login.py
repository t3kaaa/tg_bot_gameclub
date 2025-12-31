from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import httpx
from loader import db
from keyboards.inline.buttons import main_kb, kb, are_you_sure
from states.test import LoginState
from utils.language import t 
from datetime import timedelta,datetime
from aiogram.types import FSInputFile

router = Router()

@router.callback_query(F.data == 'login')
async def login_ask_u_p(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    await call.message.answer(await t(telegram_id, 'login_ask'))
    await state.set_state(LoginState.username)
    await call.answer()  


@router.message(LoginState.username)
async def login_receive_data(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if ":" not in message.text:
        await message.answer(await t(telegram_id, 'login_wrong_format'))
        return

    username, password = message.text.split(":")
    await state.update_data(username=username, password=password)

    await message.answer(
        await t(telegram_id, 'login_confirm', username=username, password=password),
        reply_markup=await are_you_sure(telegram_id=telegram_id)
    )
    await state.set_state(LoginState.confirm)


@router.callback_query(LoginState.confirm)
async def login_confirm(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    data = await state.get_data()
    username = data.get("username")
    password = data.get("password")

    if call.data == "ha":
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "http://127.0.0.1:8000/uz/api/token/",
                json={"username": username, "password": password}
            )
        if resp.status_code == 200:
            token_data = resp.json()
            access_expires = datetime.now() + timedelta(minutes=60)  
            refresh_expires = datetime.now() + timedelta(days=5)    

            await db.set_token(
                telegram_id=telegram_id,
                access=token_data["access"],
                refresh=token_data["refresh"],
                access_expires_at=access_expires,
                refresh_expires_at=refresh_expires
            )
            photo = FSInputFile("media/logo.jpg")
            await call.message.answer_photo(photo=photo,caption=await t(telegram_id, 'login_success'), reply_markup=await main_kb(telegram_id=telegram_id))
        else:
            await call.message.answer(await t(telegram_id, 'login_failed'), reply_markup=await kb(telegram_id=telegram_id))
    else:
        await call.message.answer(await t(telegram_id, 'login_cancel'), reply_markup=await kb(telegram_id=telegram_id))

    await state.clear()
    await call.answer()
