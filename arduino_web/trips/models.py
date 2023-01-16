from operator import truediv
from django.db import models
import pymongo 
import datetime

# Create your models here.
connection_string = r"mongodb+srv://edison:eggplant62@cluster0.jhwgjnr.mongodb.net/test"
client = pymongo.MongoClient(connection_string)

room_db = client['arduino_weather_room']
my_room_db = room_db["夏茄子"]

local_db = client['arduino_weather_local']
my_local_db = local_db["夏茄子"]

future_db = client['arduino_weather_future']
my_future_db = future_db["夏茄子"]

def find_room_all():
    data_list = []
    for x in my_room_db.find({}, {"_id": 0}):
        data_list.append(x)
    print(data_list)
    return data_list

def  find_local_all():
    data_list = []
    for x in my_local_db.find({}, {"_id": 0}):
        data_list.append(x)
    print(data_list)
    return data_list

#只保留今天(看預測的準不準)和明天(主要)的資料，所以超過兩筆，即刪除最舊的資料
def  future_oldest_data_del():
    before_yesterday = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%m-%d")
    data_list = []
    for x in my_future_db.find({}, {"日期": before_yesterday}):
        data_list.append(x)
    print("刪除此資料:(以下) ")
    print( data_list )
    my_future_db.delete_one( data_list[0] )

#返回最新一筆 隔日天氣 的 預測
def  find_future_last():
    future_last_one = my_future_db.find().sort('_id', -1)
    future_last_one = next(future_last_one)
    #print(future_last_one['天氣現象'])
    return future_last_one

def  find_future_old():
    future_old_one = my_future_db.find_one()
    #取出未來預測資料(只有兩筆 今日、明日)中的 舊資料 即 今天的天氣預測
    return future_old_one

#返回最新一筆 arduino傳過來的房內資訊
def find_room_last():
    room_last_one = my_room_db.find().sort('_id', -1)
    room_last_one = next(room_last_one)
    #print(room_last_one)
    return room_last_one

#返回最新一筆 室外天氣狀況
def find_local_last():
    local_last_one = my_local_db.find().sort('_id', -1)
    local_last_one = next(local_last_one)
    #print(local_last_one)
    return local_last_one


def del_old_local_data():
    #算出超過一周的日期，刪掉。   本系統只紀錄一周內發生的事
    the_final_day = (datetime.datetime.now()+datetime.timedelta(days=-8)).strftime("%m-%d")
    print("the_del_day == ",the_final_day)
    # my_room_db.delete_one( { "date": the_final_day } ) 刪除一筆
    #刪除多個
    my_room_db.delete_many( { "date": the_final_day } ) 

def del_old_room_data():
    #算出超過一周的日期，刪掉。   本系統只紀錄一周內發生的事
    the_final_day = (datetime.datetime.now()+datetime.timedelta(days=-9)).strftime("%m-%d")
    #print(the_final_day)
    # my_room_db.delete_one( { "date": the_final_day } ) 刪除一筆
    #刪除多個
    my_room_db.delete_many( { "date": the_final_day } ) 

#---------------------------------------------------------------------------------------------------DB儲存資料-------------------------------------------------------
def insert_room_data(User_name,data_date,data_time,temperature,humandity,pm25,co2,tvoc):
    insert_data = {"User_name": User_name,"date": data_date ,"time": data_time , "arduino_room" : {"溫度": temperature,"濕度": humandity,"pm2_5": pm25,"co2": co2,"tvoc": tvoc}}
    my_room_db.insert_one(insert_data)

def insert_local_data(User_name,localname,DATE,TIME,WDIR,WDSD,TEMP,HUMD,H_24R,D_TX,D_TXT,D_TN,D_TNT,PM25,PM25T,UVI,UVIT):
    insert_data = {"User_name": User_name,"Localname" : localname, "日期" : DATE, "時間" : TIME,
                    "weather_now": {
                        "風向": WDIR,
                        "風速": WDSD,
                        "氣溫": TEMP,
                        "濕度": HUMD,
                        "H_24R": H_24R,
                        "最高溫度": D_TX,
                        "高溫時間": D_TXT,
                        "最低溫度": D_TN,
                        "低溫時間": D_TNT,
                        "PM2_5"  : PM25,
                        "PM2_5T": PM25T,
                        "紫外線" : UVI,
                        "紫外線T": UVIT
                    }
    }
    my_local_db.insert_one(insert_data)


