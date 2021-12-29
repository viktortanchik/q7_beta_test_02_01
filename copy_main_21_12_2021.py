import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
#from aiogram.types import InputFile
import csv
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
#5049839636:AAGU4R4Ibn-qwonYWMBfFWHfU0xM6LubqFA
import sqlite3
from db import *
import asyncio
from create_chat_02 import create_chat
#from create_chat.create_01 import create_chat
#from create_chat import create_01
#2141799369:AAEhbbxAsNFkfeLs6kU4WYuz4i0O5iCzIyE
bot = Bot(token="2141799369:AAEhbbxAsNFkfeLs6kU4WYuz4i0O5iCzIyE")

#bot = Bot(token="5049839636:AAGU4R4Ibn-qwonYWMBfFWHfU0xM6LubqFA")
dp = Dispatcher(bot)
con = sqlite3.connect('bot.sqlite')
import re

#row = rows.clear()
rows = (get_all(con))

def admins(user):
    admins = get_admins(con)
    flag=False
    for i in range(len(admins)):
        #print(admins[i][1])
        if int(admins[i][1])==int(user):
            flag=True
    return flag

def super_admin(user):
    super_admins = get_super_admin(con)
    flag=False
    for i in range(len(super_admins)):
        #print(admins[i][1])
        if int(super_admins[i][1])==int(user):
            flag=True
    return flag
#admins("123")

async def find_all():
    rows = (get_all(con))
    return rows

def all_users():
    rows = (get_all(con))
    #print("all_users>>",rows)
    newrow = []
    #mes = ''
    for row in range(len(rows)):

        newrow.append( '/'+rows[row][2])
    #print("newrow >>> ",newrow)
    return newrow

# def test_join_admin():
#     admin = get_admins(con)
#     print("admin>>>",admin)
#     for i in admin:
#         print(i[1])
#
# test_join_admin()



@dp.message_handler(content_types=["new_chat_members"])
async def on_user_joined(message: types.Message):
    #await message.delete()
    admin = get_admins(con)
    adm=[]
    for i in admin:
        adm.append(i[1])
        print(i[1])
    flag_admin=True
    #print("admin>>>",adm[1])
    #print('message>>>>>>>>>>>>>>>>>>',message['from'].id)
    for i in range(len(adm)):
        print('>>>>>>>>>>',adm[i])
        if int(adm[i]) == int(message['from'].id):
            print("ADMIN JOIN CHAT")
            flag_admin=False

    if flag_admin==True:
        data =['real_name',str(message['from'].username),'user_id',str(message.chat.title),'name_of_agency','payid','strikes','hyperlink','tag','notes','0',"cash_out"]
        sql_insert_all(con,data)
        await bot.send_message(674868256, "Hey!\n added new user\n Chat "+message.chat.title+'\n username '+message['from'].username)
    #rowsget_all(con)
    #await message.reply("Привет!\n добавлен новый пользователь ")

@dp.message_handler(commands='start')
async def process_start_command(message: types.Message):
    flag = admins(message['from'].id)
    if flag!=True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
        print(message)
        print(message['from'].username)
    else:
        #await message.delete()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu"]
        keyboard.add(*buttons)
        #await message.answer(".", reply_markup=keyboard)
        await message.delete()
        time.sleep(3)
        await bot.send_message(message.chat.id,'at your serviсe', reply_markup=keyboard)

        #await message.delete()

    chat = await bot.get_chat_member(message.chat.id, message['from'].id)
    print(chat)
    #await message.delete()

        #await message.delete()


newrows=[]
genelamain =["Main menu"]
@dp.message_handler(Text(equals=genelamain))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Find","USER CARD","Settings ⚙"]
        keyboard.add(*buttons)
        await message.answer("at your serviсe", reply_markup=keyboard)
        #await message.delete()


