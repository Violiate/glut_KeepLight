import time,os,sys
from Scripts.utils import *
from Scripts.init import *

cookies=""
money="0.01"
version="1.0.0"
password="123456"


if __name__ == "__main__":
    init(version)
    cookies=noneprompt.InputPrompt(
        message="请输入你的一卡通cookies，通过抓包获得，在企业微信 A-校园一卡通里可随便抓到，格式为：Jgg-User=Jgg-User-oKJ_xxxxxxxxxxxxxxx; ASP.NET_SessionId=xxxxxxxxxxxxx"

    ).prompt()
    money=noneprompt.InputPrompt(
        message="请输入要充值的金额，默认为0.01，单位为元",
        default_text="0.01"
    ).prompt()
    password=noneprompt.InputPrompt(
        message="请输入你的一卡通密码，用于支付",
    ).prompt()
    logger.info("Starting...")
    charge_self=AutoCharge(cookies,money,password)
    YZM=AutoCharge.get_YZM(charge_self)
    AutoCharge.get_cookies(charge_self,YZM)
    AutoCharge.choose_room(charge_self)
    AutoCharge.update_cookies(charge_self)
    AutoCharge.save(charge_self)
    AutoCharge.get_Vtoken(charge_self)
    AutoCharge.submit(charge_self)
    logger.info("Finished!")
    time.sleep(10)
