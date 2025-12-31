from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import httpx

from loader import db
from keyboards.inline.buttons import are_you_sure, main_kb, kb
from states.test import RegisterState
from utils.language import t  # <-- t() funksiyasi import qilindi

router = Router()


@router.callback_query(F.data == "register")
async def register_start(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    await call.message.answer(await t(telegram_id, "username_prompt"))
    await state.set_state(RegisterState.username)


@router.message(RegisterState.username)
async def register_username(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    await state.update_data(username=message.text.strip())
    await message.answer(await t(telegram_id, "password_prompt"))
    await state.set_state(RegisterState.password1)


@router.message(RegisterState.password1)
async def register_password1(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    await state.update_data(password1=message.text.strip())
    await message.answer(await t(telegram_id, "password_repeat_prompt"))
    await state.set_state(RegisterState.password2)


@router.message(RegisterState.password2)
async def register_password2(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    data = await state.get_data()
    password1 = data.get("password1")
    password2 = message.text.strip()

    if password1 != password2:
        await message.answer(await t(telegram_id, "password_mismatch"))
        await state.set_state(RegisterState.password1)
        return

    await state.update_data(password2=password2)
    await message.answer(
        await t(telegram_id, "confirm_registration").format(username=data['username']),
        reply_markup=await are_you_sure(telegram_id=telegram_id)
    )
    await state.set_state(RegisterState.confirm)


@router.callback_query(RegisterState.confirm)
async def register_confirm(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    if call.data != "ha":
        await call.message.answer(await t(telegram_id, "cancelled"), reply_markup=await kb(telegram_id=telegram_id))
        await state.clear()
        return

    data = await state.get_data()
    username = data["username"]
    password = data["password1"]

    lang = await db.get_language(telegram_id=telegram_id)
    async with httpx.AsyncClient() as client:
        reg_resp = await client.post(
            f"http://127.0.0.1:8000/{lang}/api/register/",
            json={"username": username, "password": password},
            timeout=10
        )

        if reg_resp.status_code != 201:
            await call.message.answer(await t(telegram_id, "username_taken"), reply_markup=await kb(telegram_id=telegram_id))
            await state.clear()
            return

        token_resp = await client.post(
            f"http://127.0.0.1:8000/{lang}/api/token/",
            json={"username": username, "password": password},
            timeout=10
        )

        if token_resp.status_code == 200:
            tokens = token_resp.json()
            await db.set_token(telegram_id=telegram_id, access=tokens["access"], refresh=tokens["refresh"])
            await call.message.answer(await t(telegram_id, "registered_success"), reply_markup=await main_kb(telegram_id=telegram_id))
        else:
            await call.message.answer(await t(telegram_id, "token_error"), reply_markup=await kb(telegram_id=telegram_id))

    await state.clear()
