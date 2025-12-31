from aiogram import Router,F
from aiogram.types import Message,input_file
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loader import db
from keyboards.inline.buttons import are_you_sure
from states.test import AdminState
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from utils.pgtoexcel import export_to_excel


router = Router()


@router.message(Command('allusers'), IsBotAdminFilter(ADMINS))
async def get_all_users(message: Message):
    users = await db.select_all_users()
    file_path = f"data/users_list.xlsx"
    await export_to_excel(data=users, headings=['ID', 'Full Name', 'Username', 'Telegram ID'], filepath=file_path)
    await message.answer_document(input_file.FSInputFile(file_path))


@router.message(Command('cleandb'), IsBotAdminFilter(ADMINS))
async def ask_are_you_sure(message: Message, state: FSMContext):
    msg = await message.reply("Haqiqatdan ham bazani tozalab yubormoqchimisiz?", reply_markup= await are_you_sure())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(AdminState.are_you_sure)
