from aiogram.fsm.state import StatesGroup, State

class AdminCommands(StatesGroup):
    user_id = State()
    del_user = State()
    set_admin =State()
    del_admin = State()

class FindId(StatesGroup):
    send_ip_file = State() #ip faylni serverga yuborish xolati
    send_neid_file = State() #Hw nce filini serverga yuborish xolati
    get_updated_ip_file = State() #faylni serverdan qabul qilib olish xolati
    search_comand = State() #qidirishni bosganda ishga tushadigan xolat
    input_bs_id = State() #yangi BS uchun ip adres olayotganda, bs idsi kiritilganda ishga tushadigan xolat
    input_bs_name = State() #yangi BS uchun ip adres olayotganda, bs nomini kiritilganda ishga tushadigan xolat
    send_msg = State() #userlarga message yuborish xolati
    check_ip = State() #ip faylini tekshirish xolati


