from aiogram.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()


class LoginState(StatesGroup):
    username = State()
    confirm = State()


class RegisterState(StatesGroup):
    username=State()
    password1=State()
    password2=State()
    confirm=State()
    
class BookingState(StatesGroup):
    choose_time = State()
    choose_hours = State()
    confirm = State()