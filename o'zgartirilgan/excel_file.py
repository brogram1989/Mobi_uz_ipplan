import io
import random
from io import BytesIO
import pandas as pd
from aiogram.enums import ParseMode
from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove, Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from .admin import is_admin, is_user
from tgbot.config import ADMINS, USERS
from tgbot.states.personalData import FindId
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from tgbot.config import load_config
from loader import bot
from tgbot.keyboards.dynamic_inlinekeyboard_builder import InlineKeyboardBuilder
from tgbot.keyboards.inline import MenuNeID

import logging
from pathlib import Path
from logging_config import setup_logging  # Import the setup_logging function

#_____________________________________________________________________________________#

#log fayllarni yozish uchun
# Set up logging
setup_logging()
logger = logging.getLogger("excel_file_logger")

#_____________________________________________________________________________________#
#log infolarni yig'ish uchun funksiyalar
def give_new_ip_to_base_station(ip_address, bs_id, bsnode_id, user_id, user_firstname):
    logger.info(f"New BS {bs_id} took new IP address {ip_address} from node {bsnode_id} by user_id {user_id} user_firstname is {user_firstname}")
    # Rest of the function logic

def change_base_station_ip(bs_id, old_ip, new_ip,old_node,new_node,user_id,user_firstname):
    logger.info(f"Changed {bs_id} IP address from {old_ip} node {old_node} to new IP address {new_ip} node {new_node} by user_id {user_id} user_first_name is {user_firstname}")
    # Rest of the function logic
def delete_ip_address(bs_id, ip, node, user_id, user_firstname):
    logger.info(f"Deleted {bs_id} IP address {ip} from {node} node by user_id {user_id} user_first_name is {user_firstname}")
    # Rest of the function logic
def file_uploaded(user_id, user_firstname, file_type):
    logger.info(f"user_id {user_id} user_first_name is {user_firstname} uploaded file {file_type}")

#_____________________________________________________________________________________#

file_router = Router()
#faylni serverdan yuklash uchun funksiya
async def download_file(file_id):
    file_info = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    return BytesIO(downloaded_file.read()), file_info


#ip plan faylni serverga yuklash handleri

#upload_neid_file yoki upload_ip_file inline query bilan boshlanadigan callback_querylarni ushlash
@file_router.callback_query(lambda callback_query: callback_query.data.startswith('upload_'))
async def fayl_yubor(query: CallbackQuery, state: FSMContext):
    if is_admin(query.from_user.id):
        await query.answer("📎 tegishli faylni serverga yuklang")
        await query.message.answer(f"📎 выгрузите файл {query.data}", reply_markup=ReplyKeyboardRemove())
        #state belgilaymiz
        if query.data == "upload_ip_file":
            await state.set_state(FindId.send_ip_file)
        else:
            await query.message.answer("Fayl zagruzka qilishdan oldin, Hw NCE dan olgan excel fileni o'z "
                                       "kompyuteringizda ochib, keyin uni qaytadan .xlsx formatda saqlab, "
                                       "so'ngra uni serverga yuklang! ")
            await state.set_state(FindId.send_neid_file)

    else:
        await query.answer("🚫У Вас нет прав, Вы не админ!", reply_markup=ReplyKeyboardRemove())
    # Command to handle incoming Excel files

    # 3 martta urinishdan so'ng statedan chiqib ketadigan qilish uchun i ni elon qilamiz