def insert_future_data(User_name,localname,future_Date,
                        future_Weather_phenomenon_0t3,
                        future_Weather_phenomenon_3t6,
                        future_Weather_phenomenon_6t9,
                        future_Weather_phenomenon_9t12,
                        future_Weather_phenomenon_12t15,
                        future_Weather_phenomenon_15t18,
                        future_Weather_phenomenon_18t21,
                        future_Weather_phenomenon_21t24,
                        future_TEMP_0t3,
                        future_TEMP_3t6,
                        future_TEMP_6t9,
                        future_TEMP_9t12,
                        future_TEMP_12t15,
                        future_TEMP_15t18,
                        future_TEMP_18t21,
                        future_TEMP_21t24,
                        future_HUMD_0t3,
                        future_HUMD_3t6,
                        future_HUMD_6t9,
                        future_HUMD_9t12,
                        future_HUMD_12t15,
                        future_HUMD_15t18,
                        future_HUMD_18t21,
                        future_HUMD_21t24,
                        future_feel_0t3,
                        future_feel_3t6,
                        future_feel_6t9,
                        future_feel_9t12,
                        future_feel_12t15,
                        future_feel_15t18,
                        future_feel_18t21,
                        future_feel_21t24,
                        future_rain_0t3,
                        future_rain_3t6,
                        future_rain_6t9,
                        future_rain_9t12,
                        future_rain_12t15,
                        future_rain_15t18,
                        future_rain_18t21,
                        future_rain_21t24,
                        ):
    
    insert_data = {"User_name": User_name,"Localname" : localname, "日期" : future_Date,
                    "天氣現象": {
                        "00到03": future_Weather_phenomenon_0t3,
                        "03到06": future_Weather_phenomenon_3t6,
                        "06到09": future_Weather_phenomenon_6t9,
                        "09到12": future_Weather_phenomenon_9t12,
                        "12到15": future_Weather_phenomenon_12t15,
                        "15到18": future_Weather_phenomenon_15t18,
                        "18到21": future_Weather_phenomenon_18t21,
                        "21到24": future_Weather_phenomenon_21t24
                    },
                    "溫度": {
                        "00到03": future_TEMP_0t3,
                        "03到06": future_TEMP_3t6,
                        "06到09": future_TEMP_6t9,
                        "09到12": future_TEMP_9t12,
                        "12到15": future_TEMP_12t15,
                        "15到18": future_TEMP_15t18,
                        "18到21": future_TEMP_18t21,
                        "21到24": future_TEMP_21t24
                    },
                    "濕度": {
                        "00到03": future_HUMD_0t3,
                        "03到06": future_HUMD_3t6,
                        "06到09": future_HUMD_6t9,
                        "09到12": future_HUMD_9t12,
                        "12到15": future_HUMD_12t15,
                        "15到18": future_HUMD_15t18,
                        "18到21": future_HUMD_18t21,
                        "21到24": future_HUMD_21t24
                    },
                    "舒適度": {
                        "00到03": future_feel_0t3,
                        "03到06": future_feel_3t6,
                        "06到09": future_feel_6t9,
                        "09到12": future_feel_9t12,
                        "12到15": future_feel_12t15,
                        "15到18": future_feel_15t18,
                        "18到21": future_feel_18t21,
                        "21到24": future_feel_21t24
                    },
                    "降雨機率": {
                        "00到03": future_rain_0t3,
                        "03到06": future_rain_3t6,
                        "06到09": future_rain_6t9,
                        "09到12": future_rain_9t12,
                        "12到15": future_rain_12t15,
                        "15到18": future_rain_15t18,
                        "18到21": future_rain_18t21,
                        "21到24": future_rain_21t24
                    }
    }
    my_future_db.insert_one(insert_data)


#------------------------------------------------------------------------------ROOM DATA整理(室內)----------------------------------------------------
 #兩種資料分類， 1. 按照 時間 每個小時 6:00~24:00 的平均(一整周) ， 2. 按照 日期 每個禮拜 一~日 的平均 

