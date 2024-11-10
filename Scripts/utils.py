import requests
import noneprompt,re,json
import urllib.parse
from loguru import logger
from bs4 import BeautifulSoup
from urllib.parse import unquote

class AutoCharge:
    def __init__(self,cookies,money,password,reload) -> None:
        if reload:
         self.load()
        else:
          if cookies:
           self.cookies=dict(item.split("=", 1) for item in cookies.split("; "))
          else:
           logger.error("cookies is empty")
          self.money=money
          self.password=password
        

    def get_YZM(self) :
        headers = {
          'Host': 'yktpt.glut.edu.cn',
          'X-Requested-With': 'XMLHttpRequest',
          'Sec-Fetch-Site': 'same-origin',
          'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
          'Accept-Encoding': 'gzip, deflate, br',
          'Sec-Fetch-Mode': 'cors',
          'Accept': '*/*',
          'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2011K2C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
          'Connection': 'keep-alive',
          'Referer': 'https://yktpt.glut.edu.cn/Home',
          #'Cookie': self.cookies,
          'Sec-Fetch-Dest': 'empty',
          }
        data={
           "Id":1
        }
        for i in range(5):
            response = requests.post('https://yktpt.glut.edu.cn/Home/GetYzm',data=data ,cookies=self.cookies,headers=headers)
            if response.status_code == 200:
              """ YZM=response.json()["dataModel"]
              match = re.search(r'Yzm=([^&]+)', YZM)
              if match:
                YZM=match.group(1)
              else:
                 YZM=None
              self.YZM=YZM """
              YZM=response.text
              if not YZM: continue
              self.YZM=YZM
              return YZM
        return None
            
    def get_allcookies(self,response):
    # 尝试直接从 headers 获取 Set-Cookie
       cookies_header = response.headers.get('Set-Cookie')
       if cookies_header:
          return cookies_header.split(', ')  # 将结果返回为一个列表
       else:
          # 如果没有 Set-Cookie 或需要处理 cookies 对象
          return response.cookies.get_dict()  # 返回 cookies 字典
    

    def get_cookies(self,YZM):
       if not YZM: logger.error("YZM获取失败！")
       url=f"https://yktdkcz.glut.edu.cn/a?Yzm={YZM}"
       headers = {
          'Host': 'yktdkcz.glut.edu.cn',
          'Sec-Fetch-Site': 'same-origin',
          'Accept-Encoding': 'gzip, deflate, br',
          #'Cookie': self.cookies,
          'Connection': 'keep-alive',
          'Sec-Fetch-Mode': 'navigate',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2011K2C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
          'Referer': 'https://yktdkcz.glut.edu.cn/?Yzm=4c342ffb68c64dd095f2bf84005a294865750&',
          'Sec-Fetch-Dest': 'document',
          'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
           }
       for i in range(5):
        try:
           response=requests.get(url,headers=headers,cookies=self.cookies)
        
           if response.status_code==200: 
             #logger.debug(response.text) 
             cookies_list = self.get_allcookies(response)
             if len(cookies_list)<2: continue
             for cookie in cookies_list:
               new_cookie = cookie.split(';')[0]
               try:
                self.cookies.update({new_cookie.split('=')[0]:new_cookie.split('=')[1]})
               except:
                  logger.debug(f"跳过无效cookie:{new_cookie}")
          
             verfication_token=self.analyze_verfication_token(response.text)
             self.verfication_token=verfication_token
             html=BeautifulSoup(response.text,"html.parser")
             self.studentName=html.find("input",{"id":"StudentName"})
             if self.studentName:
                self.studentName=unquote(self.studentName.get("value"))
             return self.cookies,self.verfication_token
        except requests.exceptions as e:
             logger.error("请求错误，正在重试")
             logger.error(e)
        return None
    
    def choose_room(self):
       self.studentNumber=urllib.parse.unquote(self.cookies["1000142StudentNumber"])
       headers = {
          'Host': 'yktdkcz.glut.edu.cn',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'X-Requested-With': 'XMLHttpRequest',
          'Sec-Fetch-Site': 'same-origin',
          'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
          'Accept-Encoding': 'gzip, deflate, br',
          'Sec-Fetch-Mode': 'cors',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Origin': 'https://yktdkcz.glut.edu.cn',
          'Content-Length': '233',
          'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2011K2C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
          'Referer': f"https://yktdkcz.glut.edu.cn/a/?Yzm={self.YZM}",
          'Connection': 'keep-alive',
          'Sec-Fetch-Dest': 'empty',
          #'Cookie': self.cookies,
               }

       data = {
          'level': '1',
          'studentNumber': self.studentNumber,
          '__RequestVerificationToken': self.verfication_token,
            }
       url='https://yktdkcz.glut.edu.cn/a/Home/GetRoomTree'
       response = requests.post(url, headers=headers, data=data,cookies=self.cookies)
       areas=[]
       for i in response.json()['dataModel']:
          data={}
          data['name']=i['name']
          data["cookieName"]=i["cookieName"]
          data["code"]=i["code"]
          areas.append(data)
       self.areas=areas                        
       self.area=(noneprompt.ListPrompt(
                            question="请选择区域",
                            choices=[
                               noneprompt.Choice(x["name"],data=x["code"])
                               for x in areas
                               
                            ],
                         ).prompt()
               )
       
       self.area_name=self.area.name
       self.area=self.area.data
       self.area=urllib.parse.unquote(self.area)
       data = {
          'level': '2',
          'campusCode':self.area,
          'studentNumber': self.studentNumber,
          '__RequestVerificationToken': self.verfication_token,
            }
       response = requests.post(url,headers=headers,data=data,cookies=self.cookies)
       buildings=[]
       for i in response.json()['dataModel']:
          data={}
          data['name']=i['name']
          data["cookieName"]=i['cookieName']
          data["code"]=i['code']
          buildings.append(data)
       self.buildings=buildings
       self.building=(noneprompt.ListPrompt(
                         question="请选择楼栋",
                         choices=[
                            noneprompt.Choice(name=x["name"],data=x["code"])
                            for x in buildings
                         ],
                        ).prompt())
       self.building_name=self.building.name
       self.building=self.building.data
       self.building=urllib.parse.unquote(self.building)
       data = {
          'level': '3',
          'campusCode':self.area,
          'buildingCode':self.building,
          'studentNumber': self.studentNumber,
          '__RequestVerificationToken': self.verfication_token,
            }
       response = requests.post(url,headers=headers,data=data,cookies=self.cookies)
       rooms=[]
       for i in response.json()['dataModel']:
          data={}
          data["name"]=i['name']
          data["cookieName"]=i['cookieName']
          data["code"]=i['code']
          rooms.append(data)
       self.rooms=rooms
       self.room=(noneprompt.ListPrompt(
                             question="请选择房间",
                             choices=[
                                noneprompt.Choice(name=x["name"],data=x["code"])
                                for x in rooms
                             ]
                                ).prompt())
       self.room_name=self.room.name
       self.room=self.room.data
       self.room=urllib.parse.unquote(self.room)
       
    def update_cookies(self):
       self.cookies.update({"1000142buildingCode":urllib.parse.quote(self.building)})
       self.cookies.update({"1000142campusCode":urllib.parse.quote(self.area)})
       self.cookies.update({"1000142roomCode":urllib.parse.quote(self.room)})
       self.cookies.update({"balance":"60.00"})
       self.cookies.update({"StudentNumber":self.studentNumber})
       self.cookies.update({"1000142":urllib.parse.quote(f"{self.area_name}/{self.building_name}/{self.room_name}")})
       self.cookies.update({"stuName":urllib.parse.quote(self.studentName)})
    def analyze_verfication_token(self,html):
        
        match = re.search(r'name="__RequestVerificationToken"([^/]+)', html)
        if match:
            match=re.search(r'value="([^"]+)', match.group(1))
            self.verfication_token=match.group(1)

            return self.verfication_token
        else:
            self.verfication_token=None
    def save(self):
      data={}
      data["cookies"]=self.cookies
      data["area"]=self.area             
      data["building"]=self.building
      data["room"]=self.room
      data["studentNumber"]=self.studentNumber
      data["YZM"]=self.YZM
      data["vefication_token"]=self.verfication_token
      data["areas"]=self.areas
      data["buildings"]=self.buildings
      data["rooms"]=self.rooms
      data["money"]=self.money
      data["password"]=self.password
      with open("data.json","w") as f:
          json.dump(data,f)              

    def load(self):
        with open("data.json","r") as f:
            data=json.load(f)
        self.cookies=data["cookies"]
        self.area=data["area"]
        self.building=data["building"]
        self.room=data["room"]
        self.studentNumber=data["studentNumber"]
        self.YZM=data["YZM"]
        self.vefication_token=data["vefication_token"]
        self.money=data["money"]
        self.password=data["password"]
    def get_Vtoken(self):
       
       headers = {
          'Host': 'yktdkcz.glut.edu.cn',
          'Sec-Fetch-Site': 'same-origin',
          #'Cookie': datas["cookies"],
          'Connection': 'keep-alive',
          'Sec-Fetch-Mode': 'navigate',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2011K2C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
          'Referer': f"https://yktdkcz.glut.edu.cn/a/?Yzm={self.YZM}",
          'Sec-Fetch-Dest': 'document',
          'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                 }
       for i in range(5):
          
          response = requests.get('https://yktdkcz.glut.edu.cn/a/RechargeAndQuery/Index',cookies=self.cookies, headers=headers) 
          if response.status_code==200:
              vefication_token=self.analyze_verfication_token(response.text)
              if vefication_token:
                 
                 self.vefication_token=vefication_token


    def submit(self):
        headers = {
          'Host': 'yktdkcz.glut.edu.cn',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'X-Requested-With': 'XMLHttpRequest',
          'Sec-Fetch-Site': 'same-origin',
          'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
          'Accept-Encoding': 'gzip, deflate, br',
          'Sec-Fetch-Mode': 'cors',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Origin': 'https://yktdkcz.glut.edu.cn',
          'Content-Length': '295',
          'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2011K2C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
          'Referer': 'https://yktdkcz.glut.edu.cn/a/RechargeAndQuery/Index',
          'Connection': 'keep-alive',
          'Sec-Fetch-Dest': 'empty',
          #'Cookie': self.cookies,
            }

        data = {
          'roomCode': urllib.parse.unquote(self.room),
          'rechargeNumber': self.money,
          'studentNumber': urllib.parse.unquote(self.studentNumber),
          '__RequestVerificationToken': self.vefication_token,
          'password': self.password,
           }

        response = requests.post('https://yktdkcz.glut.edu.cn/a/RechargeAndQuery/Recharge', headers=headers, data=data,cookies=self.cookies)     
        logger.info(response.text)