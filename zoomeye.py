import requests
import json
import re
import os
from urllib.parse import quote
from datetime import datetime, date, timedelta

mode = 2 # 两种模式 为1是access_token 2 是 api
user_info = {
    "username": "username",
    "password": "password"
}
today = date.today()
yesterday = (date.today() + timedelta(days=-10)).strftime("%Y-%m-%d")  # 昨天日期
# print(yesterday)

write_file_name = str(today) + ".txt"
zoomeye_api = "api"

def back_access_token():  # 获取token
    headers = {'Content-Type': 'application/json'}
    request_access_token_url = "https://api.zoomeye.org/user/login"
    response = requests.post(request_access_token_url, headers=headers, timeout=10, data=json.dumps(user_info)).text
    rr = re.findall(r'"access_token": "(.+)"', response)
    access_token = rr[0]
    return access_token


def url_encode(str): # url 编码
    text = quote(str, 'utf-8')
    return text





if mode == 1:
    access_token = back_access_token()  # 函数返回 token
    headers = {'Authorization': 'JWT {}'.format(access_token)}
if mode == 2:
    headers = {'API-KEY': '{}'.format(zoomeye_api)}


def huoqu_page(): # 获取页数
    page = 0
    change1 = ":"
    change2 = "+"
    a = open("zoomeye_keyword.txt", "r", encoding="utf8")
    aa = a.readlines()
    for i in range(len(aa)):
        b = aa[i].replace("\n", "")
        query = b.replace(change1, url_encode(change1)).replace(change2, url_encode(change2))
        # print(query)
        url = "https://api.zoomeye.org/host/search?query={}".format(query)
        res = requests.get(url, headers=headers).text
        text = json.loads(res)  # 将网页结果转换为json类型
        # print(text)
        total = text['total'] # 查询结果总数
        # print(total)
        if total == 0:
            exit("无结果")
        elif total % 20 == 0:page=int(total/20)
        else:
            page = int(total/20) + 1
        return page

def zoomeye_request():
    change1 = ":"
    change2 = "+"
    a = open("zoomeye_keyword.txt", "r", encoding="utf8")
    aa = a.readlines()
    for i in range(len(aa)):
        b = aa[i].replace("\n", "")
        query = b.replace(change1, url_encode(change1)).replace(change2, url_encode(change2))
        for page in range(1,huoqu_page()+1):
            # print(page)
            url = "https://api.zoomeye.org/host/search?query={}&page={}".format(query,page)
            res = requests.get(url, headers=headers).text
            text = json.loads(res) # 将网页结果转换为json类型
            length = len(text['matches'])
            # print(length)
            try:
                for j in range(length):
                    service = text['matches'][j]['portinfo']['service']
                    ip = text['matches'][j]['ip']
                    port = text['matches'][j]['portinfo']['port']
                    print(str(service)+"://"+str(ip)+":"+str(port))
                    # with open(write_file_name, 'a+') as oo:
                    #     oo.write(url + "\n")
                    #     oo.close()
            except:
                pass


zoomeye_request()