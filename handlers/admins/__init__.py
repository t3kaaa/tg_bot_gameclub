from aiogram import Router

from filters import ChatPrivateFilter
from . import admin


router = Router()
    
admin.router.message.filter(ChatPrivateFilter(chat_type=["private"]))

router.include_router(admin.router)
