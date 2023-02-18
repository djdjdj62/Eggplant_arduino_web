from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from trips import models
import datetime
import requests
import json
import time
from bs4 import BeautifulSoup

weather_data_now_cont = {
        "日期" : "",
        "時間" : "",
        "風向" : "",
        "風速" : "",
        "氣溫" : "",
        "濕度" : "",
        "H_24R" : "",
        "最高溫度" : "",
        "高溫時間" : "",
        "最低溫度" : "",
        "低溫時間" : "",
        "PM2_5"  : "",
        "PM2_5T": "",
        "紫外線" : "",
        "紫外線T": ""
    }

#___________________________目前 天氣環境 查詢___________________________________________________________
def weather_api_now_from_web(local_name):
    api_for_weather_observation = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-8521776A-F32C-441F-AA12-F9DF23DFCE45&locationName="
    api_for_weather_observation += local_name
    response = requests.get(api_for_weather_observation)
    data_json = response.json()
    data_json = data_json['records']
    timeString = data_json['location'][0]['time']['obsTime']
    #資料時間處理
    struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M:%S" )
    timeString = time.strftime("%m-%d %H:%M", struct_time)
    print("取得 綜合資料 的時間: " + timeString) 
    timeString = timeString.split(" ")
    DateString = timeString[0]
    TimeString = timeString[1]
    
    weather_data = {
        "高溫時間" : data_json['location'][0]['weatherElement'][11]['elementValue'],
        "低溫時間" : data_json['location'][0]['weatherElement'][13]['elementValue'],
    }

    weather_data['高溫時間'] = weather_data['高溫時間'][11:]
    weather_data['高溫時間'] = weather_data['高溫時間'][:5]
    weather_data['低溫時間'] = weather_data['低溫時間'][11:]
    weather_data['低溫時間'] = weather_data['低溫時間'][:5]

    weather_data_now_cont["日期"] = DateString
    weather_data_now_cont["時間"] = TimeString
    weather_data_now_cont["風向"] = data_json['location'][0]['weatherElement'][1]['elementValue']
    weather_data_now_cont["風速"] = data_json['location'][0]['weatherElement'][2]['elementValue']
    weather_data_now_cont["氣溫"] = data_json['location'][0]['weatherElement'][3]['elementValue']
    weather_data_now_cont["濕度"] = str(float(data_json['location'][0]['weatherElement'][4]['elementValue'])*100)
    weather_data_now_cont["H_24R"] = data_json['location'][0]['weatherElement'][6]['elementValue']
    weather_data_now_cont["最高溫度"] = data_json['location'][0]['weatherElement'][10]['elementValue']
    weather_data_now_cont["高溫時間"] = weather_data['高溫時間']
    weather_data_now_cont["最低溫度"] = data_json['location'][0]['weatherElement'][12]['elementValue']
    weather_data_now_cont["低溫時間"] = weather_data['低溫時間']
    #print(weather_data)

#-------------------------
#API_參考: https://drive.google.com/file/d/13kPG4SJ_4IQI2mVBK_-i422U41BUb-d5/view

# PM2.5   測站名 = local_name
# https://data.epa.gov.tw/dataset/detail/AQX_P_02
def PM25_api_now_from_web(local_name):
    api_for_pm25_observation = "https://data.epa.gov.tw/api/v2/AQX_P_02?format=json&offset=0&limit=100&api_key=19339998-14cc-4ce6-873e-2821e803f17c"
    response = requests.get(api_for_pm25_observation)
    pm25_json = response.json()
    pm25_json = pm25_json['records']
    for i in pm25_json:
        if i['site'] == local_name:
            pm25_data = i['pm25']
            pm25_data_time = i['datacreationdate']

    print("PM2.5 = " + pm25_data , "data got time: " + pm25_data_time) 
    #資料時間處理
    struct_time = time.strptime(pm25_data_time, "%Y-%m-%d %H:%M" )
    timeString = time.strftime("%m-%d %H:%M", struct_time)
    print("PM2.5取得的時間: " + timeString) 
    timeString = timeString.split(" ")
    TimeString = timeString[1]
    weather_data_now_cont["PM2_5"] = pm25_data
    weather_data_now_cont["PM2_5T"] = TimeString
      

