from datetime import *
import csv
from db import *
import time
con = sqlite3.connect('bot.sqlite')
while True:
    time.sleep(0.5)
    #today = datetime.utcnow()
    current_time_in_utc = datetime.utcnow()
    today = current_time_in_utc + timedelta(hours=10)
    #today = datetime.now(timezone(UTC+10:00))


    week = today.strftime("%U")
    temps = open("week"+ "temp.txt", "r")
    UPDATE_week = temps.read()
    temps.close()


    if UPDATE_week != week:
        todays = datetime.today()
        #print(todays.strftime("%m/%d/%Y"))
        myFile = open('WEEK.csv', 'w')
        file = open("week"+ "temp.txt", "w")
        file.write(week)
        file.close()
        alluser = get_all(con)
        d = datetime.today() - timedelta(days=7)
        title=['NAME CHAT',' OLD WEEK '+d.strftime("%m/%d/%Y")+" NEW WEEK "+todays.strftime("%m/%d/%Y")]
        with myFile:
            writer = csv.writer(myFile)
            writer.writerow(title)
            for i in alluser:
                print(i[11])
                new=[i[4],i[11]]
                writer.writerow(new)
                # записываем текущее значения кошелька в базу для хранения на этой неделе
                set = 'name_of_agency'
                set_name = (str(i[11]))
                where = ('chat')
                where_name = (str(i[4]))
                sql_update(con, set, set_name, where, where_name)
                # изменяем текущее значения  кощелька на 0
                set = 'wallet'
                set_name = (str(0))
                where = ('chat')
                where_name = (str(i[4]))
                sql_update(con, set, set_name, where, where_name)
    else:
        pass
