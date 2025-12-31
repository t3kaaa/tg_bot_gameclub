from aiogram import Router


def setup_routers() -> Router:
    from . import users
    from . import errors
    from . import admins
    
    from .users import autheration
    from .users import main
    router = Router()

    router.include_routers(admins.router, users.router,errors.router, autheration.router)

    return router
