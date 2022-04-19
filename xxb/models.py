from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#
class Events(models.Model):
    even_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.CharField(max_length=255, null=True, blank=True)
    end_time = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.event_name

# 公汽报餐-人员信息
class user_info(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=255, null=False, blank=True)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)
    line = models.CharField(max_length=255, null=True, blank=True)

# 公汽报餐-报餐信息
class Meal_offer(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey('user_info', on_delete=models.CASCADE, null=True)
    order_date = models.DateField(null=True, blank=True)
    breakfast = models.CharField(max_length=255, null=True, blank=True, default="")
    breakfast_check = models.CharField(max_length=255, null=True, blank=True, default="")
    lunch = models.CharField(max_length=255, null=True, blank=True, default="")
    lunch_check = models.CharField(max_length=255, null=True, blank=True, default="")
    dinner = models.CharField(max_length=255, null=True, blank=True, default="")
    dinner_check = models.CharField(max_length=255, null=True, blank=True, default="")

class gps_info(models.Model):
    id = models.AutoField(primary_key=True)
    gprs_id = models.CharField(max_length=255, null=True, blank=True)
    onboard_id = models.CharField(max_length=255, null=True, blank=True)
    nextstop_id = models.CharField(max_length=255, null=True, blank=True)
    server_time = models.DateTimeField(null=True, blank=True)

class gps_info_backup(models.Model):
    id = models.AutoField(primary_key=True)
    gprs_id = models.CharField(max_length=255, null=True, blank=True)
    onboard_id = models.CharField(max_length=255, null=True, blank=True)
    nextstop_id = models.CharField(max_length=255, null=True, blank=True)
    server_time = models.DateTimeField(null=True, blank=True)

class station_info(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    gprs_id = models.CharField(max_length=255, null=True, blank=True)
    order_no = models.CharField(max_length=255, null=True, blank=True)
    direction = models.CharField(max_length=255, null=True, blank=True)

class RoadSite_info(models.Model):
    id = models.AutoField(primary_key=True)
    RoadID = models.CharField(max_length=255, null=True, blank=True)
    RoadName = models.CharField(max_length=255, null=True, blank=True)
    RoadType = models.CharField(max_length=255, null=True, blank=True)
    SiteID = models.CharField(max_length=255, null=True, blank=True)
    SiteNo = models.IntegerField(null=True, blank=True)
    SiteName = models.CharField(max_length=255, null=True, blank=True)

class RoadID_to_BusLine(models.Model):
    id = models.AutoField(primary_key=True)
    RoadID = models.CharField(max_length=255, null=True, blank=True)
    BusLine = models.CharField(max_length=255, null=True, blank=True)
    RoadType = models.CharField(max_length=255, null=True, blank=True)
    Line_info = models.CharField(max_length=255, null=True, blank=True)
    Rank = models.IntegerField(null=True, blank=True)

class RoadID_to_BusLine_new(models.Model):
    id = models.AutoField(primary_key=True)
    RoadID = models.CharField(max_length=255, null=True, blank=True)
    BusLine = models.CharField(max_length=255, null=True, blank=True)
    RoadType = models.CharField(max_length=255, null=True, blank=True)
    Line_info = models.CharField(max_length=255, null=True, blank=True)
    Rank = models.IntegerField(null=True, blank=True)

# 公汽报餐-菜谱信息
class week_menu(models.Model):
    id = models.AutoField(primary_key=True)
    week_day = models.CharField(max_length=255, null=True, blank=True, default="")
    breakfast = models.CharField(max_length=255, null=True, blank=True, default="")
    lunch = models.CharField(max_length=255, null=True, blank=True, default="")
    dinner = models.CharField(max_length=255, null=True, blank=True, default="")

# 公汽报餐-操作历史信息
class edit_log(models.Model):
    id = models.AutoField(primary_key=True)
    edit_time = models.DateTimeField(null=True, auto_now=True)
    edit_type = models.CharField(max_length=255, null=True, blank=True, default="")
    edit_date = models.CharField(max_length=255, null=True, blank=True, default="")
    breakfast = models.CharField(max_length=255, null=True, blank=True, default="")
    lunch = models.CharField(max_length=255, null=True, blank=True, default="")
    dinner = models.CharField(max_length=255, null=True, blank=True, default="")
    openid = models.CharField(max_length=255, null=True, blank=True, default="")

class strong_mileage_info(models.Model):
    id = models.AutoField(primary_key=True)
    car_id = models.CharField(max_length=255, null=True, blank=True, default="")
    car_num = models.CharField(max_length=255, null=True, blank=True, default="")
    YunYingRiQi = models.DateField(null=True, blank=True)
    today_mileage = models.CharField(max_length=255, null=True, blank=True, default="")
    total_mileage = models.CharField(max_length=255, null=True, blank=True, default="")
    data_create_time = models.CharField(max_length=255, null=True, blank=True, default="")

class gprsid_to_busline(models.Model):
    id = models.AutoField(primary_key=True)
    gprsid = models.CharField(max_length=255, null=True, blank=True, default="")
    busline = models.CharField(max_length=255, null=True, blank=True, default="")
    direction = models.CharField(max_length=255, null=True, blank=True, default="")

# 公汽报餐-统计列表信息
class c_select(models.Model):
    id = models.AutoField(primary_key=True)
    select = models.CharField(max_length=255, null=True, blank=True, default="")
    Rank = models.IntegerField(null=True, blank=True)

class traffic_count(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(null=True, auto_now_add=True)
    ip_adress = models.CharField(max_length=255, null=True, blank=True, default="")
    web_traffic = models.IntegerField(null=True, blank=True)

class customer_service(models.Model):
    id = models.AutoField(primary_key=True)
    system_id = models.CharField(max_length=255, null=True, blank=True, default="")
    openid = models.CharField(max_length=255, null=True, blank=True, default="")
    name = models.CharField(max_length=255, null=True, blank=True, default="")
    phone_num = models.CharField(max_length=255, null=True, blank=True, default="")
    line = models.CharField(max_length=255, null=True, blank=True, default="")
    car_num = models.CharField(max_length=255, null=True, blank=True, default="")
    opinion = models.CharField(max_length=1024, null=True, blank=True, default="")
    happen_date = models.DateTimeField(null=True)
    start_stop = models.CharField(max_length=255, null=True, blank=True, default="")
    end_stop = models.CharField(max_length=255, null=True, blank=True, default="")
    img = models.ImageField(upload_to="img/", null=True, blank=True)
    video = models.FileField(upload_to="video/", null=True, blank=True)
    reply = models.CharField(max_length=1024, null=True, blank=True, default="")
    reply_time = models.DateTimeField(null=True)


# 义祠报餐-人员信息
class user_info_yc(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=255, null=False, blank=True)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)
    line = models.CharField(max_length=255, null=True, blank=True)
    activation = models.CharField(max_length=255, null=True, blank=True, default="ban")

# 义祠报餐-报餐信息
class Meal_offer_yc(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey('user_info_yc', on_delete=models.CASCADE, null=True)
    order_date = models.DateField(null=True, blank=True)
    breakfast = models.CharField(max_length=255, null=True, blank=True, default="")
    breakfast_check = models.CharField(max_length=255, null=True, blank=True, default="")
    lunch = models.CharField(max_length=255, null=True, blank=True, default="")
    lunch_check = models.CharField(max_length=255, null=True, blank=True, default="")
    dinner = models.CharField(max_length=255, null=True, blank=True, default="")
    dinner_check = models.CharField(max_length=255, null=True, blank=True, default="")

# 义祠报餐-菜谱信息
class week_menu_yc(models.Model):
    id = models.AutoField(primary_key=True)
    week_day = models.CharField(max_length=255, null=True, blank=True, default="")
    breakfast = models.CharField(max_length=255, null=True, blank=True, default="")
    lunch = models.CharField(max_length=255, null=True, blank=True, default="")
    dinner = models.CharField(max_length=255, null=True, blank=True, default="")

# 义祠报餐-操作历史信息
class edit_log_yc(models.Model):
    id = models.AutoField(primary_key=True)
    edit_time = models.DateTimeField(null=True, auto_now=True)
    edit_type = models.CharField(max_length=255, null=True, blank=True, default="")
    edit_date = models.CharField(max_length=255, null=True, blank=True, default="")
    breakfast = models.CharField(max_length=255, null=True, blank=True, default="")
    lunch = models.CharField(max_length=255, null=True, blank=True, default="")
    dinner = models.CharField(max_length=255, null=True, blank=True, default="")
    openid = models.CharField(max_length=255, null=True, blank=True, default="")

# 义祠报餐-统计列表信息
class c_select_yc(models.Model):
    id = models.AutoField(primary_key=True)
    select = models.CharField(max_length=255, null=True, blank=True, default="")
    Rank = models.IntegerField(null=True, blank=True)


# xxb-备件库存信息
class warehouse_data(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=255, null=True, blank=True, default="")
    equipment = models.CharField(max_length=255, null=True, blank=True, default="")
    stock = models.IntegerField(null=True, blank=True)

# xxb-维修记录
class userecord(models.Model):
    id = models.AutoField(primary_key=True)
    rep_time = models.DateTimeField(null=True, auto_now=True)
    car_num = models.CharField(max_length=255, null=True, blank=True, default="")
    falut = models.CharField(max_length=255, null=True, blank=True, default="")
    use_item = models.CharField(max_length=255, null=True, blank=True, default="")
    company = models.CharField(max_length=255, null=True, blank=True, default="")

# xxb-入仓明细
class detail_data(models.Model):
    id = models.AutoField(primary_key=True)
    in_time = models.DateTimeField(null=True, auto_now=True)
    company = models.CharField(max_length=255, null=True, blank=True, default="")
    item = models.CharField(max_length=255, null=True, blank=True, default="")
    num = models.IntegerField(null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True, default="")