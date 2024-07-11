from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from tgbot.filters.admin import AdminFilter
from tgbot.config import ADMINS, USERS
from tgbot.states.personalData import AdminCommands
from aiogram.fsm.context import FSMContext
from aiogram.handlers import CallbackQueryHandler
from tgbot.keyboards.inline import admin_keyboard, admin_menu, file_menu

admin_router = Router()
admin_router.message.filter(AdminFilter())

# Check if the user is an admin

#______________________________________________________________________#
def is_admin(user_id: int):
    return user_id in ADMINS

def is_user(user_id: int):
    return user_id in USERS
def add_user(user_id: int ):
    if user_id not in USERS:
        USERS.append(user_id)
        return "админ добавлен успешно"
    else:
        return "нет такого админа!"

def del_user(user_id: int ):
    if user_id in USERS:
        USERS.remove(user_id)
        return "удалён успешно !"
    else:
        return "нет такого узера!"

def set_admin(user_id: int ):
    if user_id not in ADMINS:
        ADMINS.append(user_id)
        return "узер добавлен успешно "
    else:
        return "нет такого узера!"

def remove_admin(user_id: int ):
    if user_id in ADMINS:
        ADMINS.remove(user_id)
        return "удалён успешно !"
    else:
        return "нет такого админа!"

#______________________________________________________________________#
#admin komandasi
@admin_router.message(Command("admin"))
async def admin_comands(message: types.Message):
    await message.answer("выбирайте нужный вам кнопки!",
                         reply_markup=admin_menu)
@admin_router.callback_query(F.data == "admin")
async def admin_comands2(query: CallbackQuery):
    await query.answer("Menuni tanglang")
    await query.message.edit_text("выбирайте нужный вам кнопки!",
                                  reply_markup=admin_menu)
#______________________________________________________________________#


# We can use F.data filter to filter callback queries by data field from CallbackQuery object
# file_works callback query kelganda ishlaydigan handler
@admin_router.callback_query(F.data == "file_works")
async def file_work(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("выбирайте нужный вам кнопки!",
                                  reply_markup=file_menu)


#______________________________________________________________________#
# admin_command callback query kelganda ishlaydigan handler
@admin_router.callback_query(F.data == "admin_command")
async def admin_manage_uppon_users(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("выбирайте нужный вам кнопки!",
                                  reply_markup=admin_keyboard)


@admin_router.callback_query(F.data == "add_user")
async def admin_check(query: CallbackQuery, state: FSMContext):
    if is_admin(query.from_user.id):
        await query.answer("введите ID нового пользователя")
        await query.message.answer("Foydalanuvchi 🆔 sini aniqlash uchun https://t.me/username_to_id_bot dan foydalanishingiz mumkun")
        await state.set_state(AdminCommands.user_id)
    else:
        await query.answer("у Вас нет прав!")


#admin kirgizadigan useridni USERS listga yozish uchun handler

@admin_router.message(AdminCommands.user_id)
async def new_users_id(message: types.Message, state:FSMContext):
    try:
        # Get the comment from the message
        new_user = message.text
        new_user = int(new_user)
        add_user(new_user)
        await message.answer(f"siz id={new_user} foydalanuvchini bazaga kiritdingiz!\nBazada {len(USERS)} ta foydalanuvchi bor")
        # Finish the state
        await state.clear()
    except Exception as e:
        await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                            f"qaytadan urinib ko'ring!")
        await state.finish()

@admin_router.callback_query(F.data == "list_users")
async def list_users(query: CallbackQuery):
    if is_admin(query.from_user.id):
        # Your logic to delete a user here
        await query.answer("Списка пользователей")
        await query.message.edit_text(f"Bazada {len(USERS)} ta 👤 foydalanuvchi bor.\nFoydalanuvchilar ro'yxati\n"
                                            f"{USERS}")
        await query.message.answer(f"Bazada {len(ADMINS)} ta 🥷 admin bor.\nAdminlar ro'yxati\n{ADMINS}")
    else:
        await query.answer("Siz admin emasiz")



@admin_router.callback_query(F.data == "del_user")
async def delete_user(query: CallbackQuery, state: FSMContext):
    if is_admin(query.from_user.id):
        # Your logic to delete a user here
        await query.answer("введите ID пользователя которого Вы хотите удалить")
        await query.message.answer("Foydalanuvchini o'chirish, uning 🆔 sini kiriting. \n"
                                            "<code>🆔 faqatgina raqamlardan iborat ketma ketligdagi son</code>")
        await state.set_state(AdminCommands.del_user)
    else:
        await query.answer("Siz admin emasiz")



# #admin kirgizadigan useridni USERS listdan o'chirish uchun handler

@admin_router.message(AdminCommands.del_user)
async def del_users(message: types.Message, state:FSMContext):
    try:
        # Get the comment from the message
        user_id = message.text
        user_id = int(user_id)
        del_user(user_id)
        await message.answer(f"id={user_id} foydalanuvchi bazadan o'chirildi!\nBazada {len(USERS)} ta foydalanuvchi qoldi!")
        # Finish the state
        await state.clear()
    except Exception as e:
        await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                            f"qaytadan urinib ko'ring!")
        await state.clear()


@admin_router.callback_query(F.data == "set_admin")
async def set_new_admin(query: CallbackQuery, state:FSMContext):
    if is_admin(query.from_user.id):
        # Your logic to set a user as admin here
        await query.answer("введите ID пользователя которого Вы хотите назначить админом")
        await query.message.answer("Foydalanuvchini admin qilish uchun, uning 🆔 sini kiriting. \n"
                                    "<code>🆔 faqatgina raqamlardan iborat ketma ketligdagi son</code>")
        await state.set_state(AdminCommands.set_admin)
    else:
        await query.answer("Siz admin emasiz")

@admin_router.message(AdminCommands.set_admin)
async def new_admin(message: types.Message, state:FSMContext):
    try:
        # Get the comment from the message
        admin = message.text
        admin = int(admin)
        add_user(admin)
        set_admin(admin)
        await message.answer(f"siz id={admin} foydalanuvchini admin qilib belgiladingiz!\nBazada {len(ADMINS)} ta admin bor")
        # Finish the state
        await state.clear()
    except Exception as e:
        await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                            f"qaytadan urinib ko'ring!")
        await state.clear()

@admin_router.callback_query(F.data == "del_admin")
async def delete_admin(query: CallbackQuery, state: FSMContext):
    if is_admin(query.from_user.id):
        # Your logic to remove admin privileges from a user here
        await query.answer("userni adminlikdan chiqarish")
        await query.message.answer("Foydalanuvchini adminlar ro'yxatidan o'chirish uchun, uning 🆔 sini kiriting. \n"
                                            "<code>🆔 faqatgina raqamlardan iborat ketma ketligdagi son</code>")
        await state.set_state(AdminCommands.del_admin)
    else:
        await query.answer("Siz admin emasiz")


# #admin kirgizadigan useridni ADMINS listdan o'chirish uchun handler

@admin_router.message(AdminCommands.del_admin)
async def del_admin(message: types.Message, state:FSMContext):
    try:
        # Get the comment from the message
        user_id = message.text
        user_id = int(user_id)
        remove_admin(user_id)
        await message.answer(f"id={user_id} admin bazadan o'chirildi!\nBazada {len(ADMINS)} ta admin qoldi!")
        # Finish the state
        await state.clear()
    except Exception as e:
        await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                            f"qaytadan urinib ko'ring!")
        await state.clear()

#______________________________________________________________________#