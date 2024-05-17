from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from translations import _

def main_menu(lang):
    Main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text = _('📑 Estadísticas', lang), callback_data='UsersStatistics')
    ],
    [
        InlineKeyboardButton(text=_('🇪🇸 Cambiar de idioma', lang), callback_data='change_lang')
    ],
    [
        InlineKeyboardButton(text=_('Actualizar', lang), callback_data='Refresh_menu')
    ]
    ])
    return Main

def group_kb(link):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="unirse a un grupo", url=link)]
    ])
    return keyboard

def stats_kb(lang):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('Volver al menú', lang), callback_data='Refresh_menu')]
    ])
    return keyboard
