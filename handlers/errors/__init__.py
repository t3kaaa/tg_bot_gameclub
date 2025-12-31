from aiogram import Router

from filters import ChatPrivateFilter
from . import error_handler

router = Router()
    

router.include_routers(error_handler.router)
