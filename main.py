import time,os
from Scripts.utils import *
from Scripts.init import *

cookies=""
money="0.01"
version="1.0.0"
password="123456"
def load_config():
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
    
    
    AutoCharge.get_Vtoken(charge_self)
    AutoCharge.submit(charge_self)
    logger.info("Finished!")
    time.sleep(10)