room_data_list={}

date0 = (datetime.datetime.now()+datetime.timedelta(days=0)).strftime("%m-%d")
date1 = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%m-%d")
date2 = (datetime.datetime.now()+datetime.timedelta(days=-2)).strftime("%m-%d")
date3 = (datetime.datetime.now()+datetime.timedelta(days=-3)).strftime("%m-%d")
date4 = (datetime.datetime.now()+datetime.timedelta(days=-4)).strftime("%m-%d")
date5 = (datetime.datetime.now()+datetime.timedelta(days=-5)).strftime("%m-%d")
date6 = (datetime.datetime.now()+datetime.timedelta(days=-6)).strftime("%m-%d")
date7 = (datetime.datetime.now()+datetime.timedelta(days=-7)).strftime("%m-%d")
date_all =[ date0,date1,date2,date3,date4,date5,date6,date7]

ti = [
    "01:00","02:00","03:00","04:00","05:00","06:00",
    "07:00","08:00","09:00","10:00","11:00","12:00",
    "13:00","14:00","15:00","16:00","17:00","18:00",
    "19:00","20:00","21:00","22:00","23:00","00:00"
]

#此處為 按照 小時 每個天的 這個時間 的平均(一整周)， 存放 公用變數 名稱格式: room_data_time_XX (xx為時間縮寫(拿掉分鐘) ) -------------1
def return_room_data_collect_1():
    time_data_arrange={} #存放整理後的 平均這個小時 每日 資料
    time_data=[]
    #所有 的 這個時間點 ，以時間點為key的所有資料，按照ti分類
    for i in ti:
        for l in my_room_db.find({"time": { "$regex": '^'+str(i[:2]) }}): #regex+正則表達
            #print(time_data)
            time_data.append(l)

        #print("time_data = ",time_data)
        globals()['room_data_time_'+str(i[:2])] = time_data
        time_data=[]
    #print(room_data_time_02)

    #把數個這個時段的資料作平均
    day_same_hour={}
    for i in ti:
        for l in globals()['room_data_time_'+str(i[:2])]:
            l['date'] = l['date'][3:]
            if l['date'] not in day_same_hour:
                day_same_hour[ l['date'] ] = l
            else:
                day_same_hour[l['date']]['arduino_room']['溫度'] = (int(l['arduino_room']['溫度'])+int(day_same_hour[l['date']]['arduino_room']['溫度']) )/2
                day_same_hour[l['date']]['arduino_room']['濕度'] = (int(l['arduino_room']['濕度'])+int(day_same_hour[l['date']]['arduino_room']['濕度']) )/2
                day_same_hour[l['date']]['arduino_room']['pm2_5'] = (int(l['arduino_room']['pm2_5'])+int(day_same_hour[l['date']]['arduino_room']['pm2_5']) )/2
                day_same_hour[l['date']]['arduino_room']['co2'] = (int(l['arduino_room']['co2'])+int(day_same_hour[l['date']]['arduino_room']['co2']) )/2
                day_same_hour[l['date']]['arduino_room']['tvoc'] = (int(l['arduino_room']['tvoc'])+int(day_same_hour[l['date']]['arduino_room']['tvoc']) )/2
            time_data_arrange[str(i[:2])] = day_same_hour
        day_same_hour={}
    #time_data_arrange 一個以時間為基底 所有有這段時間的紀錄 天
    # time_data_arrange = {
    # '10(時間)': {
    #       '10(日期)': {'_id': ObjectId('62f31d174f1115b6eaa9158b'), 'User_name': '夏茄子', 'date': '08-10', 'time': '10:50', 'arduino_room': {'溫度': '25', '濕度': '61', 'pm2_5': '6', 'co2': '404', 'tvoc': '0'}},
    #       '11': {'_id': ObjectId('62f31d174f1115b6eaa9158b'), 'User_name': '夏茄子', 'date': '08-11', 'time': '10:20', 'arduino_room': {'溫度': '25', '濕度': '61', 'pm2_5': '6', 'co2': '404', 'tvoc': '0'}}
    # }, 
    # '11': {'10': {'_id': ObjectId('62f3230ace22ac7f700f66ae'), 'User_name': '夏茄子', 'date': '08-10', 'time': '11:16', 'arduino_room': {'溫度': 25.5, '濕度': '61', 'pm2_5': '7', 'co2': '403', 'tvoc': '0'}}} 
    # }
    #print(time_data_arrange)
    #print(time_data_arrange['24']['22']['arduino_room']['溫度'])
    return time_data_arrange
   