soni = 1
xisob = 0
sheet_names = []
#ip plan faylini yuklash uchun callback handler
@file_router.message(FindId.send_ip_file)
async def handle_ip_document(message: types.Message, state:FSMContext):
    global excel_data, soni, sheet_names  # Declare the global variable
    # sheet_names ni bo'shhatib olamiz xar bir fayl yuklaganda
    sheet_names = []
    try:
        # Download the Excel file
        file_content, info = await download_file(message.document.file_id)

        # Load the Excel file into a Pandas DataFrame
        #barcha sheetlarni o'qish. sheet nomlari dict key bo'lib yoziladi,
        # sheetdagi malumotlari dict value bo'lib yoziladi
        excel_data = pd.read_excel(file_content, sheet_name=None)
        #key are expressed as excel sheets
        for key in excel_data:
            sheet_names.append(key)
        await message.reply(f"\n <b>✅ выгрузился успешно !</b>\nСписок листов на вашом файле {sheet_names}")
        file_uploaded(user_id=message.from_user.id, user_firstname=message.from_user.first_name, file_type='ip_plan')
    except Exception as e:
        await message.reply(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n"
                            f"Попробуйте заново !📎\n"
                            f"{soni}ая попитка. После 3 ого попитки выходите с етого меню.\n"
                            f"наберите /reset чтобы выйти от статуса")
        if soni == 3:
            await state.clear()
            await message.answer(f"С етого меню вышли , уверен ли Вы , что выгружайте правилный файл?")
        else:
            soni += 1
            # Do not finish the state, allowing the user to try again
            return

    #agar tegishli fayl yuklansa statedan chiqib ketamiz
    await state.clear()
