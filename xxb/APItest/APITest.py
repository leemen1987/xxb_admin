# -*- coding:utf-8 -*-
import requests
import json
import datetime
import uuid
import pymysql
from sshtunnel import SSHTunnelForwarder

# server = SSHTunnelForwarder(ssh_address_or_host=('113.107.137.16', 1133), ssh_username='readonly',
#                                 ssh_password='LYPlyp123456', remote_bind_address=('127.0.0.1', 3308))
# server.start()
#
# db = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user='readonly', password='readonly',
#                      db='td_busonlinedisp845')
# print(db)
# cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
# sql = "SELECT * FROM `dh_busstatusinfoday` WHERE memo = '19177' AND DATE_FORMAT(newdate,'%Y%m%d') = '20220503'"
# cursor.execute(sql)
# data = cursor.fetchall()
# print(data, type(data[0]))
# cursor.close()
# db.close()
#
# reqid = str(uuid.uuid1())
# headers = {'Accept-Charset': 'utf-8', 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
# publicrequest = {
#     "protover": "1.0", "signdata": "", "servicecode": "00000030001", "sysid": "91182F78-B3CF-43BF-AF5B-D1E276792296",
#     "requesttime": "", "reserve": "", "servicever": "1.0", "message": "", "reqid": reqid
# }
# body = {"SysId": "91182F78-B3CF-43BF-AF5B-D1E276792296", "AccountName": "PTJ010", "Password": "mb9p2c"}
# data = {"publicrequest": publicrequest, "body": body}
# time = datetime.datetime.now().strftime("%Y%m%d%H%M%S000")
# data['publicrequest']['requesttime'] = time
# ret = requests.post('http://103.56.76.162:17007/api/ServiceGateway/DataService', headers=headers, json=data)
# jsonstr = ret.json()
# print(data)
# print(jsonstr)
# key = json.loads(jsonstr)
# print(key['body'])

# reqid2 = str(uuid.uuid1())
# headers2 = {'Accept-Charset': 'utf-8', 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8', 'token': '4d8dff46-ec5d-4961-a1e6-23de8480e28c'}
# publicrequest = {"protover":"1.0","signdata":"","servicecode":"005200100101","sysid":"91182F78-B3CF-43BF-AF5B-D1E276792296","requesttime":"","reserve":"","servicever":"1.0","reqid":reqid2}
# items = [{"CheJiaHao": "LJ16AD3C0C3004486", "QiShiLiCheng": "10", "XiaQuXian": "开平", "YeHuMingCheng": "开平市公共汽车总公司",
#           "JieShuShiJian": "14:38", "JingYingFanWei": "公共客运", "JieShuLiCheng": "20", "XiaQuShi": "江门",
#           "KaiShiYunYingRiQi": "2019-02-1", "ChePaiYanSe": "黄色", "XiaQuSheng": "广东", "YunYingRiQi": "2019-02-25",
#           "YeHuDaiMa": "J4000034", "FaDongJiHao": "FC5REC00586", "ChePaiHao": "粤J44427", "YunYingLiCheng": "50.11",
#           "JieShuYunYingRiQi": "2019-02-25", "KaiShiShiJian": "14:35"}]
# body = {"UserInfo":{"UserCode":"PTJ010","Id":""},"isreturndetailresult":True, "istransaction":True, "items":items}
# time = datetime.datetime.now().strftime("%Y%m%d%H%M%S000")
# publicrequest['requesttime'] = time
# data2 = {"publicrequest": publicrequest, "body": body}
# data3 = {"publicrequest":{"protover":"1.0","signdata":"","servicecode":"005200100101","sysid":"91182F78-B3CF-43BF-AF5B-D1E276792296","requesttime":"20190226173322368","reserve":"","servicever":"1.0","reqid":reqid2},"body":{"UserInfo":{"UserCode":"PTJ010","Id":""},"isreturndetailresult":True,"items":[{"CheJiaHao":"LJ16BV5F8A3012442","QiShiLiCheng":"10","XiaQuXian":"鹤山","YeHuMingCheng":"鹤山市鸿运公共汽车有限公司","JieShuShiJian":"14:38","JingYingFanWei":"公共客运","JieShuLiCheng":"20","XiaQuShi":"江门","KaiShiYunYingRiQi":"2019-02-1","ChePaiYanSe":"黄色","XiaQuSheng":"广东","YunYingRiQi":"2019-02-25","YeHuDaiMa":"J600014","FaDongJiHao":"J63JBA00033","ChePaiHao":"粤JX2089","YunYingLiCheng":"50.11","JieShuYunYingRiQi":"2019-02-25","KaiShiShiJian":"14:35"}],"istransaction":True}}
# print(json.dumps(data2,ensure_ascii=False,indent=2))
# # print(data2)
# ret2 = requests.post('http://103.56.76.162:17008/api/ServiceGateway/DataService', headers=headers2, json=data2)
# jsonstr = ret2.json()
# print(jsonstr)
# key = json.loads(jsonstr)
# print(key['body'])