# UVI   測站名 = city_name
# https://data.epa.gov.tw/dataset/detail/UV_S_01
def UVI_api_now_from_web(county_name): #臺南市
    api_for_uvi_observation = "https://data.epa.gov.tw/api/v2/UV_S_01?format=json&offset=0&limit=100&api_key=19339998-14cc-4ce6-873e-2821e803f17c"
    response = requests.get(api_for_uvi_observation)
    uvi_json = response.json()
    uvi_json = uvi_json['records']
    for i in uvi_json:
        if i['county'] == county_name:
            uvi_data = i['uvi']
            uvi_data_time = i['publishtime']
            break   #這個天才api會把目前全部測站的內容給你看，所以只取出最近/新的一筆

    print("UVI = " + uvi_data , "data got time: " + uvi_data_time)
    #資料時間處理
    struct_time = time.strptime(uvi_data_time, "%Y-%m-%d %H:%M" )
    timeString = time.strftime("%m-%d %H:%M", struct_time)
    print("UVI取得的時間: " + timeString) 
    timeString = timeString.split(" ")
    TimeString = timeString[1]
    weather_data_now_cont["紫外線"] = uvi_data
    weather_data_now_cont["紫外線T"] = TimeString


#_________________未來 天氣 預測____________________________________________________________________

future_weather_data_pre = {
    "日期" : "",
    "天氣現象" : {
        "00到03" : "",
        "03到06" : "",
        "06到09" : "",
        "09到12" : "",
        "12到15" : "",
        "15到18" : "",
        "18到21" : "",
        "21到24" : ""
    },
    "溫度" : {
        "00到03" : "",
        "03到06" : "",
        "06到09" : "",
        "09到12" : "",
        "12到15" : "",
        "15到18" : "",
        "18到21" : "",
        "21到24" : ""
    },
    "濕度" : {
        "00到03" : "",
        "03到06" : "",
        "06到09" : "",
        "09到12" : "",
        "12到15" : "",
        "15到18" : "",
        "18到21" : "",
        "21到24" : ""
    },
    "舒適度" : {
        "00到03" : "",
        "03到06" : "",
        "06到09" : "",
        "09到12" : "",
        "12到15" : "",
        "15到18" : "",
        "18到21" : "",
        "21到24" : ""
    },
    "降雨機率" : {
        "00到03" : "",
        "03到06" : "",
        "06到09" : "",
        "09到12" : "",
        "12到15" : "",
        "15到18" : "",
        "18到21" : "",
        "21到24" : ""
    }
}