equal=['Settings ⚙']
@dp.message_handler(Text(equals=equal))
async def settings(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu", "ALL ADMIN ⚙", "Add admin 🔧","Add super admin 🛠","Del user 🛠","Del admin 🛠","send_file","Create_chat"]
        keyboard.add(*buttons)
        await message.answer("at your serviсe", reply_markup=keyboard)


equal=['Create_chat']
@dp.message_handler(Text(equals=equal))
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        temp = [str(UPDATE)]
        adms=get_admins(con)
        len_admins=[]
        for i in adms:
            len_admins.append(int(i[1]))
        await create_chat(temp,len_admins,4)
        #create_chat(str(temp),)



equal=['send_file']
@dp.message_handler(Text(equals=equal))
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        #await message.delete()
        #bot.send_document(message.chat.id, ('filename.txt', 'test.txt'))

        myData = ('real_name', 'username', 'user_id', 'chat', 'agency', 'payid', 'strikes', 'hyperlink', 'tag', 'notes',
                  'wallet', 'cash_out')
        temp_db = get_all(con)

        myFile = open('db.csv', 'w')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerow(myData)
            for i in temp_db:
                print(i[1:])
                writer.writerow(i[1:])
        #myFile.close()

        #bot.send_document(chat_id, ('filename.txt', file))
        #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        await message.reply_document(open("db.csv", "rb"))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu"]
        keyboard.add(*buttons)
        await message.answer("at your serviсe", reply_markup=keyboard)


equal=['Add admin 🔧']
@dp.message_handler(Text(equals=equal))
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu", "Save admin 🔧"]
        keyboard.add(*buttons)
        await message.answer("at your serviсe", reply_markup=keyboard)

equal=['Save admin 🔧']
@dp.message_handler(Text(equals=equal))
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()

        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        temp=[str(UPDATE)]
        print("SAVE_ADMIN>>>",temp)
        sql_insert_admins(con,temp)
        await message.answer("SAVE_ADMIN")

equal=['ALL USER']
@dp.message_handler(Text(equals=equal))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu"]
        keyboard.add(*buttons)
        rows= get_all(con)
        print('rows>>',rows)
        mes=''
        for row in range (len(rows)):
            mes += ' /'
            print(rows[row])
            mes+=str(rows[row][2])
            newrows.append(rows[row][2])
            print('newrows >> ', newrows)
            #mes+=' /'cxvbcvxxb
        dp.message_handler(commands=[newrows[row] for row in range(len(newrows))])
        await message.answer(mes, reply_markup=keyboard)

@dp.message_handler(Text(equals="Find"))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['real_name 🔎','username 🔎','user_id 🔎','chat 🔎', 'name_of_agency 🔎', 'payid 🔎', 'strikes 🔎', 'hyperlink 🔎',
                        'tag 🔎', 'notes 🔎', 'wallet 🔎','cash_out 🔎',"Main menu"]
        keyboard.add(*buttons)
        await message.answer("Find ", reply_markup=keyboard)

@dp.message_handler(Text(equals="chat 🔎"))
async def find_chat(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>",chat_find[i][4])
            finds = str(chat_find[i][4])
            print("FINDS>>>>> ",finds.find(UPDATE))
            if finds.find(UPDATE)>=0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][4], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("FIND chat 🔎 " + mes)

@dp.message_handler(Text(equals="user_id 🔎"))
async def find_user_id(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][3])
            finds = str(chat_find[i][3])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][3], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("FIND ser_id 🔎 " + mes)

@dp.message_handler(Text(equals="username 🔎"))
async def find_username(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][2])
            finds = str(chat_find[i][2])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][2], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("username 🔎 " + mes)

@dp.message_handler(Text(equals="real_name 🔎"))
async def find_real_name(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][1])
            finds = str(chat_find[i][1])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][1], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("real_name 🔎 " + mes)

@dp.message_handler(Text(equals="name_of_agency 🔎"))
async def find_name_of_agency(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][5])
            finds = str(chat_find[i][5])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][5], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("name_of_agency 🔎 " + mes)

@dp.message_handler(Text(equals="payid 🔎"))
async def find_payid(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][6])
            finds = str(chat_find[i][6])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][6], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("payid 🔎 " + mes)

@dp.message_handler(Text(equals="strikes 🔎"))
async def find_strikes(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][7])
            finds = str(chat_find[i][7])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][7], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("strikes 🔎 " + mes)

@dp.message_handler(Text(equals="hyperlink 🔎"))
async def find_hyperlink(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][8])
            finds = str(chat_find[i][8])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][8], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("hyperlink 🔎 " + mes)

@dp.message_handler(Text(equals="tag 🔎"))
async def find_tag(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][9])
            finds = str(chat_find[i][9])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][9], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
            await message.delete()

        else:
            await message.answer("tag 🔎 " + mes)
            await message.delete()


@dp.message_handler(Text(equals="notes 🔎"))
async def find_notes(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][10])
            finds = str(chat_find[i][10])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][10], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("notes 🔎 " + mes)

@dp.message_handler(Text(equals="wallet 🔎"))
async def find_deposit(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][11])
            finds = str(chat_find[i][11])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][11], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("deposit 🔎 " + mes)


