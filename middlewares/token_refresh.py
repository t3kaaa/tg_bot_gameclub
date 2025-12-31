from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import db
from keyboards.inline.buttons import kb
from utils.language import t
from datetime import datetime
import httpx
from states.test import LoginState, RegisterState

class TokenRefreshMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = event.from_user.id

   
        state: FSMContext = data.get("state")
        current_state = await state.get_state() if state else None

        
        bypass_states = (
            LoginState.username.state,
            LoginState.confirm.state,
            RegisterState.username.state,
            RegisterState.password1.state,
            RegisterState.password2.state,
            RegisterState.confirm.state
        )
        if current_state in bypass_states:
            return await handler(event, data)

    
        if isinstance(event, CallbackQuery):
            event_text = event.data
        elif isinstance(event, Message):
            event_text = event.text
        else:
            event_text = None

        if event_text and event_text.startswith(("login", "register", "ha", "yoq")):
            return await handler(event, data)

   
        token_row = await db.get_token(user_id)

        if token_row:
            access, refresh = token_row['access'], token_row['refresh']

           
            if token_row.get('access_expires_at') and token_row['access_expires_at'] < datetime.now():
                new_tokens = await self.refresh_access(refresh, user_id)
                if new_tokens:
                    await db.set_token(
                        telegram_id=user_id,
                        access=new_tokens['access'],
                        refresh=new_tokens['refresh']
                    )
                else:
                    await db.delete_token(user_id)
                    await event.answer(
                        await t(user_id, 'login_required'),
                        reply_markup=await kb(telegram_id=user_id)
                    )
        else:
          
            await event.answer(
                await t(user_id, 'login_required'),
                reply_markup=await kb(telegram_id=user_id)
            )

        return await handler(event, data)

    async def refresh_access(self, refresh_token, telegram_id):
        lang = await db.get_language(telegram_id)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"http://127.0.0.1:8000/{lang}/api/token/refresh/",
                json={"refresh": refresh_token}
            )
            if resp.status_code == 200:
                return resp.json()
        return None