def weather_api_future_from_web(city_name,Localname):
    #https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization=CWB-8521776A-F32C-441F-AA12-F9DF23DFCE45&format=JSON&locationId=F-D0047-077&sort=time&timeFrom=2022-06-28T00%3A00%3A00&timeTo=2022-06-29T00%3A00%3A00
    api_for_future_weather = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization=CWB-8521776A-F32C-441F-AA12-F9DF23DFCE45&format=JSON&locationId=F-D0047-077&sort=time&timeFrom="
    future_start_time_ = "T00%3A00%3A00&timeTo="
    future_end_time_ = "T00%3A00%3A00"
    
    #"2022-06-28"
    print(datetime.datetime.now())

    now =datetime.datetime.now()
    tomorrow1_date = datetime.timedelta(days=1)  
    tomorrow2_date = datetime.timedelta(days=2)  
    n1_day = now +tomorrow1_date
    n2_day = now +tomorrow2_date
    print(n1_day.strftime('%Y-%m-%d'))
    print(n2_day.strftime('%Y-%m-%d'))

    #"2022-06-28"
    future_start_time = n1_day.strftime('%Y-%m-%d')
    #"2022-06-29"
    future_end_time = n2_day.strftime('%Y-%m-%d')

    future_weather_data_pre['日期'] = future_start_time

    api_for_future_weather = api_for_future_weather + future_start_time + future_start_time_ + future_end_time + future_end_time_
    print(api_for_future_weather)
    response = requests.get(api_for_future_weather)
    future_json = response.json()
    locationName_json = future_json['records']['locations'][0]['location']
    for i in locationName_json:
        if i['locationName'] == (Localname+"區"):
            Localname_json= i 
    #print(Localname_json)
    for i in Localname_json['weatherElement']:
        if i['description'] == "天氣現象":
            future_weather_data_pre['天氣現象']['00到03'] = i['time'][0]['elementValue'][0]['value']
            future_weather_data_pre['天氣現象']['03到06'] = i['time'][1]['elementValue'][0]['value']
            future_weather_data_pre['天氣現象']['06到09'] = i['time'][2]['elementValue'][0]['value']
            future_weather_data_pre['天氣現象']['09到12'] = i['time'][3]['elementValue'][0]['value']
            future_weather_data_pre['天氣現象']['12到15'] = i['time'][4]['elementValue'][0]['value']
            future_weather_data_pre['天氣現象']['15到18'] = i['time'][5]['elementValue'][0]['value']
            future_weather_data_pre['天氣現象']['18到21'] = i['time'][6]['elementValue'][0]['value']
            future_weather_data_pre['天氣現象']['21到24'] = i['time'][7]['elementValue'][0]['value']
        if i['description'] == "溫度":
            future_weather_data_pre['溫度']['00到03'] = i['time'][0]['elementValue'][0]['value']
            future_weather_data_pre['溫度']['03到06'] = i['time'][1]['elementValue'][0]['value']
            future_weather_data_pre['溫度']['06到09'] = i['time'][2]['elementValue'][0]['value']
            future_weather_data_pre['溫度']['09到12'] = i['time'][3]['elementValue'][0]['value']
            future_weather_data_pre['溫度']['12到15'] = i['time'][4]['elementValue'][0]['value']
            future_weather_data_pre['溫度']['15到18'] = i['time'][5]['elementValue'][0]['value']
            future_weather_data_pre['溫度']['18到21'] = i['time'][6]['elementValue'][0]['value']
            future_weather_data_pre['溫度']['21到24'] = i['time'][7]['elementValue'][0]['value']
        if i['description'] == "相對濕度":
            future_weather_data_pre['濕度']['00到03'] = i['time'][0]['elementValue'][0]['value']
            future_weather_data_pre['濕度']['03到06'] = i['time'][1]['elementValue'][0]['value']
            future_weather_data_pre['濕度']['06到09'] = i['time'][2]['elementValue'][0]['value']
            future_weather_data_pre['濕度']['09到12'] = i['time'][3]['elementValue'][0]['value']
            future_weather_data_pre['濕度']['12到15'] = i['time'][4]['elementValue'][0]['value']
            future_weather_data_pre['濕度']['15到18'] = i['time'][5]['elementValue'][0]['value']
            future_weather_data_pre['濕度']['18到21'] = i['time'][6]['elementValue'][0]['value']
            future_weather_data_pre['濕度']['21到24'] = i['time'][7]['elementValue'][0]['value']
        if i['description'] == "舒適度指數":
            future_weather_data_pre['舒適度']['00到03'] = i['time'][0]['elementValue'][1]['value']
            future_weather_data_pre['舒適度']['03到06'] = i['time'][1]['elementValue'][1]['value']
            future_weather_data_pre['舒適度']['06到09'] = i['time'][2]['elementValue'][1]['value']
            future_weather_data_pre['舒適度']['09到12'] = i['time'][3]['elementValue'][1]['value']
            future_weather_data_pre['舒適度']['12到15'] = i['time'][4]['elementValue'][1]['value']
            future_weather_data_pre['舒適度']['15到18'] = i['time'][5]['elementValue'][1]['value']
            future_weather_data_pre['舒適度']['18到21'] = i['time'][6]['elementValue'][1]['value']
            future_weather_data_pre['舒適度']['21到24'] = i['time'][7]['elementValue'][1]['value']
        if i['description'] == "6小時降雨機率":
            future_weather_data_pre['降雨機率']['00到03'] = i['time'][0]['elementValue'][0]['value']
            future_weather_data_pre['降雨機率']['03到06'] = i['time'][0]['elementValue'][0]['value']
            future_weather_data_pre['降雨機率']['06到09'] = i['time'][1]['elementValue'][0]['value']
            future_weather_data_pre['降雨機率']['09到12'] = i['time'][1]['elementValue'][0]['value']
            future_weather_data_pre['降雨機率']['12到15'] = i['time'][2]['elementValue'][0]['value']
            future_weather_data_pre['降雨機率']['15到18'] = i['time'][2]['elementValue'][0]['value']
            future_weather_data_pre['降雨機率']['18到21'] = i['time'][3]['elementValue'][0]['value']
            future_weather_data_pre['降雨機率']['21到24'] = i['time'][3]['elementValue'][0]['value']


    print(future_weather_data_pre)
    return future_weather_data_pre


