import sqlite3
import time
import sqlite3

from telethon import sync, events
import asyncio

from telethon.sync import TelegramClient
from telethon import functions, types

from telethon.tl.types import PeerUser, PeerChat, PeerChannel

# для корректного переноса времени сообщений в json
from datetime import date, datetime
from db import *
#['@Ihortihor',674868256]

chat_name='test_Q7_create_chat_01'
admin_id=['@Ihortihor',674868256,'@Q7CRM_test_bot']
account=4

async def create_chat(chat_name,admin_id,account):
    con = sqlite3.connect('bot.sqlite')

    print("chat_name>>",chat_name)
    print("admin_id>>",admin_id)
    x = account
    db = sqlite3.connect('Account.db')
    cur = db.cursor()
    print(cur)
    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone, ' Номер ',x)
    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))

    client = TelegramClient(session, api_id, api_hash)
    task1 = asyncio.create_task(client.start())
    await task1
    #x+= 1
    #time.sleep(1)
    #use=[674868256]
    results = await client(functions.messages.CreateChatRequest(
        users=admin_id,
        title=str(chat_name[0])
    ))
    print(results)
    #print(results.chats[0].id)
    time.sleep(1)
    await client.send_message(results.chats[0].id, 'Hello!')
    chat_id= int(results.chats[0].id)
    print("chat_id>>",chat_id)
    id='-'
    id+=str(chat_id)
    id_name=[id,chat_name[0]]
    print("id_name>>",id_name)
    sql_insert_chat_info(con,id_name)
    #697292785
    for i in range(len(admin_id)):
        result = await client(functions.messages.EditChatAdminRequest(
            chat_id=chat_id,
            user_id=admin_id[i],  # '@Ihortihor',
            is_admin=True
        ))
        print(result)
    task3 = asyncio.create_task(client.disconnect())
    await task3



async def find_user(chat_id,user_name,account):
    print("chat_id>>",chat_id)
    print("user_name>>",user_name)
    x = 2
    db = sqlite3.connect('Account.db')
    cur = db.cursor()
    print(cur)
    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone, ' Номер ',x)
    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))

    client = TelegramClient(session, api_id, api_hash)
    task1 = asyncio.create_task(client.start())
    await task1
    #x+= 1

    #members =
    task2 = asyncio.create_task(client.get_participants(chat_id))

    for i in await task2:
        print(i.username)
        if i.username == user_name[0]:
            print("i.id>>",i.id)
            return i.id

    task3 = asyncio.create_task(client.disconnect())
    await task3