@dp.message_handler(Text(equals="cash_out 🔎"))
async def find_deposit(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        print('chat_find',chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        print("UPDATE>>",UPDATE)
        temps.close()
        mes = ''
        find=0
        for i in range(len(chat_find)):
            print("chat_find>>>>>", chat_find[i][12])
            finds = str(chat_find[i][12])
            print("FINDS>>>>> ", finds.find(UPDATE))
            if finds.find(UPDATE) >= 0:
                find+=1
                mes += ' /'
                mes += str(chat_find[i][2])
                print("FIND AND >>", chat_find[i][12], '  ', mes)
        if find==0:
            await message.answer("Search did not return any result ❌")
        else:
            await message.answer("cash_out 🔎 " + mes)

genelamain =["USER CARD"]
@dp.message_handler(Text(equals=genelamain))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        #print()
        getchat = await bot.get_chat(message.chat.id)
        print(getchat.title)
        card = sql_select_chat(con, getchat.title)
        s1 = re.sub("[/]", "", card[2])
        if float(card[11]) >= 0:
            deposit = 'balance   '
        else:
            deposit = 'credit'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=False)
        # Change info
        buttons = ["Main menu","CARD",'Change_info']


        butt= "User card " + s1 + '\n' + 'real_name ' + card[1] + '\n' + 'username ' + card[2] + '\n' + 'user_id ' + card[3] + '\n' + 'chat ' + card[4] + '\n' + 'agency ' +card[5] + '\n' + 'payid ' + card[6] + '\n' + 'strikes ' + card[
                                 7] + '\n' + 'hyperlink ' + card[8] + '\n' + 'tag ' + card[
                                 9] + '\n' + 'notes ' + card[10] + '\n' + deposit + str(
            card[11]) + '\n' + 'cash_out     ' + card[12]
        keyboard.add(*buttons)
        #
        await message.answer("User card", reply_markup=keyboard)  # test_pots_pip  -1001600149738   # test_chat -1001392919876
        #await message.answer("ready for work", reply_markup=keyboard)

genelamain =["Change_info"]
@dp.message_handler(Text(equals=genelamain))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        getchat = await bot.get_chat(message.chat.id)
        print(getchat.title)
        card = sql_select_chat(con, getchat.title)
        s1 = re.sub("[/]", "", card[2])
        if float(card[11]) >= 0:
            deposit = 'balance   '
        else:
            deposit = 'credit'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=False)
        # Change info
        buttons = ["Main menu", "CARD", 'real_name', 'username', 'user_id', 'chat_', 'agency_', 'payid_', 'strikes_',
                   'hyperlink_',
                   'tag_', 'notes_', 'wallet_', 'cash_out_']

        butt = "User card " + s1 + '\n' + 'real_name ' + card[1] + '\n' + 'username ' + card[2] + '\n' + 'user_id ' + \
               card[3] + '\n' + 'chat ' + card[4] + '\n' + 'agency ' + card[5] + '\n' + 'payid ' + card[
                   6] + '\n' + 'strikes ' + card[
                   7] + '\n' + 'hyperlink ' + card[8] + '\n' + 'tag ' + card[
                   9] + '\n' + 'notes ' + card[10] + '\n' + deposit + str(
            card[11]) + '\n' + 'cash_out     ' + card[12]
        keyboard.add(*buttons)
        #
        await message.answer("User card",reply_markup=keyboard)  # test_pots_pip  -1001600149738   # test_chat -1001392919876


@dp.message_handler(commands='wallet')
async def process_start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Click me", callback_data="wallet"))
    await message.answer("let's see your balance", reply_markup=keyboard)

@dp.callback_query_handler(text="wallet")
async def send_random_value(call: types.CallbackQuery):
    getchat = await bot.get_chat(call.message.chat.id)
    print(getchat.title)
    card = sql_select_chat(con, getchat.title)
    s1 = re.sub("[/]", "", card[2])
    if float(card[11]) >= 0:
        deposit = '🟢 balance   '
    else:
        deposit = '🔴 credit   '
    butt =  deposit + str(card[11])
    # print("call>>",call.message.chat.id)
    print(len(butt))
    await call.answer(text=butt, show_alert=True)
    await call.message.delete()


@dp.message_handler(Text(equals="CARD"))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Click me", callback_data="CARD"))
        await message.answer("let's see your balance", reply_markup=keyboard)

