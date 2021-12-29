# Переделано под команды

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
from create_chat_02 import create_chat,find_user
#from create_chat.create_01 import create_chat
#from create_chat import create_01

bot = Bot(token="5049839636:AAGU4R4Ibn-qwonYWMBfFWHfU0xM6LubqFA")
dp = Dispatcher(bot)
con = sqlite3.connect('bot.sqlite')
import re

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

async def find_all():
    rows = (get_all(con))
    return rows

def all_users():
    rows = (get_all(con))
    newrow = []
    for row in range(len(rows)):
        newrow.append( '/'+rows[row][2])
    return newrow
# когда пользователь подкулючился к чату.
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
        #print('>>>>>>>>>>',adm[i])
        if int(adm[i]) == int(message['from'].id):
            print("ADMIN JOIN CHAT")
            flag_admin=False

    if flag_admin==True:
        data =['real_name',str(message['from'].username),'user_id',str(message.chat.title),'0','0','0','0','tag','notes','0',"cash_out"]
        sql_insert_all(con,data)
        adms = get_admins(con)
        for i in adms:
            print("added new user>>",i)
            await bot.send_message(int(i[1]), "Hey!\n added new user\n Chat "+str(message.chat.title)+'\n username '+str(message['from'].username))
    #rowsget_all(con)
    #await message.reply("Привет!\n добавлен новый пользователь ")
@dp.message_handler(commands='help')
async def process_start_command(message: types.Message):
    flag = admins(message['from'].id)
    if flag!=True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
        print(message)
        print(message['from'].username)
    else:
        mes='Available commands.\n ' \
            '/CARD this command shows the users card \n ' \
            '/Change_balance this command changes the users balance. First a number then a command example( 1000 (enter) /Change_balance) \n' \
            '/Change_tag this command changes  values tag. First a values then a command example( bonus (enter) /Change_tag) \n' \
            '/Create_chat this command create  new chat example( chat/name/123 (enter) /Create_chat) \n' \
            '/Del_user this command deletes user example( username (enter) /Del_user)\n ' \
            '/Save_admin \n' \
            '/send_file \n' \
            '/send_week \n' \
            '/spam tag = bonus \n ' \
            ' tag = no credit'
        await message.answer(mes )


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
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        buttons = ["Main menu"]
        keyboard.add(*buttons)
        #await message.answer(".", reply_markup=keyboard)
        await message.delete()
        time.sleep(1)
        #await bot.send_message(674868256, "Hey!\n added new user\n Chat "+message.chat.title+'\n username '+message['from'].username)
        #await bot.send_message(message.chat.id,'start bot', reply_markup=keyboard)
        adms = get_admins(con)

        for i in adms:

            await bot.send_message(int(i[1]),
                               "Hey!\n added new user\n Chat " + '\n username ' + message[
                                   'from'].username)

    chat = await bot.get_chat_member(message.chat.id, message['from'].id)
    print(chat)


newrows=[]
#$$$$$$$$$$$$$$$$$$$$$$$$$$$4
# genelamain =["Main menu"]
# #@dp.message_handler(Text(equals=genelamain))
# @dp.message_handler(commands='start')
# async def with_puree(message: types.Message):
#     flag = admins(message['from'].id)
#     if flag != True:
#         #await message.delete()
#         await message.answer("this chat is not allowed to work with the bot " )
#     else:
#         await message.delete()
#
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         #buttons = ["Find","USER CARD","Settings ⚙"]
#         #buttons = ["CARD",'wallet_','Change_info',"Settings ⚙"]
#         buttons = ["CARD",'Change_balance ','Change_info',"Settings ⚙"]
#         keyboard.add(*buttons)
#         await bot.send_message(message['from'].id,"at your serviсe", reply_markup=keyboard)
#         #await message.answer("at your serviсe", reply_markup=keyboard)
#         #await message.delete()


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
        buttons = ["Main menu", "ALL ADMIN ⚙", "Add admin 🔧","Del user 🛠","Del admin 🛠","send_file","Create_chat","send_week","Find",'ALL USER']
        keyboard.add(*buttons)
        await message.answer("at your serviсe", reply_markup=keyboard)

