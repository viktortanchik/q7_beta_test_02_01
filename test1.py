from datetime import *
import csv
from db import *

today = datetime.today()
week = today.strftime("%U")
temps = open("week"+ "temp.txt", "r")
UPDATE_week = temps.read()
temps.close()
con = sqlite3.connect('bot.sqlite')

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
    #print("OLD WEEK")





    # записеваем в базу новое значения

#
# checkdb='no credit'
#
# if (checkdb == 'no credit') and ((float(1) + float(-5)) < 0):
#     print("OK")
# else:
#     print("error")
#
# # names= '/test1/test2/test3/test4/test5/test6'
# # name=[]
# # tempname=''
# # for i in names:
# #     if i !='/':
# #         tempname+=i
# #
# #     else:
# #         name.append(tempname)
# #         tempname = ''
# #
# #
# # print(name)



# myData = ('real_name', 'username', 'user_id', 'chat', 'agency', 'payid', 'strikes', 'hyperlink', 'tag', 'notes',
#           'wallet', 'cash_out')
# temp_db = get_all(con)
#
# myFile = open('db.csv', 'w')
# with myFile:
#     writer = csv.writer(myFile)
#     writer.writerow(myData)
#     for i in temp_db:
#         print(i[1:])
#         writer.writerow(i[1:])


