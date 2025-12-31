from aiogram import Router


from . import start, help,account_show, main,history,book

router = Router()
    
router.include_routers(start.router,account_show.router, help.router, main.router,history.router,book.router)
