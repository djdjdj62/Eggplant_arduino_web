# from asyncio import futures
# from asyncio.windows_events import NULL
#from asyncio.windows_events import NULL
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from trips import models

from trips.weather_api import api_for_view

import requests
import json
import time
import datetime

User_name = "夏茄子"
city_name = "臺南"      
Localname = "安南"      #for PM2.5 and 綜合 測站的位置
county_name = "臺南市"  #for uvi 測站的位置
t = time.localtime()

def hello_world(request):
    
    return render(request, 'test.html')

def vue(request):
    return render(request, 'vue.html' , {"type_back": 'A' } )


def data_put_test(request):
    return render(request, 'put_data.html')



def the_page(request):
    weather_now_level={}
    weather_predict_future={}

    predict_future_weather_data={}
    weather_predict_future_icon={}

    today_total_temp=[]
    tomorrow_total_temp=[]

    #取得 室外 資料整理(key為 時間、日期)
    weather_data_list = models.return_weather_data_collect()
    
    #取得 房內 資料整理(key為 時間、日期)
    room_data_list = models.return_room_data_collect()
    
    #取得 最新 的當地天氣情況
    local_data = models.find_local_last()

    #取得 最新 的房內狀況
    room_data = models.find_room_last()

    #取得 最新 的天氣預測(明天)
    future_tomorrow_data = models.find_future_last()

    #取得 最舊 的天氣預測(當天)
    future_now_data = models.find_future_old()

    #下面用 現在時間 去取得 昨天 未來推測 的 天氣狀態 和 舒適度 預測
    now_date = time.strftime("%d", t )
    now_time = time.strftime("%H", t )
    weather_time_level = int( now_time )//3+1
    print( "now_time == ",now_time )
    print( "now_date == ",now_date )
    #print("本日的資料: ",room_data_list['date_data'][now_date])
    #print( "此時的資料:", room_data_list['time_data'][now_time])
    date_list=[]
    now_time_Roomdata={}
    now_time_localdata={}
    everyday_Room_average={}
    everyday_local_average={}
    #每日的 高低資料
    everyday_Room_hi={}
    everyday_Room_lo={}
    everyday_local_hi={}
    everyday_local_lo={}
    #製造 日期 表
    for i in range(8):
        date_list.append((datetime.datetime.now()+datetime.timedelta(days=-i)).strftime("%d"))
    #print(date_list)
    #取出要放在 chart_每日這個時段的xx 的資料
    #print(room_data_list['time_data'])
    for i in room_data_list['time_data']:
        if i == now_time:
            #print("find time")
            counter = 0
            for l in room_data_list['time_data'][i]:
                for counter in range(8):
                    if l == date_list[counter]:
                        #print("find date")
                        now_time_Roomdata[counter]=(room_data_list['time_data'][str(now_time)][l]['arduino_room'])
            counter = 0
            for counter in range(8):
                if counter not in now_time_Roomdata:
                    now_time_Roomdata[counter]={'溫度': '0', '濕度': '0', 'pm2_5': '0', 'co2': '0', 'tvoc': '0'}
                    #date_list[counter] = str( date_list[counter])
            break
    for i in weather_data_list['time_data']:
        if i == now_time:
            #print("find time")
            counter = 0
            for l in weather_data_list['time_data'][i]:
                for counter in range(8):
                    if l == date_list[counter]:
                        #print("find date")
                        now_time_localdata[counter]=(weather_data_list['time_data'][str(now_time)][l]['weather_now'])
                        if now_time_localdata[counter]['紫外線']=="":
                            now_time_localdata[counter]['紫外線'] = 0
                        if now_time_localdata[counter]['PM2_5']=="":
                            now_time_localdata[counter]['PM2_5'] = 0
            counter = 0
            for counter in range(8):
                if counter not in now_time_localdata:
                    now_time_localdata[counter]={'風向': '0', '風速': '0', '氣溫': '0', '濕度': '0', 'H_24R': '0',
                                                '最高溫度': '0', '高溫時間': '0', '最低溫度': '0', '低溫時間': '0', 
                                                'PM2_5': '0', 'PM2_5T': '0', '紫外線': '0', '紫外線T': '0', 
                                                }
                    #date_list[counter] = str( date_list[counter])
            break
    

    #計算 每日 的 ROOM各項數值 總平均( 放在 chart_每日平均 )
    for i in room_data_list['date_data']:
        for counter in range(8):
            if i == date_list[counter]:
                max_temp_room = 0
                min_temp_room = 999
                tempe_room = 0

                max_humid_room = 0
                min_humid_room = 999
                humid_room = 0

                max_pm25_room = 0
                min_pm25_room = 999
                pm25_room = 0

                max_co2_room = 0
                min_co2_room = 0
                co2_room = 0

                max_tvoc_room = 0
                min_tvoc_room = 999
                tvoc_room = 0

                count =0
                for item in room_data_list['date_data'][i]:
                    if int(room_data_list['date_data'][i][item]['arduino_room']['溫度']) >= max_temp_room: max_temp_room= int(room_data_list['date_data'][i][item]['arduino_room']['溫度'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['溫度']) <= min_temp_room: min_temp_room= int(room_data_list['date_data'][i][item]['arduino_room']['溫度'])
                    tempe_room+= int(room_data_list['date_data'][i][item]['arduino_room']['溫度'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['濕度']) >= max_humid_room: max_humid_room= int(room_data_list['date_data'][i][item]['arduino_room']['濕度'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['濕度']) <= min_humid_room: min_humid_room= int(room_data_list['date_data'][i][item]['arduino_room']['濕度'])
                    humid_room+= int(room_data_list['date_data'][i][item]['arduino_room']['濕度'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['pm2_5']) >= max_pm25_room: max_pm25_room= int(room_data_list['date_data'][i][item]['arduino_room']['pm2_5'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['pm2_5']) <= min_pm25_room: min_pm25_room= int(room_data_list['date_data'][i][item]['arduino_room']['pm2_5'])
                    pm25_room+= int(room_data_list['date_data'][i][item]['arduino_room']['pm2_5'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['co2']) >= max_co2_room: max_co2_room= int(room_data_list['date_data'][i][item]['arduino_room']['co2'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['co2']) <= min_co2_room: min_co2_room= int(room_data_list['date_data'][i][item]['arduino_room']['co2'])
                    co2_room+= int(room_data_list['date_data'][i][item]['arduino_room']['co2'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['tvoc']) >= max_tvoc_room: max_tvoc_room= int(room_data_list['date_data'][i][item]['arduino_room']['tvoc'])
                    if int(room_data_list['date_data'][i][item]['arduino_room']['tvoc']) <= min_tvoc_room: min_tvoc_room= int(room_data_list['date_data'][i][item]['arduino_room']['tvoc'])
                    tvoc_room+= int(room_data_list['date_data'][i][item]['arduino_room']['tvoc'])
                    count+= 1
                everyday_Room_average[counter]={'溫度': str(round(tempe_room/count)), '濕度': str(round(humid_room/count)), 'pm2_5': str(round(pm25_room/count)), 'co2': str(round(co2_room/count)), 'tvoc': str(round(tvoc_room/count))}
                everyday_Room_hi[counter]={'溫度': str(max_temp_room), '濕度': str(max_humid_room), 'pm2_5': str(max_pm25_room), 'co2': str(max_co2_room), 'tvoc': str(max_tvoc_room)}
                everyday_Room_lo[counter]={'溫度': str(min_temp_room), '濕度': str(min_humid_room), 'pm2_5': str(min_pm25_room), 'co2': str(min_co2_room), 'tvoc': str(min_tvoc_room)}

    #計算 每日 的 local各項數值 總平均( 放在 chart_每日平均 )
    #print(weather_data_list)
    for i in weather_data_list['date_data']:
        for counter in range(8):
            if i == date_list[counter]:
                #風向
                wind_come = 0
                
                wind_speed_local = 0

                max_temp_local = 0
                min_temp_local = 999
                tempe_local = 0

                max_humid_local = 0
                min_humid_local = 999
                humid_local = 0

                max_rain24_local = 0
                min_rain24_local = 999
                rain24_local = 0

                max_pm25_local = 0
                min_pm25_local = 999
                pm25_local = 0

                max_uvi_local = 0
                min_uvi_local = 999
                uvi_local = 0

                count =0

                for item in weather_data_list['date_data'][i]:
                    for type in weather_data_list['date_data'][i][item]['weather_now']:
                        if weather_data_list['date_data'][i][item]['weather_now'][type] == "":
                            weather_data_list['date_data'][i][item]['weather_now'][type] = 0

                for item in weather_data_list['date_data'][i]:
                    #風速、風向無最大最小，只有平均
                    wind_come+=int(float(weather_data_list['date_data'][i][item]['weather_now']['風向']))

                    wind_speed_local+= int(float(weather_data_list['date_data'][i][item]['weather_now']['風速']))

                    weather_data_list['date_data'][i][item]['weather_now']['氣溫'] = float(weather_data_list['date_data'][i][item]['weather_now']['氣溫'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['氣溫']) >= max_temp_local: max_temp_local= int(weather_data_list['date_data'][i][item]['weather_now']['氣溫'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['氣溫']) <= min_temp_local: min_temp_local= int(weather_data_list['date_data'][i][item]['weather_now']['氣溫'])
                    tempe_local+= int(weather_data_list['date_data'][i][item]['weather_now']['氣溫'])

                    if float(weather_data_list['date_data'][i][item]['weather_now']['濕度']) < 1 :
                        weather_data_list['date_data'][i][item]['weather_now']['濕度'] = float(weather_data_list['date_data'][i][item]['weather_now']['濕度']) 
                        weather_data_list['date_data'][i][item]['weather_now']['濕度'] *= 100
                    else:
                        weather_data_list['date_data'][i][item]['weather_now']['濕度'] = float(weather_data_list['date_data'][i][item]['weather_now']['濕度']) 
                    if int(weather_data_list['date_data'][i][item]['weather_now']['濕度']) >= max_humid_local: max_humid_local= int(weather_data_list['date_data'][i][item]['weather_now']['濕度'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['濕度']) <= min_humid_local: min_humid_local= int(weather_data_list['date_data'][i][item]['weather_now']['濕度'])
                    humid_local+= int(weather_data_list['date_data'][i][item]['weather_now']['濕度'])

                    weather_data_list['date_data'][i][item]['weather_now']['H_24R'] = float(weather_data_list['date_data'][i][item]['weather_now']['H_24R'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['H_24R']) >= max_rain24_local: max_rain24_local= int(weather_data_list['date_data'][i][item]['weather_now']['H_24R'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['H_24R']) <= min_rain24_local: min_rain24_local= int(weather_data_list['date_data'][i][item]['weather_now']['H_24R'])
                    rain24_local+= int(weather_data_list['date_data'][i][item]['weather_now']['H_24R'])

                    weather_data_list['date_data'][i][item]['weather_now']['PM2_5'] = float(weather_data_list['date_data'][i][item]['weather_now']['PM2_5'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['PM2_5']) >= max_pm25_local: max_pm25_local= int(weather_data_list['date_data'][i][item]['weather_now']['PM2_5'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['PM2_5']) <= min_pm25_local: min_pm25_local= int(weather_data_list['date_data'][i][item]['weather_now']['PM2_5'])
                    pm25_local+= int(weather_data_list['date_data'][i][item]['weather_now']['PM2_5'])

                    weather_data_list['date_data'][i][item]['weather_now']['紫外線'] = float(weather_data_list['date_data'][i][item]['weather_now']['紫外線'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['紫外線']) >= max_uvi_local: max_uvi_local= int(weather_data_list['date_data'][i][item]['weather_now']['紫外線'])
                    if int(weather_data_list['date_data'][i][item]['weather_now']['紫外線']) <= min_uvi_local: min_uvi_local= int(weather_data_list['date_data'][i][item]['weather_now']['紫外線'])
                    uvi_local+= int(weather_data_list['date_data'][i][item]['weather_now']['紫外線'])

                    count+= 1
                
                everyday_local_average[counter]={'風向': str(round(wind_come/count)),'風速': str(round(wind_speed_local/count)),'氣溫': str(round(tempe_local/count)),'濕度': str(round(humid_local/count)),'H_24R': str(round(rain24_local/count)),'PM2_5': str(round(pm25_local/count)),'紫外線': str(round(uvi_local/count))}
                everyday_local_hi[counter]={'氣溫': str(max_temp_local),'濕度': str(max_humid_local),'H_24R': str(max_rain24_local),'PM2_5': str(max_pm25_local),'紫外線': str(max_uvi_local)}
                everyday_local_lo[counter]={'氣溫': str(min_temp_local),'濕度': str(min_humid_local),'H_24R': str(min_rain24_local),'PM2_5': str(min_pm25_local),'紫外線': str(min_uvi_local)}


    for counter in range(8):
        if counter not in everyday_Room_average:
            everyday_Room_average[counter]={'溫度': '0', '濕度': '0', 'pm2_5': '0', 'co2': '0', 'tvoc': '0'}
            everyday_Room_hi[counter]={'溫度': '0', '濕度': '0', 'pm2_5': '0', 'co2': '0', 'tvoc': '0'}
            everyday_Room_lo[counter]={'溫度': '0', '濕度': '0', 'pm2_5': '0', 'co2': '0', 'tvoc': '0'}

        if counter not in everyday_local_average:
            everyday_local_average[counter]={'風向': '0' ,'風速': '0' ,'氣溫': '0' ,'濕度': '0' ,'H_24R': '0' ,'PM2_5': '0' ,'紫外線': '0' }
            everyday_local_hi[counter]={'風速': '0','氣溫': '0' , '濕度': '0' ,'H_24R': '0' ,'PM2_5': '0' ,'紫外線': '0' }
            everyday_local_lo[counter]={'風速': '0','氣溫': '0' , '濕度': '0' ,'H_24R': '0' ,'PM2_5': '0' ,'紫外線': '0' }
    #print("everyday_Room_average ===",everyday_Room_average)
    #print("everyday_Room_hi ===",everyday_Room_hi)
    #print("everyday_local_lo == ",everyday_local_lo)
    date_list[0]="本日"

    #這邊因為要配合chart的資料顯示順序，因此需要reversed
    date_list = list(reversed(date_list))

    #print(now_time_Roomdata)
    #print(date_list)
    #放入今天 天氣資料
    for i in future_now_data['天氣現象']:
        weather_time_level -= 1
        today_total_temp.append(future_now_data['溫度'][i])
        if weather_time_level==0:
            weather_now_level['天氣現象'] = future_now_data['天氣現象'][i]
            weather_now_level['舒適度'] = future_now_data['舒適度'][i]
            weather_now_level['降雨機率'] = future_now_data['降雨機率'][i]
        if weather_time_level<=0:
            predict_future_weather_data['天氣現象'] = future_now_data['天氣現象'][i]
            predict_future_weather_data['溫度'] = future_now_data['溫度'][i]
            predict_future_weather_data['濕度'] = future_now_data['濕度'][i]
            predict_future_weather_data['舒適度'] = future_now_data['舒適度'][i]
            predict_future_weather_data['降雨機率'] = future_now_data['降雨機率'][i]
            
            if '晴' in future_now_data['天氣現象'][i]:
                predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/sun.png'
            elif '雷' in future_now_data['天氣現象'][i]:
                predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/thunder.png'
            elif '雨' in future_now_data['天氣現象'][i]:
                predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/rain.png'
            elif '陰' or '雲' in future_now_data['天氣現象'][i]:
                predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/cloud.png'
            else:
                predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/cute.png'
            
            weather_predict_future['今日'+i] = predict_future_weather_data
            predict_future_weather_data={}
    
    #放入明天 天氣資料
    for i in future_tomorrow_data['天氣現象']:
        tomorrow_total_temp.append(future_tomorrow_data['溫度'][i])
        predict_future_weather_data['天氣現象'] = future_tomorrow_data['天氣現象'][i]
        predict_future_weather_data['溫度'] = future_tomorrow_data['溫度'][i]
        predict_future_weather_data['濕度'] = future_tomorrow_data['濕度'][i]
        predict_future_weather_data['舒適度'] = future_tomorrow_data['舒適度'][i]
        predict_future_weather_data['降雨機率'] = future_tomorrow_data['降雨機率'][i]
        if '晴' in future_tomorrow_data['天氣現象'][i]:
            predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/sun.png'
        elif '雷' in future_tomorrow_data['天氣現象'][i]:
            predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/thunder.png'
        elif '雨' in future_tomorrow_data['天氣現象'][i]:
            predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/rain.png'
        elif '陰' or '雲' in future_tomorrow_data['天氣現象'][i]:
            predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/cloud.png'
        else:
            predict_future_weather_data['天氣圖案'] = '../static/images/logo_icon/weather/cute.png'

        weather_predict_future['明日'+i] = predict_future_weather_data
        predict_future_weather_data={}

    today_total_temp_min = min(today_total_temp)
    today_total_temp_max = max(today_total_temp)
    tomorrow_total_temp_min = min(tomorrow_total_temp)
    tomorrow_total_temp_max = max(tomorrow_total_temp)

    #print("local_data", local_data )
    #print("room_data", room_data )


    #print(weather_now_level)
    #print(weather_predict_future)
    #print(room_data_list)
    #print("now_time_Roomdata === ", now_time_Roomdata )    
    #這邊在搞 天氣預測 的大圖片
    def select_weather_background(weather_keyword):
        if int(now_time)//3+1 >= 6:
            time_keyword = 1 #晚上
        elif int(now_time)//3+1 <= 2:
            time_keyword = 1 #晚上
        else:
            time_keyword = 0 #白天
        if '晴' in weather_keyword:
            return 10+time_keyword
        if '雨' in weather_keyword:
            return 20+time_keyword
        if '陰' or '雲' in weather_keyword:
            return 30+time_keyword
        return 40+time_keyword

    #酷熱指數表
    out_danger_tab = api_for_view.the_hot_danger_tab(local_data['weather_now']['濕度'],local_data['weather_now']['氣溫'])
    in_danger_tab= api_for_view.the_hot_danger_tab(room_data['arduino_room']['濕度'],room_data['arduino_room']['溫度'])
    #print(danger_tab)

    #懸浮微粒濃度
    out_pm25_concentration = api_for_view.the_pm25_concentration(local_data['weather_now']['PM2_5'])
    in_pm25_concentration = api_for_view.the_pm25_concentration(room_data['arduino_room']['pm2_5'])

    #co2濃度
    in_co2_inside = api_for_view.the_co2_inside(room_data['arduino_room']['co2'])
    #紫外線量
    out_uv_outside = api_for_view.the_uv_outside(local_data['weather_now']['紫外線'])
    #有害廢氣
    in_tvoc_inside = api_for_view.the_tvoc_inside(room_data['arduino_room']['tvoc'])


    weather_bg = select_weather_background(weather_now_level['天氣現象'])
    print("weather_bg =", weather_bg)
    return render(request, "index.html", {
        "local_data": local_data , 
        "User_name": User_name , 
        "room_data": room_data , 
        "weather_level" : weather_now_level ,
        "天氣圖": weather_bg ,
        "weather_predict_future": weather_predict_future,
        "today_total_temp_min": today_total_temp_min,
        "today_total_temp_max": today_total_temp_max,
        "tomorrow_total_temp_min": tomorrow_total_temp_min,
        "tomorrow_total_temp_max": tomorrow_total_temp_max,
        "now_time":now_time,
        "date_list": date_list,
        "now_time_Roomdata": now_time_Roomdata,
        "everyday_Room_average": everyday_Room_average,
        "everyday_Room_hi": everyday_Room_hi,
        "everyday_Room_lo": everyday_Room_lo,
        "now_time_localdata": now_time_localdata,
        "everyday_local_average": everyday_local_average,
        "everyday_local_hi": everyday_local_hi,
        "everyday_local_lo": everyday_local_lo,
        "out_danger_tab": out_danger_tab,
        "in_danger_tab" : in_danger_tab,
        "out_pm25_concentration": out_pm25_concentration,
        "in_pm25_concentration": in_pm25_concentration,
        "in_co2_inside": in_co2_inside,
        "out_uv_outside": out_uv_outside,
        "in_tvoc_inside": in_tvoc_inside
    } )


#-------------------------------------------------------------------------------------------------------for weather now/future
#抓取 中央氣象局的 未來 需要選出 城市 然後是 區名稱 才有 未來天氣環境 網路資料
def weather_future_by_web(request):
    data = api_for_view.weather_api_future_from_web(city_name,Localname)
    #存進 資料庫
    models.insert_future_data( User_name , Localname , api_for_view.future_weather_data_pre['日期'],
    api_for_view.future_weather_data_pre['天氣現象']['00到03'],api_for_view.future_weather_data_pre['天氣現象']['03到06'],api_for_view.future_weather_data_pre['天氣現象']['06到09'],api_for_view.future_weather_data_pre['天氣現象']['09到12'],
    api_for_view.future_weather_data_pre['天氣現象']['12到15'],api_for_view.future_weather_data_pre['天氣現象']['15到18'],api_for_view.future_weather_data_pre['天氣現象']['18到21'],api_for_view.future_weather_data_pre['天氣現象']['21到24'],
    api_for_view.future_weather_data_pre['溫度']['00到03'],api_for_view.future_weather_data_pre['溫度']['03到06'],api_for_view.future_weather_data_pre['溫度']['06到09'],api_for_view.future_weather_data_pre['溫度']['09到12'],
    api_for_view.future_weather_data_pre['溫度']['12到15'],api_for_view.future_weather_data_pre['溫度']['15到18'],api_for_view.future_weather_data_pre['溫度']['18到21'],api_for_view.future_weather_data_pre['溫度']['21到24'],
    api_for_view.future_weather_data_pre['濕度']['00到03'],api_for_view.future_weather_data_pre['濕度']['03到06'],api_for_view.future_weather_data_pre['濕度']['06到09'],api_for_view.future_weather_data_pre['濕度']['09到12'],
    api_for_view.future_weather_data_pre['濕度']['12到15'],api_for_view.future_weather_data_pre['濕度']['15到18'],api_for_view.future_weather_data_pre['濕度']['18到21'],api_for_view.future_weather_data_pre['濕度']['21到24'],
    api_for_view.future_weather_data_pre['舒適度']['00到03'],api_for_view.future_weather_data_pre['舒適度']['03到06'],api_for_view.future_weather_data_pre['舒適度']['06到09'],api_for_view.future_weather_data_pre['舒適度']['09到12'],
    api_for_view.future_weather_data_pre['舒適度']['12到15'],api_for_view.future_weather_data_pre['舒適度']['15到18'],api_for_view.future_weather_data_pre['舒適度']['18到21'],api_for_view.future_weather_data_pre['舒適度']['21到24'],
    api_for_view.future_weather_data_pre['降雨機率']['00到03'],api_for_view.future_weather_data_pre['降雨機率']['03到06'],api_for_view.future_weather_data_pre['降雨機率']['06到09'],api_for_view.future_weather_data_pre['降雨機率']['09到12'],
    api_for_view.future_weather_data_pre['降雨機率']['12到15'],api_for_view.future_weather_data_pre['降雨機率']['15到18'],api_for_view.future_weather_data_pre['降雨機率']['18到21'],api_for_view.future_weather_data_pre['降雨機率']['21到24'],
    )
    models.future_oldest_data_del()
    models.del_old_local_data()
    print("明天天氣: ",data)
    return HttpResponse("future is good")

#抓取中央氣象局的 目前天氣環境 網路資料
def weather_now_by_web(request):
    api_for_view.weather_api_now_from_web(Localname)
    try:
        api_for_view.PM25_api_now_from_web(Localname)
    except:
        print("PM25 Request timeout!!!!!!!!!!!!")
    try:
        api_for_view.UVI_api_now_from_web(county_name)
    except:
        print("UVI Request timeout!!!!!!!!!!!!")
    #存進 資料庫
    models.insert_local_data( User_name, Localname, api_for_view.weather_data_now_cont['日期'], 
    api_for_view.weather_data_now_cont['時間'], api_for_view.weather_data_now_cont['風向'], api_for_view.weather_data_now_cont['風速'], 
    api_for_view.weather_data_now_cont['氣溫'], api_for_view.weather_data_now_cont['濕度'], api_for_view.weather_data_now_cont['H_24R'],
    api_for_view.weather_data_now_cont['最高溫度'], api_for_view.weather_data_now_cont['高溫時間'], api_for_view.weather_data_now_cont['最低溫度'], 
    api_for_view.weather_data_now_cont['低溫時間'], api_for_view.weather_data_now_cont["PM2_5"], api_for_view.weather_data_now_cont['PM2_5T'],
    api_for_view.weather_data_now_cont['紫外線'],  api_for_view.weather_data_now_cont['紫外線T'] )
    print(api_for_view.weather_data_now_cont)
    return HttpResponse("now is good")
#----------------------------------------------------------------------------------------------------------

#   https://arduino-web-eggplant.herokuapp.com        http://127.0.0.1:8000/

#令arduino把資料直接 get 到伺服器 http://127.0.0.1:8000/data_get_test_by_get/?Date=08-15&Time=17:24&Temperature=24&Humandity=43&PM25=1&Co2=406&TVOC=1
def data_get_test_by_get(request):
    print("Get Ip From ----> "+request.META['REMOTE_ADDR'] )
    data_date = request.GET['Date']
    datatime = request.GET['Time']
    temperature = request.GET['Temperature']
    humandity = request.GET['Humandity']
    pm25 = request.GET['PM25']
    co2 = request.GET['Co2']
    tvoc = request.GET['TVOC']
    if temperature == 0 and humandity == 0 and pm25 == 0 and co2 == 0 and tvoc ==0 :
        return HttpResponse('get data not OK')
    #利用arduino定時功能來觸發另外兩個api
    try:
        weather_now_by_web(request)
    except:
        print("get weather_data timeout!!!!!!!!!!!!")
    #查看時間是否需要call明天天氣api
    tomorrow_time_api = datetime.datetime.now().strftime("%H:%M")
    if tomorrow_time_api == "00:20":
        weather_future_by_web(request)
    #這邊使用arduino傳過來的時間為標準，如果以伺服器為標準 時間 會有問題
    #data_time = time.strftime("%H:%M", t)
    #alist = request.GET.getlist('a')
    print("Server got this: \n" +" Date = "+ data_date +" time = "+ datatime + "\n Temperature = " + temperature + "\n Humandity = " + humandity + "\n PM2.5 = " + pm25 + "\n Co2 = " + co2 + "\n TVOC = " + tvoc)
    models.insert_room_data(User_name,data_date,datatime,temperature,humandity,pm25,co2,tvoc)
    return HttpResponse('get data OK')

#令arduino把資料直接 post 到伺服器 https://arduino-web-eggplant.herokuapp.com/data_get_test_by_post/
def data_get_test_by_post(request):
    print(request.POST['txt'])
    return HttpResponse('post data OK')  

#把JSON資料丟到某網頁，再由伺服器去抓 http://127.0.0.1:8000/data_get_test_by_html
def data_get_test_by_html(request): 
    response = requests.get("https://arduino-web-eggplant.herokuapp.com/data_put_test/")
    response.encoding="UTF-8"
    json_data = eval(response.text)
    print(json_data)
    print(json_data['name'])
    print(json_data['age'])
    return HttpResponse('html data OK')

# 接收POST请求数据
def search_post(request):
	if request.POST:
		data = request.POST['post_data']
	return HttpResponse('this is '+data)

#-------------------------------------------------------------------------------------------------------for Line_Bot
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
Line_cmd = ["房間資訊","更新天氣","天氣資訊","明天天氣","網站","指令查詢"]

def line_bot(request):
#例如: data = [{'name': '夏茄子', 'location': '安南'}]   格式 為 list包裹dic，print( data[0]['name'] ) 可取出資料
    if request.method == 'POST':


        room_data=models.find_room_last()
        local_data=models.find_local_last()


        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                user_id = event.source.user_id
                profile = line_bot_api.get_profile(user_id) 
                some_one = profile.display_name
                some_one_say = event.message.text
                print("Master "+some_one+" 說--> "+ some_one_say)
                
                if some_one_say == "房間資訊":
                    user_local_str = ( "Master" + room_data['User_name'] + " ( ◐‿◑ ) " )
                    user_arduino_str = ( "\n" + "房內資訊 :" 
                    + "\n" + "_______________"
                    + "\n" + "氣溫: " +room_data['arduino_room']["溫度"] + " 度"
                    + "\n" + "---------------"
                    + "\n" + "濕度: " +room_data['arduino_room']["濕度"] + " %"
                    + "\n" + "---------------"
                    + "\n" + "PM2_5: " +room_data['arduino_room']["pm2_5"] + " ug/m3"
                    + "\n" + "---------------"
                    + "\n" + "二氧化碳: " +room_data['arduino_room']["co2"] + " ppm"
                    + "\n" + "---------------"
                    + "\n" + "有毒氣體: " +room_data['arduino_room']["tvoc"] + " ppb" 
                    + "\n" + "_______________"
                    + "\n" + "資料時間: " +room_data['date'] +" "+room_data['time'] )
                    replay_str = user_local_str + user_arduino_str
                    
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=replay_str) )
                #------------------------------------------------------------------------------------
                if some_one_say == "更新天氣":


                    weather_now_by_web(request)


                    replay_str = "Master" + some_one + "大人 ˙>˙  \n您的資料已更新......"
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=replay_str) )

                if some_one_say == "天氣資訊":
                    user_weather_str_head = ( local_data['Localname'] + "的 Master " + local_data['User_name'] )
                    user_weather_str = ( "\n" + "您的 環境資訊 _(:_」∠)_ " 
                    + "\n" + "_______________"
                    + "\n" + "風向: " +local_data['weather_now']["風向"] + " 度"
                    + "\n" + "---------------"
                    + "\n" + "風速: " +local_data['weather_now']["風速"] + " m/s"
                    + "\n" + "---------------"
                    + "\n" + "氣溫: " +local_data['weather_now']["氣溫"] + " 度"
                    + "\n" + "---------------"
                    + "\n" + "濕度: " +local_data['weather_now']["濕度"] + " %"
                    + "\n" + "---------------"
                    + "\n" + "H_24R: " +local_data['weather_now']["H_24R"] + " mm" 
                    + "\n" + "---------------"
                    + "\n" + "最高溫度: " +local_data['weather_now']["最高溫度"] + " 度"
                    + "\n" + "---------------"
                    + "\n" + "高溫時間: " +local_data['weather_now']["高溫時間"]
                    + "\n" + "---------------"
                    + "\n" + "最低溫度: " +local_data['weather_now']["最低溫度"] + " 度"
                    + "\n" + "---------------"
                    + "\n" + "低溫時間: " +local_data['weather_now']["低溫時間"] 
                    + "\n" + "---------------"
                    + "\n" + "PM2.5: " +local_data['weather_now']["PM2_5"] + " ug/m3"
                    + "\n" + "---------------"
                    + "\n" + "PM2.5T: " +local_data['weather_now']["PM2_5T"] 
                    + "\n" + "---------------"
                    + "\n" + "紫外線: " +local_data['weather_now']["紫外線"] + " uvi"
                    + "\n" + "---------------"
                    + "\n" + "紫外線T: " +local_data['weather_now']["紫外線T"] 
                    + "\n" + "_______________"
                    + "\n" + "資料時間: " +local_data['日期'] +" "+ local_data['時間']
                    )
                    replay_str = user_weather_str_head + user_weather_str
                    
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=replay_str) )
                #-------------------------------------------------------------------------------
                if some_one_say == "明天天氣":

                    weather_future_by_web(request)
                    futures_data = models.find_future_last()
                    user_future_str_head = ( "Master" + some_one + "大人 ,明天預測..... \n"+ futures_data['日期'])
                    user_future_str = ( "\n" + " ´･ω･` " 
                    + "\n" + "_______________"
                    + "\n" + "00到03點:  " +futures_data['天氣現象']["00到03"] 
                    + "\n" + "---------------"
                    + "\n" + "03到06點:  " +futures_data['天氣現象']["03到06"] 
                    + "\n" + "---------------"
                    + "\n" + "06到09點:  " +futures_data['天氣現象']["06到09"] 
                    + "\n" + "---------------"
                    + "\n" + "09到12點:  " +futures_data['天氣現象']["09到12"] 
                    + "\n" + "---------------"
                    + "\n" + "12到15點:  " +futures_data['天氣現象']["12到15"]
                    + "\n" + "---------------"
                    + "\n" + "15到18點:  " +futures_data['天氣現象']["15到18"] 
                    + "\n" + "---------------"
                    + "\n" + "18到21點:  " +futures_data['天氣現象']["18到21"] 
                    + "\n" + "---------------"
                    + "\n" + "21到24點:  " +futures_data['天氣現象']["21到24"] 
                    + "\n" + "_______________" )
                    replay_str = user_future_str_head + user_future_str
                    
                    

                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=replay_str) )
                if some_one_say == "網站":
                    user_str_head = ( "Master" + some_one + "大人 * > * \n以下是您的網站......\n" )
                    replay_str = user_str_head+"https://arduino-web-eggplant.herokuapp.com/main"
                    
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=replay_str) )
                #-------------------------------------------------------------------------------
                if some_one_say == "指令查詢":
                    user_str_head = ( "Master" + some_one + "大人 ˙>˙  \n歡迎您使用以下指令......\n" )
                    user_str = ""
                    for i in Line_cmd:
                        user_str += i + "\n"
                    replay_str = user_str_head + user_str
                    
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=replay_str) )

                #-------------------------------------------------------------------------------
                if some_one_say not in Line_cmd :
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text="朕 知道了，汝 何不試試 指令查詢? ") )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
