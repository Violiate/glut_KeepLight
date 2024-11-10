from datetime import datetime

class Time:
    def init(self):
         pass
    def count(self):
         if self.get_weekday() and self.is_workingday_time():
              return True
         elif not self.get_weekday() and self.is_holiday_time():
              return True
         else:
                return False
    
    def is_workingday_time(self):
        # 获取当前时间
        now = datetime.now()
    
        # 定义要检查的时间点
        special_times = [
        (23, 32),
        (23, 37),
        (23, 42),
        (23, 47),
        (0, 6),
        (0, 16)
        ]
    
        # 获取当前时间的具体时、分、秒
        current_time = (now.hour, now.minute)
    
        # 检查当前时间是否在特殊时间列表中
        if current_time in special_times:
            return True
        else:
            return False
        
    def is_holiday_time(self):
        # 获取当前时间
        now = datetime.now()
    
        # 定义要检查的时间点
        special_times = [
        
        (0, 2),
        (0, 6),
        (0, 16)
        ]
    
        # 获取当前时间的具体时、分、秒
        current_time = (now.hour, now.minute)
    
        # 检查当前时间是否在特殊时间列表中
        if current_time in special_times:
            return True
        else:
            return False
    def get_weekday(self):
         # 获取当前时间
         now = datetime.now()
    
         # 获取当前时间的星期数，周一为0，周日为6
         weekday = now.weekday()
    
         
    
         # 判断是否为周天到周四
         if 6 >= weekday >= 0 and weekday <= 3:
        
                return True
         # 特别处理周日的情况，因为周日的weekday()返回6
         elif weekday == 6:
            
                return True
    
         return False