# reqid4 = str(uuid.uuid1())
# headers4 = {'Accept-Charset': 'utf-8', 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8', 'token': '4d8dff46-ec5d-4961-a1e6-23de8480e28c'}
# publicrequest = {"protover":"1.0","signdata":"","servicecode":"005200100106","sysid":"91182F78-B3CF-43BF-AF5B-D1E276792296","requesttime":"","reserve":"","servicever":"1.0","reqid":reqid4}
# items = [
#     {"YeHuDaiMa": "J4000034",
#      "YeHuMingCheng": "开平市公共汽车总公司",
#      "ChePaiHao": "粤J44427",
#      "ChePaiYanSe": "黄色",
#      "CheJiaHao": "LJ16AD3C0C3004486",
#      "FaDongJiHao": "FC5REC00586",
#      "NianDu": 2018,
#      "JingYingFanWei": "公共客运",
#      "KaiShiYunYingRiQi": "2018-01-14",
#      "JieShuYunYingRiQi": "2018-12-25",
#      "ZongYunYingTianShu": 345,
#      "QiShiLiCheng": "450",
#      "JieShuLiCheng": "2120",
#      "ZongYunYingLiCheng": "1450.11",
#      "XiaQuSheng": "广东",
#      "XiaQuShi": "江门",
#      "XiaQuXian": "开平"},
#     {"YeHuDaiMa": "J4000034",
#      "YeHuMingCheng": "开平市公共汽车总公司",
#      "ChePaiHao": "粤J44428",
#      "ChePaiYanSe": "黄色",
#      "CheJiaHao": "LJ16AD3C0C3004486",
#      "FaDongJiHao": "FC5REC00586",
#      "NianDu": 2018,
#      "JingYingFanWei": "公共客运",
#      "KaiShiYunYingRiQi": "2018-01-14",
#      "JieShuYunYingRiQi": "2018-12-25",
#      "ZongYunYingTianShu": 345,
#      "QiShiLiCheng": "450",
#      "JieShuLiCheng": "2120",
#      "ZongYunYingLiCheng": "1450.11",
#      "XiaQuSheng": "广东",
#      "XiaQuShi": "江门",
#      "XiaQuXian": "开平"}
# ]
# body = {"UserInfo":{"UserCode":"PTJ010","Id":""},"isreturndetailresult":True, "istransaction":True, "items":items}
# time = datetime.datetime.now().strftime("%Y%m%d%H%M%S000")
# publicrequest['requesttime'] = time
# data4 = {"publicrequest": publicrequest, "body": body}
# print(json.dumps(data4,ensure_ascii=False,indent=2))
# # print(data2)
# ret2 = requests.post('http://103.56.76.162:17008/api/ServiceGateway/DataService', headers=headers4, json=data4)
# jsonstr = ret2.json()
# print(jsonstr)
# key = json.loads(jsonstr)
# print(key['body'])

# reqid3 = str(uuid.uuid1())
# headers3 = {'Accept-Charset': 'utf-8', 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8', 'token': '4d8dff46-ec5d-4961-a1e6-23de8480e28c'}
# publicrequest = {
#     "sysid": "91182F78-B3CF-43BF-AF5B-D1E276792296","reqid":reqid3,
#     "protover": "1.0","servicever": "1.0","requesttime": "","signdata": "","servicecode": "000001900002","reserve": ""
#     }
# time = datetime.datetime.now().strftime("%Y%m%d%H%M%S000")
# publicrequest['requesttime'] = time
# body = {"reqid":["8873d57e-564a-4de9-87e5-5990e07ab75e"]}
# data3 = {"publicrequest": publicrequest, "body": body}
# ret3 = requests.post('http://103.56.76.162:17008/api/ServiceGateway/DataService', headers=headers3, json=data3)
# print(json.dumps(data3, ensure_ascii=False,indent=2))
# if ret3.json():
#     jsonstr = ret3.json()
#     print(jsonstr)
# else:
#     print(ret3.text)

