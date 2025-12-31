from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import db, bot
from data.config import ADMINS
from keyboards.inline.buttons import select_language, kb, main_kb
from utils.language import t
from utils.auth import get_valid_access
from aiogram.types import FSInputFile
router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    
    try:
        await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
        for admin in ADMINS:
            try:
                await bot.send_message(
                    chat_id=admin,
                    text=f"Yangi user {username}",
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            except Exception as error:
                logger.info(f"Data did not send to admin: {admin}. Error: {error}")
    except Exception as error:
        logger.info(error)

    
    lang = await db.get_language(telegram_id)
    
    if not lang:
        
        text = await t(telegram_id, 'choose_language', default_text="Iltimos tilni tanlang:\nПожалуйста, выберите язык:\nPlease select your language:")
        await message.answer(text, reply_markup=select_language)
        return
    
    token = await db.get_token(telegram_id=telegram_id)

    if not token:
            text = t(telegram_id, 'account_not_logged')
            await message.answer(text,reply_markup=await kb(telegram_id=telegram_id))
    
    else:
        photo = FSInputFile("media/logo.jpg")
        welcome_text = await t(telegram_id, 'welcome', username=message.from_user.full_name)
        main_text = await t(telegram_id, 'main_menu')
        await message.answer(welcome_text)
        await message.answer_photo(photo=photo,caption=main_text, reply_markup=await main_kb(telegram_id=telegram_id))

@router.callback_query(F.data.in_(['uz', 'ru', 'en']))
async def select_user_language(call: types.CallbackQuery):
    lang = call.data
    telegram_id = call.from_user.id
    await db.set_language(telegram_id=telegram_id, language=lang)

   
    token = await db.get_token(telegram_id)
    if not token:
        login_text = await t(telegram_id, 'login_required', default_text="❗ Siz tizimga kirmagansiz")
        await call.message.answer(login_text, reply_markup=await kb(telegram_id=telegram_id))
    else:
        main_text = await t(telegram_id, 'main_menu', default_text="Asosiy menyu:")
        await call.message.answer(main_text, reply_markup=await main_kb(telegram_id=telegram_id))