def the_hot_danger_tab(h,t):
    #酷熱指數表 參照網站: https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=577&pid=10742
    #濕度40,45,50,55,60,65,70,75,80,85,90,95,100
    #溫度47,43,41,40,39,38,37,36,34,33,32,31,30,29,28,27
    #
    label=['地獄','危險','警戒','安全','優良']
    tab=[
        [51,54,58,99,99,99,99,99,99,99,99,99,99],
        [48,51,55,58,99,99,99,99,99,99,99,99,99],
        [46,48,51,54,58,99,99,99,99,99,99,99,99],
        [43,46,48,51,54,58,99,99,99,99,99,99,99],
        [41,43,45,47,51,53,57,99,99,99,99,99,99],
        [38,40,42,44,47,49,52,56,99,99,99,99,99],
        [36,38,39,41,43,46,48,51,54,57,99,99,99],
        [34,36,37,38,41,42,44,47,49,52,55,99,99],
        [33,34,35,36,38,39,41,43,45,47,50,53,56],
        [31,32,33,34,35,37,38,39,41,43,45,47,49],
        [29,31,31,32,33,34,35,36,38,39,41,42,44],
        [28,29,29,30,31,32,32,33,34,36,37,38,39],
        [27,28,28,29,29,29,30,31,32,32,33,34,35],
        [27,27,27,27,28,28,28,29,29,29,30,30,31]
    ]
    humid=[40,45,50,55,60,65,70,75,80,85,90,95,100]
    temp=[41,40,39,38,37,36,34,33,32,31,30,29,28,27]

    h = int(float(h))
    t = int(float(t))

    if  t > 26:
        for i in range(len(temp)):
            if t >= temp[i] :
                #t = temp[i]
                t = i
                break
        
        for i in range(len(humid)):
            if h <= humid[i]:
                #h = humid[i]
                h = i
                break

        #print("=======",h,t)
        print(tab[t][h])

        if (tab[t][h]) > 53:
            return label[0]
        if (tab[t][h]) > 41:
            return label[1]
        if (tab[t][h]) > 32:
            return label[2]
        else:
            return label[3]
    
    return label[4]

def the_pm25_concentration(d):
    #用世界衛生組織的標準 https://zh.m.wikipedia.org/zh-tw/%E6%87%B8%E6%B5%AE%E7%B2%92%E5%AD%90
    label=['地獄','危險','警戒','安全','優良']
    d = int(float(d))

    if d >= 35:
        return label[0]
    if d >= 25:
        return label[1]
    if d >= 15:
        return label[2]
    if d >= 10:
        return label[3]
    else:
        return label[4]

def the_co2_inside(d):
    #找無專業標準只有大概: 
    # https://purotechbogger.wordpress.com/air/ 
    # https://www.cyhg.gov.tw/News_Content.aspx?n=20C1A3DAF6A74FCE&sms=CA3FB4291106E1D9&s=225380F228925BBD
    # https://kknews.cc/zh-tw/health/8l85ell.html
    label=['地獄','危險','警戒','安全','優良']
    d = int(d)

    if d >= 1000:
        return label[0]
    if d >= 850:
        return label[1]
    if d >= 650:
        return label[2]
    if d >= 500:
        return label[3]
    else:
        return label[4]

def the_uv_outside(d):
    #世界衛生組織規範 https://www.cwb.gov.tw/Data/knowledge/announce/service13.pdf
    label=['地獄','危險','警戒','安全','優良']
    print("d =",d)
    if d == "":
        return "???"
    else:
        d = float(d)
        print("uv狀態 =",d)

    if d >= 11:
        return label[0]
    if d >= 8:
        return label[1]
    if d >= 6:
        return label[2]
    if d >= 3:
        return label[3]
    else:
        return label[4]

def the_tvoc_inside(d):
    #不知名規範 https://hackmd.io/4jX23J-jT9eNmbQ5A0ZrCg?view
    label=['地獄','危險','警戒','安全','優良']
    d = int(d)

    if d >= 1000:
        return label[0]
    if d >= 750:
        return label[1]
    if d >= 50:
        return label[2]
    if d >= 10:
        return label[3]
    else:
        return label[4]