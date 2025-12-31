from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from filters.chanel import CheckUsersSub
from keyboards.inline.buttons import Chanels,Chanels_un
from loader import db

router = Router()

@router.message(CheckUsersSub())
async def not_sub(message: Message):
	await message.answer(f"iltimos kanalga obuna boling !",reply_markup=await Chanels())

@router.callback_query(F.data == "tek")
async def check_sub_again(call: CallbackQuery):
	chanels_id = await db.select_chanels()
	unsub = []
	for i in chanels_id:
		kanal_id = i['chanel_id']
		user_status = await call.bot.get_chat_member(kanal_id, call.from_user.id)
		if user_status.status == 'left':
			unsub.append(i['chanel_link'])
	if unsub:
		await call.message.answer(f"Siz kanalga obuna boling !",reply_markup=await Chanels_un(unsub=unsub))	
	else:		
		await call.answer("Sizga mumkin",show_alert=True)
		