# text = {"body":{"isreturndetailresult":True,"items":[{"JieShuShiJian":"14:38","QiShiLiCheng":"10","KaiShiYunYingRiQi":"2018-02-1","ZongYunYingTianShu":"18","YeHuMingCheng":"开平市公共汽车总公司","ChePaiHao":"粤J44427","XiaQuShi":"江门","YeHuDaiMa":"J4000034","JingYingFanWei":"公共客运","XiaQuSheng":"广东","CheJiaHao":"LJ16AD3C0C3004486","JieShuYunYingRiQi":"2018-02-25","ChePaiYanSe":"黄色","ZongYunYingLiCheng":"18","NianDu":"2018","XiaQuXian":"开平","JieShuLiCheng":"20","YunYingLiCheng":"50.11","YunYingRiQi":"2018-02-25","FaDongJiHao":"FC5REC00586","KaiShiShiJian":"14:35"},{"JieShuShiJian":"14:38","QiShiLiCheng":"10","KaiShiYunYingRiQi":"2018-02-1","ZongYunYingTianShu":"18","YeHuMingCheng":"开平市公共汽车总公司","ChePaiHao":"粤J44428","XiaQuShi":"江门","YeHuDaiMa":"J4000034","JingYingFanWei":"公共客运","XiaQuSheng":"广东","CheJiaHao":"LJ16AD3C1C3004481","JieShuYunYingRiQi":"2018-02-25","ChePaiYanSe":"黄色","ZongYunYingLiCheng":"18","NianDu":"2018","XiaQuXian":"开平","JieShuLiCheng":"20","YunYingLiCheng":"50.11","YunYingRiQi":"2018-02-25","FaDongJiHao":"FC5REC00479","KaiShiShiJian":"14:35"}],"UserInfo":{"UserCode":"PTJ010","Id":""},"istransaction":True},"publicrequest":{"signdata":"","requesttime":"20190227162624187","protover":"1.0","servicever":"1.0","reserve":"","servicecode":"005200100106","sysid":"91182F78-B3CF-43BF-AF5B-D1E276792296","reqid":"2ee8cb41-1afa-41d2-9f58-1e31b67b32f9"}}
#
# jsontext = json.dumps(text,ensure_ascii=False,indent=2)
# print(jsontext)

# code2Session_api = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx2aa9664260efde3e&secret=ae9c8c98b11d75d077aa0aef80157fa0&grant_type=authorization_code&js_code=013yIY0w3hOlVU2yKQ2w341c7e1yIY0D'
# wx_openid = requests.get(code2Session_api)
# print(wx_openid.json())

# 获取五邑通刷卡数据
session = requests.session()
url = 'http://219.130.135.56:12011/Account/Login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400'}
data = {
    'UserName': 'kpgqhjt', 'Password': '123456', 'RememberMe': 'false'
}
data = session.post(url, headers=headers, data=data, allow_redirects=False)
cookies = data.cookies
cookies_data = requests.utils.dict_from_cookiejar(cookies)
print(cookies_data)
headers_cookies = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '161',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ASP.NET_SessionId=' + cookies_data['ASP.NET_SessionId'] + '; ' + '.ASPXAUTH=' + cookies_data['.ASPXAUTH'],
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400'
}
from_data = {
    'reprotName': '车辆综合交易汇总表',
    'merchant_id': '0005',  # 商户：开平市公共汽车总公司 0005
    'qs_date': '2022-05-01',
    'zz_date': '2022-05-31',
    'cardtype_id': ''  # 默认不填，普通卡0，学生卡1，免费长者卡2，半价长者卡3,...
}
exrport_data_url = 'http://219.130.135.56:12011/JiangmenSearch/Exreport_XF_SynthHZ_Report'
get_data = session.post(exrport_data_url, headers=headers_cookies, data=from_data, timeout=600)
print(get_data.status_code)
with open('xxx.xls', 'wb') as code:
    code.write(get_data.content)

# headers_one = {'Content-type': 'application/x-www-form-urlencoded'}
# headers = {'Content-type': 'application/json;charset=UTF-8'}
# body = {"userName": "transmitDev", "passWord": "dR3QG3gI831dFpZi"}
# # body1 = {"RoadID": ''}
# get_jsessionid = requests.post('http://113.107.137.16:58088/app/login', headers=headers_one, data=body)
# jsessionid = get_jsessionid.json()['data']
# # ret = requests.post('http://113.107.137.16:58088/app/getAppStatusInfoData;jsessionid=' + jsessionid, headers=headers, json=body1)   #站点接口
# ret = requests.post('http://113.107.137.16:58088/app/getAppStatusInfoData;jsessionid=' + jsessionid, headers=headers)  # 线路接口
# data = ret.json()
# # bus_stop = []
# # roadtype = '0'
# # if roadtype == '0':
# #     for i in data['data']:
# #         gps_info_item = {}
# #         busstate = i['BusState']
# #         roadtype_info = i['RoadType']
# #         gps_info_item['id'] = int(i['SiteId'])
# #         if busstate == '1':
# #             if roadtype_info == '0' or roadtype_info == '2':
# #                 bus_stop.append(gps_info_item)
# # if roadtype == '1':
# #     for i in data['data']:
# #         gps_info_item = {}
# #         busstate = i['BusState']
# #         roadtype_info = i['RoadType']
# #         gps_info_item['id'] = int(i['SiteId'])
# #         if busstate == '1':
# #             if roadtype_info == '1' or roadtype_info == '3':
# #                 bus_stop.append(gps_info_item)
# # print(bus_stop)
# print(json.dumps(data, ensure_ascii=False, indent=2))
