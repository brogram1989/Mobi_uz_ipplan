from aiogram.fsm.state import StatesGroup, State

class AdminCommands(StatesGroup):
    user_id = State()
    del_user = State()
    set_admin =State()
    del_admin = State()

class FindId(StatesGroup):
    send_ip_file = State() #ip faylni serverga yuborish stati
    send_neid_file = State() #Hw nce filini serverga yuborish stati
    get_updated_ip_file = State() #faylni serverdan qabul qilib olish stati
    search_comand = State() #qidirishni bosganda ishga tushadigan state
    input_bs_id = State() #yangi BS uchun ip adres olayotganda, bs idsi kiritilganda ishga tushadigan state
    input_bs_name = State() #yangi BS uchun ip adres olayotganda, bs nomini kiritilganda ishga tushadigan state
    send_msg = State() #userlarga message yuborish stati