#此處為 按照 日期 做整理(即每一個單獨天的資料)日期以 當日 回推一周， 存放 公用變數 名稱格式: room_data_date_XX (xx為日期縮寫(拿掉月份) ) -----2
def return_room_data_collect_2():
    date_data_arrange={} #存放整理後的 每一日 平均每小時 資料
    date_data=[]
    for i in date_all:
        for l in my_room_db.find({"date": i}):
            date_data.append(l)
        #print("time_data = ",time_data)
        globals()['room_data_date_'+str(i[3:])] = date_data
        date_data=[]
    #print("room_data_date_ == " , room_data_date_15)

    #一樣要把同一天相同時段的資料給平均
    same_day_hour={}
    for i in date_all:
        for l in globals()['room_data_date_'+str(i[3:])]:
            l['time'] = l['time'][:2]
            if l['time'] not in same_day_hour:
                same_day_hour[ l['time'] ] = l
            else:
                same_day_hour[l['time']]['arduino_room']['溫度'] = (int(l['arduino_room']['溫度'])/2 +int(same_day_hour[l['time']]['arduino_room']['溫度'])/2 )
                same_day_hour[l['time']]['arduino_room']['濕度'] = (int(l['arduino_room']['濕度'])/2+int(same_day_hour[l['time']]['arduino_room']['濕度'])/2 )
                same_day_hour[l['time']]['arduino_room']['pm2_5'] = (int(l['arduino_room']['pm2_5'])/2+int(same_day_hour[l['time']]['arduino_room']['pm2_5'])/2 )
                same_day_hour[l['time']]['arduino_room']['co2'] =  (int(l['arduino_room']['co2'])/2+int(same_day_hour[l['time']]['arduino_room']['co2'])/2 )
                same_day_hour[l['time']]['arduino_room']['tvoc'] = (int(l['arduino_room']['tvoc'])/2+int(same_day_hour[l['time']]['arduino_room']['tvoc'])/2 ) 
            date_data_arrange[str(i[3:])] = same_day_hour
        same_day_hour={}
    #date_data_arrange 以日期為KEY，下面劃分出所有時段的資料
    # date_data_arrange = {
    #   "15(日期)": {
    #     "17(時間)": {
    #         "_id": "62fa11d086a240f1af2317fc","User_name": "夏茄子","date": "08-15","time": "17","arduino_room": {"溫度": 0.5,"濕度": "43","pm2_5": "1","co2": "406","tvoc": "1"}
    #     },
    #     "18": {
    #         "_id": "62fa1df1ef6f0a5c8e045348","User_name": "夏茄子","date": "08-15","time": "18","arduino_room": {"溫度": "24","濕度": "44","pm2_5": "1","co2": "403","tvoc": "0"}
    #     }
    #   }
    #}
    #print(date_data_arrange)
    return date_data_arrange

def return_room_data_collect():
    room_data_list['time_data']=return_room_data_collect_1()
    room_data_list['date_data']=return_room_data_collect_2()
    #print(room_data_list)
    del_old_room_data()
    return room_data_list
    #取出限定資料
    # for i in my_room_db.find({"time": "02:00","arduino_room.溫度": "24" }):
    #     all_data_list.append(i)
    # print(all_data_list)

    #取出全部資料
    # for i in my_room_db.find({}, {"_id": 0}):
    #     all_data_list.append(i)

#------------------------------------------------------------------------------WEATHER DATA整理(室外)----------------------------------------------------
 #兩種資料分類， 1. 按照 時間 每個小時 6:00~24:00 的平均(一整周) ， 2. 按照 日期 每個禮拜 一~日 的平均 

local_data_list={}

