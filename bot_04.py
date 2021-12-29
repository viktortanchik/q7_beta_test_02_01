from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
#5049839636:AAGU4R4Ibn-qwonYWMBfFWHfU0xM6LubqFA
import sqlite3
from db import *
import asyncio
#2141799369:AAEhbbxAsNFkfeLs6kU4WYuz4i0O5iCzIyE
#bot = Bot(token="2141799369:AAEhbbxAsNFkfeLs6kU4WYuz4i0O5iCzIyE")

bot = Bot(token="5049839636:AAGU4R4Ibn-qwonYWMBfFWHfU0xM6LubqFA")
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
    print("all_users>>",rows)
    newrow = []
    #mes = ''
    for row in range(len(rows)):

        newrow.append( '/'+rows[row][2])
    print("newrow >>> ",newrow)
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
    print("admin>>>",adm[1])
    print('message>>>>>>>>>>>>>>>>>>',message['from'].id)
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
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu"]
        keyboard.add(*buttons)
        await message.answer("ready for work", reply_markup=keyboard)

newrows=[]
genelamain =["Main menu"]
@dp.message_handler(Text(equals=genelamain))
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Find","USER CARD","Settings ⚙"]
        keyboard.add(*buttons)
        await message.answer("ready for work", reply_markup=keyboard)

equal=['Settings ⚙']
@dp.message_handler(Text(equals=equal))
async def settings(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu", "ALL ADMIN ⚙", "Add admin 🔧","Add super admin 🛠","Del user 🛠","Del admin 🛠"]
        keyboard.add(*buttons)
        await message.answer("ready for work", reply_markup=keyboard)


equal=['Add admin 🔧']
@dp.message_handler(Text(equals=equal))
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu", "Save admin 🔧"]
        keyboard.add(*buttons)
        await message.answer("ready for work", reply_markup=keyboard)

equal=['Save admin 🔧']
@dp.message_handler(Text(equals=equal))
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
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
        else:
            await message.answer("tag 🔎 " + mes)

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
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Main menu",'real_name', 'username', 'user_id', 'chat_', 'agency_', 'payid_', 'strikes_', 'hyperlink_',
                        'tag_', 'notes_', 'wallet_', 'cash_out_']

        keyboard.add(*buttons)
        await message.answer("ready for work", reply_markup=keyboard)


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
        set_name = (str(UPDATE))
        where = ('username')
        where_name = (str(user))
        sql_update(con, set, set_name, where, where_name)
        await message.answer("You are in the user card " + '/' + user + ' and trying to change wallet')



@dp.message_handler()
async def process_start_command(message: types.Message):
    print("message>>>>",message)
    flag = admins(message['from'].id)
    if flag != True:
       pass
    else:
        #await message.delete()

        file = open(str(message['from'].id) + "temp.txt", "w")
        file.write(str(message.text))
        file.close()
        #print("message. >> ",message.text)
        users = all_users()
        #print("SUMA >>> ",(60+int(message.text)))
        print("users>>>",users)
        if message.text in users:
            print("message.text >> ",message.text)

            s1 = re.sub("[/]", "", message.text)
            #print(message['from'].id)
            #print('s1 >> ',s1)
            file = open(str(message['from'].id)+"user.txt", "w")
            file.write(s1)
            file.close()
            card = sql_select_id(con,s1)
            buttons =[]
            if float(card[11])>=0:
                deposit = 'balance   '
            else:
                deposit = 'credit   '
            #
            #
            # name_buttons=['real_name','username','user_id','chat','name_of_agency','payid','strikes','hyperlink','tag','notes','wallet','cash_out']
            # print('card>>>>>',card[12])
            # lennames=0
            # for i in card[1:]:
            #     #print(i)
            #     buttons.append(types.InlineKeyboardButton(text=name_buttons[lennames], callback_data=name_buttons[lennames]))
            #     lennames+=1
            # keyboard = types.InlineKeyboardMarkup(row_width=3)
            # keyboard.add(*buttons)


            await message.answer("User card     "+s1+'\n'+'real_name    '+card[1]+ '\n'+'username    '+card[2]+'\n'+'user_id        '+card[3]+'\n'+'chat             '+card[4]+'\n'+'agency        '+card[5]+ '\n'+'payid        '+card[6]+'\n'+'strikes       '+card[7]+'\n'+'hyperlink   '+card[8]+'\n'+'tag       '+card[9]+'\n'+ 'notes    '+card[10]+'\n'+deposit +str(card[11])+'\n'+'cash_out     '+card[12]) # test_pots_pip  -1001600149738   # test_chat -1001392919876