#@dp.message_handler(Text(equals="Del user 🛠"))
@dp.message_handler(commands='Del_user')
async def find_chat(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        #print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        print("USER_DELL>>",UPDATE)
        temp = [str(UPDATE)]
        userdb = sql_select_user(con,temp)
        print("del userdb",userdb)
        chat_info = sql_select_chat_info(con,userdb[4])
        print("del chat_info",chat_info)
        print("dle chat_info",int(chat_info[0]))
        chat_id = int(chat_info[0])
        user_name = temp
        account=1
        user_id = await find_user(chat_id,user_name,account)
        #time.sleep(10)
        await asyncio.sleep(5)

        print("del user_id",user_id)
        await message.bot.kick_chat_member(chat_id=chat_info[0], user_id=user_id)

        delete_user(con,temp)

        await message.answer("at your serviсe")

#@dp.message_handler(Text(equals="Del admin 🛠"))
@dp.message_handler(commands='Del_admin')

async def find_chat(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        chat_find = await find_all()
        #print(chat_find)
        temps = open(str(message['from'].id) + "temp.txt", "r")
        UPDATE = temps.read()
        temps.close()
        print("USER_DELL>>",UPDATE)
        temp = [str(UPDATE)]
        delete_admin(con,temp)
        delete_super_admin(con, temp)

        await message.answer("at your serviсe")

equal=['Create_chat']
#@dp.message_handler(Text(equals=equal))
@dp.message_handler(commands='Create_chat')
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
        len_admins=['@Q7CRM_test_bot']
        for i in adms:
            len_admins.append(int(i[1]))
        await create_chat(temp,len_admins,2)
        #create_chat(str(temp),)



equal=['send_week']

#@dp.message_handler(Text(equals=equal))
@dp.message_handler(commands='send_week')
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.reply_document(open("WEEK.csv", "rb"))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        await message.answer("at your serviсe")

equal=['send_file']
#@dp.message_handler(Text(equals=equal))
@dp.message_handler(commands='send_file')
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
        await message.reply_document(open("db.csv", "rb"))
        await message.answer("at your serviсe")
#
# equal=['Add admin 🔧']
# #@dp.message_handler(Text(equals=equal))
# @dp.message_handler(commands='Add_admin')
# async def settings(message: types.Message):
#     flag = super_admin(message['from'].id)
#     if flag != True:
#         #await message.delete()
#         await message.answer("this chat is not allowed to work with the bot " )
#     else:
#         await message.delete()
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         buttons = ["Main menu", "Save admin 🔧"]
#         keyboard.add(*buttons)
#         await message.answer("at your serviсe", reply_markup=keyboard)
#

######################################################################

equal=['ALL ADMIN ⚙']
#@dp.message_handler(Text(equals=equal))
@dp.message_handler(commands='all_admin')
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Click me", callback_data="ALLADMIN"))
        print("all_admin")
        #await message.answer("ALL ADMINS", reply_markup=keyboard)
        await bot.send_message( message['from'].id, 'all_admin', reply_markup=keyboard)


@dp.callback_query_handler(text="ALLADMIN")
async def send_random_value(call: types.CallbackQuery):
    flag = admins(call['from'].id)
    if flag != True:
        # await message.delete()
        await call.answer("this chat is not allowed to work with the bot ")
    else:
        admi = get_admins(con)
        mes=''
        for i in admi:
            mes += str(i[1])
            mes += '\n'
        await call.answer(text=mes, show_alert=True)
        await call.message.delete()
    # или просто await call.answer()

#######################################################################

equal=['Save admin 🔧']

#@dp.message_handler(Text(equals=equal))
@dp.message_handler(commands='Save_admin')
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
        sql_insert_super_admin(con,temp)
        await message.answer("SAVE_ADMIN")
#
######################################################################

equal=['ALL USER']

#@dp.message_handler(Text(equals=equal))
@dp.message_handler(commands='ALL_USER')
async def settings(message: types.Message):
    flag = super_admin(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Click me", callback_data="ALLUSER"))
        await message.answer("ALL USER", reply_markup=keyboard)

@dp.callback_query_handler(text="ALLUSER")
async def send_random_value(call: types.CallbackQuery):
    flag = admins(call['from'].id)
    if flag != True:
        # await message.delete()
        await call.answer("this chat is not allowed to work with the bot ")
    else:
        rows = get_all(con)
        print('rows>>', rows)
        mes = ''
        for row in range(len(rows)):
            print(rows[row])
            mes +=  str(rows[row][2])
            newrows.append(rows[row][2])
            print('newrows >> ', newrows)
        await call.answer(text=mes, show_alert=True)
        await call.message.delete()
    # или просто await call.answer()

#######################################################################
#
# @dp.message_handler(Text(equals="Find"))
# async def with_puree(message: types.Message):
#     flag = admins(message['from'].id)
#     if flag != True:
#         await message.delete()
#         await message.answer("this chat is not allowed to work with the bot " )
#     else:
#         await message.delete()
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         buttons = ["Main menu",'real_name 🔎','username 🔎','user_id 🔎','chat 🔎',  'payid 🔎', 'strikes 🔎',
#                         'tag 🔎', 'notes 🔎', 'wallet 🔎','cash_out 🔎']
#         keyboard.add(*buttons)
#         await message.answer("Find ", reply_markup=keyboard)

#@dp.message_handler(Text(equals="chat 🔎"))
@dp.message_handler(commands='Find_chat')
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

#@dp.message_handler(Text(equals="user_id 🔎"))
@dp.message_handler(commands='Find_user_id')
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

#@dp.message_handler(Text(equals="username 🔎"))
@dp.message_handler(commands='Find_username')
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

#@dp.message_handler(Text(equals="real_name 🔎"))
@dp.message_handler(commands='Find_real_name')
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

#@dp.message_handler(Text(equals="name_of_agency 🔎"))
@dp.message_handler(commands='Find_name_of_agency')
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

#@dp.message_handler(Text(equals="payid 🔎"))
@dp.message_handler(commands='Find_payid')

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

#@dp.message_handler(Text(equals="strikes 🔎"))
@dp.message_handler(commands='Find_strikes')
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

#@dp.message_handler(Text(equals="hyperlink 🔎"))
@dp.message_handler(commands='Find_hyperlink')
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

#@dp.message_handler(Text(equals="tag 🔎"))
@dp.message_handler(commands='Find_tag')
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


#@dp.message_handler(Text(equals="notes 🔎"))
@dp.message_handler(commands='Find_notes')

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

#@dp.message_handler(Text(equals="wallet 🔎"))
@dp.message_handler(commands='Find_wallet')

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


#@dp.message_handler(Text(equals="cash_out 🔎"))
@dp.message_handler(commands='Find_cash_out')
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
#
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


#@dp.message_handler(Text(equals="CARD"))
@dp.message_handler(commands='CARD')
async def with_puree(message: types.Message):
    flag = admins(message['from'].id)
    if flag != True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
    else:
        await message.delete()
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Click me", callback_data="CARD"))
        await message.answer("User card", reply_markup=keyboard)

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
            deposit = 'balance:   '
        else:
            deposit = 'credit:   '
        butt ='username: ' + card[2] +  '\n' + 'user_id '+card[2] + '\n' + 'payid: ' + card[6] + '\n' + 'strikes: ' + card[7] + '\n' + 'tag: ' + card[9] + '\n' + 'notes: ' + card[10] + '\n' + deposit + str(card[11]) + '\n' + 'cash_out:     ' + card[12] + '\n' +"last week's balance   "+card[5]
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


#@dp.message_handler(Text(equals='user_id'))
@dp.message_handler(commands='Change_user_id')

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

#@dp.message_handler(Text(equals='payid_'))
@dp.message_handler(commands='Change_payid')
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

#@dp.message_handler(Text(equals='strikes_'))
@dp.message_handler(commands='Change_strikes')

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

#@dp.message_handler(Text(equals='tag_'))
@dp.message_handler(commands='Change_tag')
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

#@dp.message_handler(Text(equals='notes_'))
@dp.message_handler(commands='Change_notes')
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

#@dp.message_handler(Text(equals='cash_out_'))
@dp.message_handler(commands='Change_cash_out')
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


#@dp.message_handler(Text(equals='Change_balance'))
@dp.message_handler(commands='Change_balance')

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
        checkdb = balans[9]
        print("checkdb >>",checkdb)
        if (checkdb=='no credit') and ((float(balans[11]) + float(UPDATE))<0):
            await message.answer("no credit")
        else:
            UPDATE = float(balans[11]) + float(UPDATE)
            set_name = (str(UPDATE))
            where = ('username')
            where_name = (str(user))
            sql_update(con, set, set_name, where, where_name)
        #await message.answer("You are in the user card " + '/' + user + ' and trying to change wallet')

@dp.message_handler(commands='spam')
async def process_start_command(message: types.Message):
    flag = admins(message['from'].id)
    if flag!=True:
        #await message.delete()
        await message.answer("this chat is not allowed to work with the bot " )
        print(message)
        print(message['from'].username)
    else:
        post = open(str(message['from'].id) + "spam.txt", "r")
        spam_id = post.read()
        post.close()
        #print(await bot.copy_message(message['from'].id))
        #print(message)
        chat_id=[]
        message_id= (int(message.message_id) -1)
        bonus = sql_select_tag(con,'bonus')
        for i in bonus:
            print("BONUS CHAT NAME >>",i)
            id = sql_select_chat_info(con, i)
            print("id>>>>",id[0])
            chat_id.append(id)
            await bot.forward_message(str(id[0]), message.from_user.id, int(spam_id))
        #await bot.send_message(782187872, (int(message.message_id) - 1))


        print("chat_id IN DB >>>",chat_id)

        #@Ihortihor
        #397656673
        #await bot.get_chat('Max/123456/q7')
        #print(await bot.get_chat())
        #await bot.forward_message('Ihortihor', message.from_user.id, message_id)


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    print("Photo>>",message)
    flag = admins(message['from'].id)
    if flag != True:
        pass
    else:
        # await message.delete()
        file = open(str(message['from'].id) + "spam.txt", "w")
        file.write(str(message.message_id))
        file.close()

@dp.message_handler()
async def process_start_command(message: types.Message):

    flag = admins(message['from'].id)
    if flag != True:
       pass
    else:
        print("message>>>>", message)
        getchat = await bot.get_chat(message.chat.id)
        #print("getchat.title>>", getchat)
        #await message.delete()
        file = open(str(message['from'].id) + "temp.txt", "w")
        file.write(str(message.text))
        file.close()
        if getchat.title != None:
            card = sql_select_chat(con, getchat.title)
            print("card>>",card)
            if getchat.title in card[4]:
                print(getchat.title)
                s1 = re.sub("[/]", "", card[2])
                #print(message['from'].id)
                #print('s1 >> ',s1)
                file = open(str(message['from'].id)+"user.txt", "w")
                file.write(s1)
                file.close()
                #card = sql_select_id(con,s1)
                #card = sql_select_chat(con,getchat.title)
                print("change_user")

if __name__ == '__main__':
    executor.start_polling(dp)