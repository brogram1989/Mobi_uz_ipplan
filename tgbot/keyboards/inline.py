from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

MainMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📡Транспорт", callback_data='mw'),
        ],
        [
            InlineKeyboardButton(text='💻админ команды', callback_data='admin'),
        ],
    ],
)

MenuIP = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(text='🌏Информации о регионах', callback_data='region'),
        ],
        [
            InlineKeyboardButton(text="🔎поиск БС", callback_data='search'),
        ],
        [
            InlineKeyboardButton(text='📥Взять ip адрес для нового БС', callback_data='get_newip'),
        ],
        [
            InlineKeyboardButton(text='🆕🆔 взять новый NE-ID для РРЛ елемента', callback_data='get_neid'),
        ],
        [
            InlineKeyboardButton(text='🏘назад на меню', callback_data="to_mainmenu"),
        ],
    ],
)

MenuNeID = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='AND', callback_data='neid_and'),
            InlineKeyboardButton(text='FRG', callback_data='neid_frg'),
            InlineKeyboardButton(text='NAM', callback_data='neid_nam'),
        ],
        [
            InlineKeyboardButton(text='TSH-CHR', callback_data='neid_tsh'),
            InlineKeyboardButton(text='YAN', callback_data='neid_yan'),
            InlineKeyboardButton(text='SRD', callback_data='neid_srd'),
        ],
        [
            InlineKeyboardButton(text='DZH', callback_data='neid_dzh'),
            InlineKeyboardButton(text='SAM', callback_data='neid_sam'),
            InlineKeyboardButton(text='BHR', callback_data='neid_bhr'),
        ],
        [
            InlineKeyboardButton(text='KSH', callback_data='neid_ksh'),
            InlineKeyboardButton(text='SHA', callback_data='neid_sha'),
            InlineKeyboardButton(text='SRH', callback_data='neid_srh'),
        ],
        [
            InlineKeyboardButton(text='NAV', callback_data='neid_nav'),
            InlineKeyboardButton(text='KAR', callback_data='neid_kar'),
            InlineKeyboardButton(text='HRZ', callback_data='neid_hrz'),
        ],
        [
            InlineKeyboardButton(text='🔙назад', callback_data='mw'),
            InlineKeyboardButton(text='🏘назад на меню', callback_data='to_mainmenu'),
        ],
    ],
)

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💾работа с файламы", callback_data='file_works'),
        ],
        [
            InlineKeyboardButton(text="👥📝 управление с полномочиями", callback_data='admin_command'),
        ],
        [
            InlineKeyboardButton(text="🏘назад на меню", callback_data='to_mainmenu'),
        ],
    ]
       )
file_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬆️📂выгрузка IP_PLAN файл на сервер", callback_data='upload_ip_file'),
        ],
        [
            InlineKeyboardButton(text="⬇️📂загрузка IP_PLAN файл из сервера", callback_data='download_ip_file'),
        ],
        [
            InlineKeyboardButton(text="⬆️📂выгрузка NE_ID файл на сервер", callback_data='upload_neid_file'),
        ],
        [
            InlineKeyboardButton(text="🏘назад на меню", callback_data='to_mainmenu'),
        ],
    ]
       )

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕👤 добавить пользователь", callback_data='add_user'),
        ],
        [
            InlineKeyboardButton(text="👥📝 список пользователей", callback_data='list_users'),
        ],
        [
            InlineKeyboardButton(text="❌👤 удалить пользователя", callback_data='del_user'),
        ],
        [
            InlineKeyboardButton(text="✅🥷 сделать админом", callback_data='set_admin'),
        ],
        [
            InlineKeyboardButton(text="❌🥷 удалить из списки админа", callback_data='del_admin'),
        ],
        [
            InlineKeyboardButton(text="🏘назад на меню", callback_data='to_mainmenu'),
        ],
    ],
)