#
# name_buttons = [ 'real_name','username','user_id', 'chat','name_of_agency', 'payid',  'hyperlink',
#                 'notes', 'wallet','cash_out']
#
# @dp.callback_query_handler(text='strikes')
# async def send_random_value(call: types.CallbackQuery):
#     print(call)
#     keyboard = types.InlineKeyboardMarkup(row_width=3)
#     tag_1 =types.InlineKeyboardButton(text='test_strikes_1', callback_data='test_strikes_1')
#     tag_2 =types.InlineKeyboardButton(text='test_strikes_2', callback_data='test_strikes_2')
#     tag_3 =types.InlineKeyboardButton(text='test_strikes_3', callback_data='test_strikes_3')
#     keyboard.add(tag_1,tag_2,tag_3)
#     await call.message.answer('change strikes!',reply_markup=keyboard)
#
# @dp.callback_query_handler(text='test_strikes_1')
# async def send_random_value(call: types.CallbackQuery):
#     users = open(str(call['from'].id) + "user.txt", "r")
#     user = users.read()
#     users.close()
#     #print(call.data)
#     set = 'strikes'
#     set_name = 'test_strikes_1'
#     where = ('username')
#     where_name = (str(user))
#     sql_update(con, set, set_name, where, where_name)
#     await call.message.answer("You are in the user card " + '/' + user + ' and trying to change ' + call.data)
#
#
# @dp.callback_query_handler(text='test_strikes_2')
# async def send_random_value(call: types.CallbackQuery):
#     users = open(str(call['from'].id) + "user.txt", "r")
#     user = users.read()
#     users.close()
#     #print(call.data)
#     set = 'strikes'
#     set_name = 'test_strikes_2'
#     where = ('username')
#     where_name = (str(user))
#     sql_update(con, set, set_name, where, where_name)
#     await call.message.answer("You are in the user card " + '/' + user + ' and trying to change ' + call.data)
#
# @dp.callback_query_handler(text='test_strikes_3')
# async def send_random_value(call: types.CallbackQuery):
#     users = open(str(call['from'].id) + "user.txt", "r")
#     user = users.read()
#     users.close()
#     #print(call.data)
#     set = 'strikes'
#     set_name = 'test_strikes_3'
#     where = ('username')
#     where_name = (str(user))
#     sql_update(con, set, set_name, where, where_name)
#     await call.message.answer("You are in the user card " + '/' + user + ' and trying to change ' + call.data)
#
#
#     #############
# @dp.callback_query_handler(text='tag')
# async def send_random_value(call: types.CallbackQuery):
#     print(call)
#     keyboard = types.InlineKeyboardMarkup(row_width=3)
#     tag_1 =types.InlineKeyboardButton(text='test_tag_1', callback_data='test_tag_1')
#     tag_2 =types.InlineKeyboardButton(text='test_tag_2', callback_data='test_tag_2')
#     tag_3 =types.InlineKeyboardButton(text='test_tag_3', callback_data='test_tag_3')
#     keyboard.add(tag_1,tag_2,tag_3)
#     await call.message.answer('change TAG',reply_markup=keyboard)
#
# @dp.callback_query_handler(text='test_tag_1')
# async def send_random_value(call: types.CallbackQuery):
#     users = open(str(call['from'].id) + "user.txt", "r")
#     user = users.read()
#     users.close()
#
#     print(call.data)
#     # temps = open(str(call['from'].id) + "temp.txt", "r")
#     # UPDATE = temps.read()
#     # users.close()
#
#     set = 'tag'
#     set_name = 'test_tag_1'
#     where = ('username')
#     where_name = (str(user))
#     sql_update(con, set, set_name, where, where_name)
#     await call.message.answer("You are in the user card " + '/' + user + ' and trying to change ' + call.data)
#
#
# @dp.callback_query_handler(text='test_tag_2')
# async def send_random_value(call: types.CallbackQuery):
#     users = open(str(call['from'].id) + "user.txt", "r")
#     user = users.read()
#     users.close()
#
#     print(call.data)
#     # temps = open(str(call['from'].id) + "temp.txt", "r")
#     # UPDATE = temps.read()
#     # users.close()
#
#     set = 'tag'
#     set_name = 'test_tag_2'
#     where = ('username')
#     where_name = (str(user))
#     sql_update(con, set, set_name, where, where_name)
#     await call.message.answer("You are in the user card " + '/' + user + ' and trying to change ' + call.data)
#
# @dp.callback_query_handler(text='test_tag_3')
# async def send_random_value(call: types.CallbackQuery):
#     users = open(str(call['from'].id) + "user.txt", "r")
#     user = users.read()
#     users.close()
#     print(call.data)
#     # temps = open(str(call['from'].id) + "temp.txt", "r")
#     # UPDATE = temps.read()
#     # users.close()
#     set = 'tag'
#     set_name = 'test_tag_3'
#     where = ('username')
#     where_name = (str(user))
#     sql_update(con, set, set_name, where, where_name)
#     await call.message.answer("You are in the user card " + '/' + user + ' and trying to change ' + call.data)
#
# @dp.callback_query_handler(text=[button for button in name_buttons])
# async def send_random_value(call: types.CallbackQuery):
#     print(call)
#     users = open(str(call['from'].id) + "user.txt", "r")
#     user = users.read()
#     users.close()
#
#     print(call.data)
#     temps = open(str(call['from'].id) + "temp.txt", "r")
#     UPDATE = temps.read()
#     users.close()
#
#     balans = sql_select_id(con, user)
#     if call.data == 'wallet':
#         UPDATE = float(balans[11]) + float(UPDATE)
#         set = (str(call.data))
#         set_name = (str(UPDATE))
#         where = ('username')
#         where_name = (str(user))
#         sql_update(con, set, set_name, where, where_name)
#         await call.message.answer("You are in the user card " + '/'+user +  ' and trying to change ' + call.data)
#     else:
#
#         set = (str(call.data))
#         set_name = (str(UPDATE))
#         where = ('username')
#         where_name = (str(user))
#         sql_update(con, set, set_name, where, where_name)
#         await call.message.answer("You are in the user card " + '/'+user + ' and trying to change ' + call.data)

if __name__ == '__main__':
    executor.start_polling(dp)