#_____________________________________________________________________________________________________________________#
#neid faylini yuklash bo'yicha handler
existing_values_set = set()
@file_router.message(FindId.send_neid_file)
async def handle_neid_document(message: types.Message, state:FSMContext):
    global existing_values_set # Declare the global variable
    # sheet_names ni bo'shhat
    # ib olamiz xar bir fayl yuklaganda

    try:
        # Download the Excel file
        file_content, info = await download_file(message.document.file_id)

        # Load the Excel file into a Pandas DataFrame
        #faqat birinchi sheetni o'qish. 8chi qatorda column qilib,
        # chunki Hw NCE uprovleniyada vigruzka fayl 8chi qatordan boshlanadi

        df_nce = pd.read_excel(file_content, header = 7)
        # Combine values from both columns into a single list
        combined_values = pd.concat([df_nce['Sink NE ID'], df_nce['Source NE ID']])
        # Find the unique values
        unique_values = combined_values.unique()
        unique_values = [value.replace('9-', '') for value in unique_values]
        #before seting new values to variable we should clear set object
        existing_values_set.clear()
        # Set of existing unique values for quick lookup
        existing_values_set = set(unique_values)

        await message.reply(f"\n <b>✅ выгрузился успешно!</b>")
    except Exception as e:
        await message.reply(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>")
        await message.answer("уверен ли Вы , что выгружайте правилный файл?")
        await state.clear()
    #agar tegishli fayl yuklansa statedan chiqib ketamiz
    await state.clear()
#____________________________________________________________________________________________________________________#
#____________________________________________________________________________________________________________________#
#get_neid neid olish uchun
# callback handler
@file_router.callback_query(F.data == "get_neid")
async def neid(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(f"На какому региону хотите выделит новый NE ID",
                               reply_markup=MenuNeID)
#____________________________________________________________________________________________________________________#
#buni get_neid dan keyin qilamiz

@file_router.callback_query(lambda callback_query: callback_query.data.startswith('neid_'))
async def get_neid(query: CallbackQuery):
    try:
        region = query.data[len('neid_'):]  # Extract the region name from the callback data
        await query.answer()
        if is_user(query.from_user.id):
            #solishtiriladigan ne-id str bo'lgani uchun string qilib olyabmiz region ne-id ni xam
            neid_ranges = {
                'tsh': [str(x) for x in range(11001, 15000)],
                'yan': [str(x) for x in range(15001, 17000)],
                'srd': [str(x) for x in range(17001, 19000)],
                'dzh': [str(x) for x in range(19001, 21000)],
                'nav': [str(x) for x in range(21001, 23000)],
                'hrz': [str(x) for x in range(23001, 25000)],
                'kar': [str(x) for x in range(25001, 27000)],
                'bhr': [str(x) for x in range(27001, 29000)],
                'sam': [str(x) for x in range(29001, 33000)],
                'ksh': [str(x) for x in range(33001, 35000)],
                'sha': [str(x) for x in range(35001, 37000)],
                'srh': [str(x) for x in range(37001, 39000)],
                'frg': [str(x) for x in range(39001, 43000)],
                'nam': [str(x) for x in range(43001, 45000)],
                'and': [str(x) for x in range(45001, 47000)],
            }

            if region in neid_ranges:
                all_neid_pool = set(neid_ranges[region])
            else:
                all_neid_pool = set(range(11001, 47000))

            #agar nce fayl yuklanib neid lar olingan bo'ls ular ishtirok etgani ishlatilmaydi
            if existing_values_set:
                free_neid = all_neid_pool - existing_values_set
                list_free_neid = sorted(list(free_neid))
                # Generate a new unique value
                new_unique_value = list_free_neid[0]
                existing_values_set.add(new_unique_value) #add new_unique_value to existing_values_set
            else:
                free_neid = all_neid_pool
                # Generate a new unique value
                list_free_neid = sorted(list(free_neid))
                # Generate a new unique value
                new_unique_value = list_free_neid[0]
                existing_values_set.add(new_unique_value) #add new_unique_value to existing_values_set
            await query.answer()
            await query.message.answer(f"🆕🆔 <code>9-{new_unique_value}</code>",
                                       reply_markup=ReplyKeyboardRemove())
        else:
            await query.answer()
            await query.message.answer("🚫У Вас нет прав, Вы не ползователь!")
    except Exception as e:
        await query.answer()
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")
    # Command to handle incoming Excel files
#_____________________________________________________________________________________________________________________#
#regionlarni tanlaganda sheetlarni alohida knopka qilib chiqazish
@file_router.callback_query(F.data == "region")
async def show_region(query: CallbackQuery, state: FSMContext):
    if is_user(query.from_user.id):
        await query.answer()
        if sheet_names:
            keyboard_builder = InlineKeyboardBuilder()
            for region in sheet_names:
                check = "Новый № объекта"
                # "Новый № объекта" column bo'lmagan sheetlarni buttonga qo'shmaslik
                if check in excel_data[region].columns:
                    #adding regions by sheets
                    button_name =region
                    #keyinchalik filtrda qaysi regionligini ajratib olish uchun 'region_is' qo'shimchasini qo'shyabmiz
                    callback_data = 'region_is_' + region
                    keyboard_builder.add_button(button_name, callback_data)
            #back to main menu
            keyboard_builder.add_button("🔙назад", callback_data='mw')
            site_inlinekeyboard = keyboard_builder.create_keyboard()
            await query.answer()
            await query.message.edit_text("регионы", reply_markup=site_inlinekeyboard)
        else:
            await query.answer()
            await query.message.reply("региони не нашлись, обратитес админам. Возможно ip plan файл не загружен!")
        # #state belgilaymiz
        # await state.set_state(FindId.send_file)
    else:
        await query.answer()
        await query.message.answer("🚫У Вас нет прав, Вы не ползователь!")
    # Command to handle incoming Excel files
#_____________________________________________________________________________________________________________________#

#regionlar tanlanganda uzel agrigatsiyalarni ko'rsatuvchi tugma
@file_router.callback_query(lambda callback_query: callback_query.data.startswith('region_is_'))
async def agg_nodes_in_region(query: CallbackQuery):
    try:
        region = query.data[len('region_is_'):]  # Extract the region name from the callback data
        df = excel_data[region]
        region_nodes = df['Узел агрегации'].drop_duplicates()

        #uzel aggregatsiyalarni inline keyboardga chiqazamiz
        if not region_nodes.empty:
            keyboard_builder = InlineKeyboardBuilder()
            for node in region_nodes:
                result_df = df[df['Узел агрегации'] == node]
                if not result_df.empty:
                    bsnode_name = result_df.iloc[0]["Название объекта"]
                    quantity_used_ip_address = len(result_df["Новый № объекта"].dropna())
                    quantity_all_ip_address = len(result_df["Узел агрегации"].dropna())
                    button_name = str(node)+'   '+bsnode_name+'   '+str(quantity_used_ip_address)+'/'+str(quantity_all_ip_address)
                    bsnode_id = str(node)
                    # keyinchalik filtrda qaysi uzel agrigatsiyaligini ajratib olish uchun 'node_is_' qo'shimchasini qo'shyabmiz
                    callback_data = 'node_is_' + bsnode_id + ':' + region
                    keyboard_builder.add_button(button_name, callback_data)
                    # back to main menu
            keyboard_builder.add_button("🔙назад", callback_data='region')
            nodes_inlinekeyboard = keyboard_builder.create_keyboard()
            await query.answer()
            await query.message.edit_text(f"Узли агрегации, название узли агрегации и количество занятых/всех "
                                          f"адресов на {region}", reply_markup=nodes_inlinekeyboard)
        else:
            await query.answer()
            await query.message.reply("Узли агрегации не нашлись, обратитес админам")
    except Exception as e:
        await query.answer()
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")
#_____________________________________________________________________________________________________________________#

#xar bir uzel agregatsiya xaqida xabar va undagi BS lar ro'yxatini chiqazamiz
@file_router.callback_query(lambda callback_query: callback_query.data.startswith('node_is_'))
async def agg_node(query: CallbackQuery):
    try:
        # Remove the prefix 'Node_is_' from query.data
        no_prefix = query.data[len('node_is_'):]
        # Extract the node and region name from the callback data
        # Split the remaining string at the ':'
        node, region = no_prefix.split(':')
        # Get the desired DataFrame based on the region
        df = excel_data[region]

        # Filter the DataFrame based on the node
        result_df = df[df['Узел агрегации'] == node]
        iterated_values = ''
        i = 0
        mesage = ''
        # Iterate over the non-NaN values in the "Новый № объекта" column
        for obj_num in result_df["Новый № объекта"].dropna():
            # Extract the ip add from the "OMC IP" column
            ip_add = result_df.loc[result_df.loc[:,"Новый № объекта"] == obj_num, "OMC IP"].values[0]
            name = result_df.loc[result_df.loc[:,"Новый № объекта"] == obj_num, "Название объекта"].values[0]
            i += 1
            # Append the object number and VLAN ID to the iterated_values string
            iterated_values += f"{i}. {obj_num} {name} ip: {ip_add} \n\n"

        # Extract the first object number, VLAN ID, and mask

        first_obj = result_df.iloc[0]["Новый № объекта"]
        first_obj_name = result_df.iloc[0]["Название объекта"]
        first_vlan_id = result_df.iloc[0]["OMC 2G/3G/4G/5G VLAN"]
        first_mask = result_df.iloc[0]["OMC mask"]

        # Construct the info_message
        info_message = (f"<b>Узел агрегации:</b> {first_obj}  {first_obj_name}\n<b>vlan:</b>{first_vlan_id}"
                        f"\n<b>маска подсети:</b> {first_mask}\nна етом узле сидят {i} БС\n\n{iterated_values}")
        await query.answer()
        await query.message.reply(info_message)
    except Exception as e:
        await query.answer()
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")
# ___________________________________________________________________________________________________#
#poisk BS berganda ishlaydigan handlerni qilish
@file_router.callback_query(F.data == "search")
async def search_bs(query: CallbackQuery, state: FSMContext):
    try:
        if is_user(query.from_user.id):
            await query.answer()
            await query.message.answer(f"🔎 какой БС ишете...", reply_markup=ReplyKeyboardRemove())
            await state.set_state(FindId.search_comand)
        else:
            await query.answer()
            await query.message.answer("🚫У Вас нет прав, Вы не ползователь!")
    except Exception as e:
        await query.answer()
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")
#qidirilayotgan BS ni ushlab olish handleri
@file_router.message(FindId.search_comand)
async def input_bs(message: Message, state:FSMContext):
    try:
        # user qidiryotgan BS ni ushlab olish
        bs_id = message.text.upper()
        # checking for a column Anywhere in the DataFrame
        column_to_check = 'Новый № объекта'
        check = 0
        # Iterate over each sheet and display the first few rows
        for sheet_name, df in excel_data.items():
            if column_to_check in df.columns:
                # print(f"Column '{column_to_check}' has found in the {sheet_name} dataframe")
                # # Check if bs_id value exists anywhere in the DataFrame

                if df.isin([bs_id]).any().any():
                    check = 1
                    row_index = df.loc[df['Новый № объекта'] == bs_id].index[0]
                    found_df = df.iloc[row_index]
                    node_bs = found_df['Узел агрегации']
                    bs_name = found_df['Название объекта']
                    # Iterate over the columns and display the information
                    bs_info = ""
                    for col in df.columns:
                        bs_info += f"{col}: {found_df[col]}\n"
                    #keyboard yasaymiz
                    bs_keyboard_builder = InlineKeyboardBuilder()
                    change_node_buton = "📝 изменить узел агригации"
                    # keyinchalik filtrda qaysi regionligini ajratib olish uchun 'sheet_name' va 'bs_id' qo'shimchasini qo'shyabmiz
                    change_callback_data = f'bs_change:{sheet_name}:{bs_id}:{bs_name}:{row_index}:{node_bs}'
                    #knopkalarni qo'shamiz
                    bs_keyboard_builder.add_button(change_node_buton, change_callback_data)
                    del_buton = "❌ демонтирован"
                    # keyinchalik filtrda qaysi regionligini ajratib olish uchun 'sheet_name' va 'bs_id' qo'shimchasini qo'shyabmiz
                    del_callback_data = f'bs_del:{sheet_name}:{bs_id}:{bs_name}:{row_index}:{node_bs}'
                    #knopkalarni qo'shamiz
                    bs_keyboard_builder.add_button(del_buton, del_callback_data)
                    # back to main menu
                    bs_keyboard_builder.add_button("🏘назад на меню", callback_data='to_mainmenu')
                    bs_inlinekeyboard = bs_keyboard_builder.create_keyboard()
                    if bs_id == node_bs:
                        await message.answer(f"<b>{bs_id}</b> является узлом агрегации"
                                             f"\n\n{bs_info}", reply_markup=ReplyKeyboardRemove())
                    else:
                        await message.answer(f"Узел агрегация для {bs_id} -- <b>{node_bs}</b> "
                                         f"\n\n{bs_info}", reply_markup=bs_inlinekeyboard)
                else:
                    pass
            else:
                pass
        if not check:
            await message.answer(f"База <b>{bs_id}</b> не нашлось!", reply_markup=ReplyKeyboardRemove())
        # statedan chiqib ketamiz
        await state.clear()
    except Exception as e:
        await message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")
# ___________________________________________________________________________________________________#
#endi BS da "📝 изменить узел агригации" yoki "❌ демонтирован" tanlanganda qilinadigan callback handlerlarni ishlash
@file_router.callback_query(lambda callback_query: callback_query.data.startswith('bs_'))
async def handle_command(query: CallbackQuery):
    choosen_comand = query.data
    command, region, bs_id,bs_name, row_index, old_node = choosen_comand.split(':')
    try:
        if command == "bs_change":
            await query.answer()
            # Retrieve the DataFrame for the specified region
            df = excel_data[region]
            region_nodes = df['Узел агрегации'].drop_duplicates()
            # uzel aggregatsiyalarni inline keyboardga chiqazamiz
            if not region_nodes.empty:
                keyboard_builder = InlineKeyboardBuilder()
                for node in region_nodes:
                    result_df = df[df['Узел агрегации'] == node]
                    if not result_df.empty:
                        bsnode_name = result_df.iloc[0]["Название объекта"]
                        quantity_used_ip_address = len(result_df["Новый № объекта"].dropna())
                        quantity_all_ip_address = len(result_df["Узел агрегации"].dropna())
                        button_name = str(node) + '   ' + bsnode_name + '   ' + str(
                            quantity_used_ip_address) + '/' + str(quantity_all_ip_address)
                        new_node = str(node)
                        # keyinchalik filtrda qaysi uzel agrigatsiyaligini ajratib olish uchun 'to_node' qo'shimchasini qo'shyabmiz
                        callback_data = f'to_node:{region}:{new_node}:{bs_id}:{bs_name}:{row_index}:{old_node}'
                        keyboard_builder.add_button(button_name, callback_data)
                        # back to main menu
                keyboard_builder.add_button("🏘назад на меню", callback_data='to_mainmenu')
                nodes_inlinekeyboard = keyboard_builder.create_keyboard()
                await query.answer()
                await query.message.answer(f"На какой узли агрегации Вы хотите изменить {bs_id}",
                                              reply_markup=nodes_inlinekeyboard)
        #agar demontaj komandasi bosilsa
        elif command == "bs_del":
            await query.answer()

            keyboard_builder = InlineKeyboardBuilder()
            # make buttons for aproving
            button_yes = '🗑Да, удалить'
            button_no = '🧐нет, не удалить'

            # keyinchalik filtrda ma'lumotlarni ajratib olish uchun 'aproved' qo'shimchasini qo'shyabmiz
            callback_data_yes = f'del_ip{region}:{row_index}:{bs_id}'
            callback_data_no = f'mw'
            keyboard_builder.add_button(button_yes, callback_data_yes)
            keyboard_builder.add_button(button_no, callback_data_no)

            del_prove = keyboard_builder.create_keyboard()
            await query.message.answer(f"Действительно хотите удалить <b>{bs_id}</b> из списки! Данние потом не можете востановить\n",
                                 reply_markup=del_prove)

    except Exception as e:
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")
#_______________________________________________________________________________________________#
#endi BS da "📝 изменить узел агригации" yoki "❌ демонтирован" tanlanganda qilinadigan callback handlerlarni ishlash
@file_router.callback_query(lambda callback_query: callback_query.data.startswith('del_ip'))
async def handle_command(query: CallbackQuery):
    try:
        user_id = query.from_user.id
        user_firstname = query.from_user.first_name
        no_prefix = query.data[len('del_ip'):]
        region, row_index,bs_id = no_prefix.split(':')
        # Replace BS_ID with None in the original position
        df = excel_data[region]
        df.at[int(row_index), "Новый № объекта"] = None
        df.at[int(row_index), "Название объекта"] = None
        ip = df.at[int(row_index), "OMC IP"]
        node = df.at[int(row_index), "Узел агрегации"]
        excel_data[region] = df
        #loglarni log faylga yozamiz

        delete_ip_address(bs_id, ip, node, user_id, user_firstname)
        print(f'user {user_id} delete {bs_id} ip address {ip} from {node} node')

        await query.message.answer(f"успешно удалился {bs_id} из таблиции, на узле агрегации {node}"
                               f" освободился OMC IP {ip} ", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")
#______________________________________________________________________________________________#
#Uzel agregatsiya tanlanganda , BS ni o'zi turgan uzel agregatsiyadan o'chirin, tanlangan uzel agregatsiyaga ko'chirish
@file_router.callback_query(lambda callback_query: callback_query.data.startswith('to_node'))
async def change_node(query: CallbackQuery):
    try:
        user_id = query.from_user.id
        user_firstname = query.from_user.first_name
        # Remove the prefix 'to_node' from query.data
        no_prefix = query.data[len('to_node:'):]
        # Extract the region, new_node, bs_id, row_index from the callback data
        # Split the remaining string at the ':'
        region, new_node, bs_id, bs_name, row_index, old_node = no_prefix.split(':')
        # Get the desired DataFrame based on the region
        df = excel_data[region]
        # # Find the index of the row containing the current bs_id
        index_row = df[df['Новый № объекта'] == bs_id].index[0]


        # Find the first row where 'Узел агрегации' matches new_node and 'Новый № объекта' is None
        none_rows = df[(df['Узел агрегации'] == new_node) & (df['Новый № объекта'].isna())].index
        if none_rows.any():
            # Replace the current bs_id to new node
            df.loc[none_rows[0], 'Новый № объекта'] = bs_id
            df.loc[none_rows[0], 'Название объекта'] = bs_name
            new_ip = df.loc[none_rows[0], 'OMC IP']

            # Replace the current bs_id with None in the original position
            #index_row olyabman, chunki row_index str format bo'lgani uchun, aslida
            #index_row va row_index bir xil qiymatda str yoki int ligini xisobga olmasak
            old_ip = df.at[index_row, "OMC IP"]
            df.at[index_row, "Новый № объекта"] = None
            df.at[index_row, "Название объекта"] = None
            #log faylga yozamiz
            change_base_station_ip(bs_id, old_ip, new_ip, old_node, new_node, user_id, user_firstname)
        else:
            await query.message.answer(
                    "Извините, в данной узле агрегации нет свободных мест для нового бс.",
                    reply_markup=ReplyKeyboardRemove()
                )
            return
        # Update the excel_data dictionary with the modified DataFrame
        excel_data[region] = df

        await query.answer()
        await query.message.answer(f"{bs_id} изменил узел агрегации с {old_node} на {new_node} ",
                reply_markup=ReplyKeyboardRemove()
                                   )
    except Exception as e:
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")

#______________________________________________________________________________________________#

#yangi ip adres olish uchun handler
#get_newip
@file_router.callback_query(F.data == "get_newip")
async def get_newip(query: CallbackQuery, state: FSMContext):
    try:
        if is_user(query.from_user.id):
            await query.answer()
            await query.message.answer(f"вводите БС id и его имя в формате REGXXXXX.\n"
                                       f"id БС должен бить без пробелов. Например YAN3820", reply_markup=ReplyKeyboardRemove())
            await state.set_state(FindId.input_bs_id)
        else:
            await query.answer()
            await query.message.answer("🚫У Вас нет прав, Вы не ползователь!")
    except Exception as e:
        await query.answer()
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")

#qidirilayotgan BS ni ushlab olish handleri
@file_router.message(FindId.input_bs_id)
async def input_bs_id(message: Message, state:FSMContext):
    try:
        # user kirgizayotgan BS va uning nomini ushlab olish
        bs_id = message.text.upper()
        region = message.text[0:3].upper()
        await state.update_data(bs_id=bs_id, region=region)
        await message.answer(f"База <b>{bs_id}</b> регион <b>{region}</b>! \n"
                             f"Введите название БС.", reply_markup=ReplyKeyboardRemove())
        # yangi statega o'tamiz
        await state.set_state(FindId.input_bs_name)
    except Exception as e:
        await message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")

@file_router.message(FindId.input_bs_name)
async def input_bs_name(message: Message, state:FSMContext):
    try:
        # user kirgizayotgan BS va uning nomini ushlab olish
        bs_name = message.text.capitalize()
        # Retrieve the stored values from the state
        data = await state.get_data()
        bs_id = data.get('bs_id')
        region = data.get('region')
        await state.update_data(bs_id=bs_id, bs_name= bs_name, region=region)
        keyboard_builder = InlineKeyboardBuilder()
        #make buttons for aproving
        button_yes ='✅Да'
        button_no = '✏️изменить данние'

        #keyinchalik filtrda ma'lumotlarni ajratib olish uchun 'aproved' qo'shimchasini qo'shyabmiz
        callback_data_yes = f'aproved{region}:{bs_id}:{bs_name}'
        callback_data_no = 'get_newip'
        keyboard_builder.add_button(button_yes, callback_data_yes)
        keyboard_builder.add_button(button_no, callback_data_no)
        #back to main menu
        keyboard_builder.add_button("🔙назад", callback_data='mw')
        approved_bs = keyboard_builder.create_keyboard()


        await message.answer(f"База <b>{bs_id}-{bs_name}</b> регион <b>{region}</b>! \n",
                             reply_markup=approved_bs)
        # yangi statega o'tamiz
        await state.clear()
    except Exception as e:
        await message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")

#______________________________________________________________________________________________#

#yangi kiritilayotgan BS uchun ip ajratish handleri
@file_router.callback_query(lambda callback_query: callback_query.data.startswith('aproved'))
async def new_bs(query: CallbackQuery):
    try:
        # Remove the prefix 'aproved' from query.data
        no_prefix = query.data[len('aproved'):]
        # Extract the region, bs_id, bs_name from the callback data
        # Split the remaining string at the ':'
        region, bs_id, bs_name = no_prefix.split(':')
        # Get the desired DataFrame based on the region
        df = excel_data[region]
        #kirgizilgan bs bizning dataframeda bor yoki yo'qligini tekshirib olamiz avval
        if df.isin([bs_id]).any().any():
            await query.message.answer(f"На БС '{bs_id}' уже есть ip адреса на {region} регионе!")
        #agar kirgazilgan bs_id bizni df da bo'lmasa unga shu regiondan qaysi uzel agregatsiyaga qo'yilishini so'raymiz
        else:

            region_nodes = df['Узел агрегации'].drop_duplicates()

            # uzel aggregatsiyalarni inline keyboardga chiqazamiz
            if not region_nodes.empty:
                keyboard_builder = InlineKeyboardBuilder()
                for node in region_nodes:
                    result_df = df[df['Узел агрегации'] == node]
                    if not result_df.empty:
                        bsnode_name = result_df.iloc[0]["Название объекта"]
                        quantity_used_ip_address = len(result_df["Новый № объекта"].dropna())
                        quantity_all_ip_address = len(result_df["Узел агрегации"].dropna())
                        button_name = str(node) + '   ' + bsnode_name + '   ' + str(
                            quantity_used_ip_address) + '/' + str(quantity_all_ip_address)
                        bsnode_id = str(node)
                        # keyinchalik filtrda qaysi uzel agrigatsiyaligini ajratib olish uchun 'set_node_tonewbs' qo'shimchasini qo'shyabmiz
                        callback_data = f'set_node_tonewbs{region}:{bsnode_id}:{bs_id}:{bs_name}'
                        keyboard_builder.add_button(button_name, callback_data)
                        # back to main menu
                keyboard_builder.add_button("🔙назад", callback_data='mw')
                nodes_inlinekeyboard = keyboard_builder.create_keyboard()

            await query.answer()
            await query.message.answer(
                    f"Из какого узли агрегеции Вы хотите дать ip адрес на <b>{bs_id}-{bs_name}</b>",
                    reply_markup=nodes_inlinekeyboard
                )
            return

    except Exception as e:
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")

#_________________________________________________________________________________________________________________#
#Uzel agregatsiya tanlanganda , yangi BS ga tanlangan uzel agregatsiyadan ip olib berish
@file_router.callback_query(lambda callback_query: callback_query.data.startswith('set_node_tonewbs'))
async def change_node(query: CallbackQuery):
    try:
        user_id = query.from_user.id
        user_firstname = query.from_user.first_name

        # Remove the prefix 'to_node' from query.data
        no_prefix = query.data[len('set_node_tonewbs'):]
        # Extract the region, new_node, bs_id, row_index from the callback data
        # Split the remaining string at the ':'

        region, bsnode_id, bs_id, bs_name = no_prefix.split(':')
        # Get the desired DataFrame based on the region
        df = excel_data[region]
        # # Find the index of the row containing the current bs_id

        # Find the first row where 'Узел агрегации' matches new_node and 'Новый № объекта' is None
        none_rows = df[(df['Узел агрегации'] == bsnode_id) & (df['Новый № объекта'].isna())].index
        if none_rows.any():
            # Replace the current bs_id to new node
            df.loc[none_rows[0], 'Новый № объекта'] = bs_id
            df.loc[none_rows[0], 'Название объекта'] = bs_name
            ip_address = df.loc[none_rows[0], 'OMC IP']

            # Get the IP pool information
            bs_info = ''
            for col in df.columns:
                bs_info += f"{col}: {df.loc[none_rows[0], col]}\n"

            await query.answer()
            await query.message.answer(
                f"На <b>{bs_id}-{bs_name}</b> дали новые IP-адресa из узла агрегации <b>{bsnode_id}</b>\n{bs_info}",
                reply_markup=ReplyKeyboardRemove())
            #log faylga yozamiz
            give_new_ip_to_base_station(ip_address, bs_id, bsnode_id, user_id, user_firstname)


        else:
            await query.message.answer(
                    "Извините, в данной узле агрегации нет свободных мест для нового бс.",
                    reply_markup=ReplyKeyboardRemove()
                )
            return
        # Update the excel_data dictionary with the modified DataFrame
        excel_data[region] = df

    except Exception as e:
        await query.message.answer(f"❌❓Возникло ошибка ! : <b>{str(e)}</b>\n")
#____
#
#
# __________________________________________________________________________________________________________#