from aiogram import Router
from . import login
from . import register
from . import logout

router = Router()







router.include_routers(login.router, register.router, logout.router)