@dp.callback_query_handler(text="CARD")
async def send_random_value(call: types.CallbackQuery):
    flag = admins(call['from'].id)
    if flag != True:
        # await message.delete()
        await call.answer("this chat is not allowed to work with the bot ")
    else:
        getchat = await bot.get_chat(call.message.chat.id)
        print(getchat.title)
        card = sql_select_chat(con, getchat.title)
        s1 = re.sub("[/]", "", card[2])
        if float(card[11]) >= 0:
            deposit = 'balance   '
        else:
            deposit = 'credit'
        butt ='username ' + card[2] +  '\n' + 'chat ' + card[4] + '\n' + 'agency ' + card[5] + '\n' + 'payid ' + card[6] + '\n' + 'strikes ' + card[7] + '\n' + 'google.com ' + card[8] + '\n' + 'tag ' + card[9] + '\n' + 'notes ' + card[10] + '\n' + deposit + str(card[11]) + '\n' + 'cash_out     ' + card[12]
        #print("call>>",call.message.chat.id)
        print(len(butt))
        await call.answer(text=butt, show_alert=True)
        await call.message.delete()
    # или просто await call.answer()

@dp.message_handler(Text(equals="real_name"))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'real_name'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change real_name' )
        #await message.answer("ready for work", reply_markup=keyboard)

@dp.message_handler(Text(equals="username"))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'username'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change real_name')


@dp.message_handler(Text(equals='user_id'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'user_id'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change user_id')


@dp.message_handler(Text(equals='chat_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'chat'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change chat')


@dp.message_handler(Text(equals='agency_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'name_of_agency'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change agency')

@dp.message_handler(Text(equals='payid_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'payid'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change payid')

@dp.message_handler(Text(equals='strikes_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'strikes'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change strikes')

@dp.message_handler(Text(equals='hyperlink_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'hyperlink'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change hyperlink')

@dp.message_handler(Text(equals='tag_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'tag'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change tag')
@dp.message_handler(Text(equals='notes_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'notes'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change notes')

@dp.message_handler(Text(equals='cash_out_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'cash_out'
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change cash_out')

@dp.message_handler(Text(equals='wallet_'))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        users = open(str(message['from'].id) + "user.txt", "r")
        user = users.read()
        users.close()
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        users.close()
        set = 'wallet'
        balans = sql_select_id(con, user)

        UPDATE = float(balans[11]) + float(UPDATE)

        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        #await message.answer("You are in the user card " + '/' + user + ' and trying to change wallet')





@dp.message_handler()
async def process_start_command(message: types.Message):
    print("message>>>>", message)
    getchat = await bot.get_chat(message.chat.id)
    print(getchat.title)

    #chat = await bot.get_chat_member(message.chat.id,message['from'].id)
    #print(chat)
    # for i in chat:
    #     print(i)
    # admi = await bot.get_chat_administrators(-654979481)
    # for i in admi:
    #     print(i)
    #
    flag = admins(message['from'].id)
    if flag != True:
       pass
    else:
        #await message.delete()
        file = open(str(message['from'].id) + "temp.txt", "w")
        file.write(str(message.text))
        file.close()
        #member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        #print(bot.send_message(1300980828,"test"))
#1300980828
        # users = all_users()
        # if message.text in users:
        ##################
        # card = sql_select_chat(con, getchat.title)
        #
        # if getchat.title in card[4]:
        #     print(getchat.title)
        #     s1 = re.sub("[/]", "", card[2])
        #     #print(message['from'].id)
        #     #print('s1 >> ',s1)
        #     file = open(str(message['from'].id)+"user.txt", "w")
        #     file.write(s1)
        #     file.close()
        #     #card = sql_select_id(con,s1)
        #     #card = sql_select_chat(con,getchat.title)
        #     print(card)
        #     buttons =[]
        #     if float(card[11])>=0:
        #         deposit = 'balance   '
        #     else:
        #         deposit = 'credit   '
    #await message.delete()
            #await message.answer("User card     "+s1+'\n'+'real_name    '+card[1]+ '\n'+'username    '+card[2]+'\n'+'user_id        '+card[3]+'\n'+'chat             '+card[4]+'\n'+'agency        '+card[5]+ '\n'+'payid        '+card[6]+'\n'+'strikes       '+card[7]+'\n'+'hyperlink   '+card[8]+'\n'+'tag       '+card[9]+'\n'+ 'notes    '+card[10]+'\n'+deposit +str(card[11])+'\n'+'cash_out     '+card[12]) # test_pots_pip  -1001600149738   # test_chat -1001392919876

if __name__ == '__main__':
    executor.start_polling(dp)