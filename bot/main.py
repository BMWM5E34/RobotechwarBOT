import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, callback_query, FSInputFile, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, exception
from aiogram.enums.chat_member_status import ChatMemberStatus
import aiogram.exceptions as exceptions

# Other
import time
from translations import _
from bot import keyboard as kb
from bot.settings import bot_token

import bot.settings as st

import Database.db as db

class LanguageSwitch(StatesGroup):
    SWITCHING = State()

bot = Bot(token=bot_token)

bot_link = "https://t.me/Robotechwar_w_bot?start=ref_"

group_link = f"https://t.me/Robotechwargame"

group_id = -1002096387913
# -1002139542888

# bot_link = "https://t.me/Robotechwar_w_bot?start=ref_"

# group_link = f"https://t.me/test4invbot"

# group_id = -1002096387913

async def check_user_in_group(user_id: int, chat_id: int) -> bool:
    bot = Bot(token=bot_token)
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)
        return chat_member.status != ChatMemberStatus.LEFT and chat_member.status != ChatMemberStatus.KICKED
    except exceptions.ChatNotFound:
        return False
    except exceptions.UserNotFound:
        return False

def startBOT(dp: Dispatcher):
    @dp.message(CommandStart())
    async def cmd_start(message: Message, state: FSMContext):
        user_id = message.from_user.id

        username = f"@{message.from_user.username}"
        await db.AddUser(user_id, username, 0)
        Number_of_invites = await db.GetAmount(user_id)
        first_name = message.from_user.first_name if message.from_user.first_name else ""

        set_lang = "sp"
        await state.update_data(lang=set_lang)

        state_data = await state.get_data()
        lang = state_data.get('lang')

        link = f"{bot_link}{user_id}"
        command_args = message.text.split()[1:]
        
        if command_args and command_args[0].startswith("ref_"):
            referrer_id = int(command_args[0].split("_")[1])
            if referrer_id == user_id:
                await message.answer(_("No puede utilizar su enlace de referencia", lang) + " 😋")
                await message.answer(f"👋 {_('Hola', lang)} {first_name}, {_('Invita a gente al grupo y consigue un premio', lang)}\n\n🫂 {_('Invitaste a', lang)}: {Number_of_invites}\n\n🔗 {_('Tu enlace de invitación:', lang)}\n{link}", reply_markup=kb.main_menu(lang))
                return

            is_existing = await db.user_in_invited_referrals(user_id)
            if is_existing == True:
                await message.answer(_("You can no longer use the referral link", lang) + " 😋")
            else:
                await message.answer("👌 " + (_("Ir a nuestro grupo", lang)), reply_markup=kb.group_kb(group_link))

                await asyncio.sleep(60)

                result = await check_user_in_group(user_id, group_id)
                if result is True:
                    await bot.send_message(referrer_id, f"⭐️ {_('Your link took 1 user to the group', lang)}")
                    await db.increase_amount(referrer_id)
                    await db.insert_referrer(referrer_id, user_id)
                    await db.insert_invited_referral(user_id)
                else:
                    await bot.send_message(user_id, f"⭐️ {_('La invitación ha caducado, por favor, siga el enlace de referencia de nuevo y ejecute el bot para iniciar sesión correctamente en el grupo', lang)}\n\n🔗 {link}")
        else:
            await message.answer(f"👋 {_('Hola', lang)} {first_name}, {_('Invita a gente al grupo y consigue un premio', lang)}\n\n🫂 {_('Invitaste a', lang)}: {Number_of_invites}\n\n🔗 {_('Tu enlace de invitación:', lang)}\n{link}", reply_markup=kb.main_menu(lang))

    @dp.message(F.text == "DWLSLL92341::dmmAA")
    async def Clear_Data(message: Message):
        await db.reset_database()

    @dp.callback_query(F.data == 'UsersStatistics')
    async def UsersStatistics(callback_query: types.CallbackQuery, state: FSMContext):
        state_data = await state.get_data()
        lang = state_data.get('lang')

        conn = db.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, amount FROM users ORDER BY amount DESC LIMIT 10")
        top_users = cursor.fetchall()
        conn.close()

        message_text = f"⭐️ {_('Los 10 primeros usuarios por número de invitaciones al grupo', lang)}\n\n"
        for i, (username, amount) in enumerate(top_users, 1):
            if i == 1:
                message_text += f"🏆 {username} - {amount}\n"
            elif i == 2:
                message_text += f"🥈 {username} - {amount}\n"
            elif i == 3:
                message_text += f"🥉 {username} - {amount}\n"
            else:
                message_text += f"{username} - {amount}\n"

        await callback_query.message.edit_text(message_text, reply_markup=kb.stats_kb(lang))

    @dp.callback_query(F.data == 'Refresh_menu')
    async def Refresh_menu(callback_query: types.CallbackQuery, state: FSMContext):
        first_name = callback_query.from_user.first_name if callback_query.from_user.first_name else ""
        user_id = callback_query.from_user.id
        link = f"{bot_link}{user_id}"

        Number_of_invites = await db.GetAmount(user_id)
        await callback_query.message.delete()
        state_data = await state.get_data()
        lang = state_data.get('lang')
        await callback_query.message.answer(f"👋 {_('Hola', lang)} {first_name}, {_('Invita a gente al grupo y consigue un premio', lang)}\n\n🫂 {_('Invitaste a', lang)}: {Number_of_invites}\n\n🔗 {_('Tu enlace de invitación:', lang)}\n{link}", reply_markup=kb.main_menu(lang))

    @dp.message(Command("set_sending_time"))
    async def set_sending_time(message: Message):
        user_id = message.from_user.id
        if user_id != st.admin_id:
            await message.answer(f"no puede utilizar este comando")
            return
        
        try:
            delay_seconds = int(message.text.split(maxsplit=1)[1])

            await message.answer(f"Ha establecido correctamente la hora de envío de las estadísticas.")
            await asyncio.sleep(delay_seconds * 86400)

            conn = db.create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT username, amount FROM users ORDER BY amount DESC LIMIT 10")
            top_users = cursor.fetchall()
            conn.close()

            message_text = f"⭐️ Los 10 primeros usuarios por número de invitaciones al grupo\n\n"
            for i, (username, amount) in enumerate(top_users, 1):
                if i == 1:
                    message_text += f"🏆 {username} - {amount}\n"
                elif i == 2:
                    message_text += f"🥈 {username} - {amount}\n"
                elif i == 3:
                    message_text += f"🥉 {username} - {amount}\n"
                else:
                    message_text += f"{username} - {amount}\n"

            await bot.send_message(group_id, message_text)
            await message.answer(f"Las estadísticas se enviaron al grupo.")
        except (ValueError, TypeError, IndexError):
            await message.answer("Formato de comando incorrecto. Utilice /set_sending_time <número de segundos>.")

    @dp.callback_query(F.data == 'change_lang')
    async def change_lang(callback_query: types.CallbackQuery, state: FSMContext):
        first_name = callback_query.from_user.first_name if callback_query.from_user.first_name else ""
        state_data = await state.get_data()
        lang = state_data.get('lang')
        if lang == 'sp':
            await state.update_data(lang="en")
            lang = "en"
        else:
            await state.update_data(lang="sp")
            lang = "sp"
            
        user_id = callback_query.from_user.id
        link = f"{bot_link}{user_id}"
        Number_of_invites = await db.GetAmount(user_id)

        await callback_query.message.delete()
        await callback_query.message.answer(f"👋 {_('Hola', lang)} {first_name}, {_('Invita a gente al grupo y consigue un premio', lang)}\n\n🫂 {_('Invitaste a', lang)}: {Number_of_invites}\n\n🔗 {_('Tu enlace de invitación:', lang)}\n{link}", reply_markup=kb.main_menu(lang))