#此處為 按照 小時 每個天的 這個時間 的平均(一整周)， 存放 公用變數 名稱格式: weather_data_time_XX (xx為時間縮寫(拿掉分鐘) ) -------------1
def return_weather_data_collect_1():
    time_data_arrange={} #存放整理後的 平均這個小時 每日 資料
    time_data=[]
    #所有 的 這個時間點 ，以時間點為key的所有資料，按照ti分類
    for i in ti:
        for l in my_local_db.find({"時間": { "$regex": '^'+str(i[:2]) }}): #regex+正則表達
            time_data.append(l)
            #print("time_data = ",time_data)
        globals()['local_data_time_'+str(i[:2])] = time_data
        time_data=[]
    #print( "local_data_time_01 == ", local_data_time_01 )

    #把數個這個時段的資料作平均
    day_same_hour={}
    for i in ti:
        for l in globals()['local_data_time_'+str(i[:2])]:
            l['日期'] = l['日期'][3:]
            if l['日期'] not in day_same_hour:
                day_same_hour[ l['日期'] ] = l
            time_data_arrange[str(i[:2])] = day_same_hour
        day_same_hour={}
    #time_data_arrange 一個以時間為基底 所有有這段時間的紀錄 天
    # time_data_arrange = {
    #  {
    #   '01(時間)': 
    #       {
    #           '20'(日期): {'_id': ObjectId('62ffcde0c1c05610e7321999'), 'User_name': '夏茄子', 'Localname': '安南', '日期': '20', '時間': '01:00', 'weather_now': {'風向': '0', '風速': '0.1', '氣溫': '29.0', '濕度': '0.86', 'H_24R': '0.0', '最高溫度': '29.30', '高溫時間': '00:10', '最低溫度': '29.00', '低溫時間': '01:00', 'PM2_5': '15', 'PM2_5T': '11:00PM', '紫外線': '0', '紫外線T': '01:00AM'} }
    #       }
    #  }
    #print("time_data_arrange == ", time_data_arrange )
    return time_data_arrange
   
#此處為 按照 日期 做整理(即每一個單獨天的資料)日期以 當日 回推一周， 存放 公用變數 名稱格式: room_data_date_XX (xx為日期縮寫(拿掉月份) ) -----2
def return_weather_data_collect_2():
    date_data_arrange={} #存放整理後的 每一日 平均每小時 資料
    date_data=[]
    for i in date_all:
        for l in my_local_db.find({"日期": i}):
            date_data.append(l)
        #print("time_data = ",time_data)
        globals()['local_data_date_'+str(i[3:])] = date_data
        date_data=[]
    #print("room_data_date_ == " , room_data_date_15)

    #一樣要把同一天相同時段的資料給平均
    same_day_hour={}
    for i in date_all:
        for l in globals()['local_data_date_'+str(i[3:])]:
            l['時間'] = l['時間'][:2]
            if l['時間'] not in same_day_hour:
                same_day_hour[ l['時間'] ] = l
            date_data_arrange[str(i[3:])] = same_day_hour
        same_day_hour={}
    #date_data_arrange 以日期為KEY，下面劃分出所有時段的資料
    # date_data_arrange = {
    #   "15(日期)": {
    #     "17(時間)": {
    #         "_id": "62fa11d086a240f1af2317fc","User_name": "夏茄子","date": "08-15","time": "17","arduino_room": {"溫度": 0.5,"濕度": "43","pm2_5": "1","co2": "406","tvoc": "1"}
    #     },
    #     "18": {
    #         "_id": "62fa1df1ef6f0a5c8e045348","User_name": "夏茄子","date": "08-15","time": "18","arduino_room": {"溫度": "24","濕度": "44","pm2_5": "1","co2": "403","tvoc": "0"}
    #     }
    #   }
    #}
    #print(date_data_arrange)
    return date_data_arrange

def return_weather_data_collect():
    local_data_list['time_data']=return_weather_data_collect_1()
    local_data_list['date_data']=return_weather_data_collect_2()
    #print(room_data_list)
    del_old_local_data()
    return local_data_list
    #取出限定資料
    # for i in my_room_db.find({"time": "02:00","arduino_room.溫度": "24" }):
    #     all_data_list.append(i)
    # print(all_data_list)

    #取出全部資料
    # for i in my_room_db.find({}, {"_id": 0}):
    #     all_data_list.append(i)