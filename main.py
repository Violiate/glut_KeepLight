import time,os
from datetime import datetime
from Scripts.utils import *
from Scripts.init import *
from Scripts.time import *

cookies=""
money="0.01"
version="1.0.0"
password="123456"
def load_config():
       if not os.path.exists("data.json"): return False
       reload=noneprompt.ListPrompt(
              question="是否加载上次的配置？",
              choices=[noneprompt.Choice(name=x)
                     for x in ["是","否"]
                   
              ],
       ).prompt().name
       if reload=="是" and os.path.exists("data.json"):
            
            return True
       else:
            return False

if __name__ == "__main__":
    init(version)
    if not load_config():
         logger.warning("请确保你的一卡通余额充足，否则可能会导致充值失败！")
         logger.warning("cookies通过抓包获得，在企业微信 A-校园一卡通里可随便抓到，格式为：Jgg-User=Jgg-User-oKJ_xxxxxxxxxxxxxxx; ASP.NET_SessionId=xxxxxxxxxxxxx")
         cookies=noneprompt.InputPrompt(
               question="请输入你的一卡通cookies"

            ).prompt()
         money=noneprompt.InputPrompt(
               question="请输入要充值的金额，默认为0.01，单位为元",
               default_text="0.01"
            ).prompt()
         password=noneprompt.InputPrompt(
                 question="请输入你的一卡通密码，用于支付",
            ).prompt()
         charge_self=AutoCharge(cookies,money,password,False)
         YZM=AutoCharge.get_YZM(charge_self)
         AutoCharge.get_cookies(charge_self,YZM)
         AutoCharge.choose_room(charge_self)
         AutoCharge.update_cookies(charge_self)
         AutoCharge.save(charge_self)
    else:
         charge_self=AutoCharge(None,None,None,True)
    logger.info("Starting...")
    mode=noneprompt.ListPrompt(
         "请选择模式",
         choices=[noneprompt.Choice(name=x)
                  for x in ["定时充值","直接充值"]
                  ],
            ).prompt().name
    if mode=="直接充值":    
         AutoCharge.submit(charge_self)
    else:
      now = datetime.now()
      while True:
       if now.weekday() != datetime.now().weekday():
          AutoCharge.get_Vtoken(charge_self)
          AutoCharge.save(charge_self)
          now = datetime.now()
       if datetime.now().hour>1 and datetime.now().hour<22:
            logger.info("未到时间，睡眠中...")
            time.sleep(3600)
            
       else:
             time_self=Time()
             if Time.count(time_self):
                
                     
                 AutoCharge.submit(charge_self)
                 logger.info("已充值，请留意是否来电")
             time.sleep(33)
