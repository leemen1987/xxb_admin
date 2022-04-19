from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.contrib import auth
from xxb import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import time
import requests
import datetime
import xlwt
from io import BytesIO
from dateutil.rrule import rrule, DAILY
from .models import customer_service


# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def busline(request):
    return render(request, "busline.html")


def traffic(request):
    return render(request, "traffic_count.html")


def kpbus(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')
    if user_ip:
        models.traffic_count.objects.create(ip_adress=user_ip, web_traffic="1")
    return render(request, "bus.html")


def traffic_count(request):
    if request.POST:
        date1 = request.POST.get("date_from")
        date2 = request.POST.get("date_to")
        if date1:
            date_from = date1
            f_year = date1.split('-')[0]
            f_month = date1.split('-')[1]
            f_day = date1.split('-')[2]
            d_from = datetime.datetime(int(f_year), int(f_month), int(f_day), 0, 0, 0, 0)
        else:
            date_from = datetime.datetime.now().date().strftime("%Y-%m-%d")
            f_year = date_from.split('-')[0]
            f_month = date_from.split('-')[1]
            f_day = date_from.split('-')[2]
            d_from = datetime.datetime(int(f_year), int(f_month), int(f_day), 0, 0, 0, 0)
        if date2:
            date_to = date2
            t_year = date2.split('-')[0]
            t_month = date2.split('-')[1]
            t_day = date2.split('-')[2]
            d_to = datetime.datetime(int(t_year), int(t_month), int(t_day), 23, 59, 59, 999999)
        else:
            date_to = datetime.datetime.now().date().strftime("%Y-%m-%d")
            t_year = date_to.split('-')[0]
            t_month = date_to.split('-')[1]
            t_day = date_to.split('-')[2]
            d_to = datetime.datetime(int(t_year), int(t_month), int(t_day), 23, 59, 59, 999999)
        result = models.traffic_count.objects.filter(date__range=(d_from, d_to))
        result_count = result.values('web_traffic').count()
        result_ip_count = result.values('ip_adress').distinct().count()
        all_traffic_count = models.traffic_count.objects.values('web_traffic').count()
        ip_count = models.traffic_count.objects.values('ip_adress').distinct().count()
    return render(request, "traffic_count.html",
                  {"result": result, "result_count": result_count, "result_ip_count": result_ip_count,
                   "all_traffic_count": all_traffic_count, "ip_count": ip_count, "date_from": date_from,
                   "date_to": date_to})


# 后台页面登陆
def login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return render(request, "meal_order.html")
        else:
            # 用户名密码错误
            redirect("/login/")
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/login/")


def register(request):
    return render(request, "register.html")


@login_required
def xxb_index(request):
    return render(request, "meal_order.html")


@login_required
def updata_menu(request):
    return render(request, "updata_menu.html")


# 课程统计(个人项目)
@login_required
@csrf_exempt
def search_class(request):
    # all_events = models.Events.objects.all()
    search_result = []
    c_result = ""
    c_price = []
    error_msg = ""
    if request.POST:
        d1 = request.POST.get("class_name")
        if d1 == "0":
            class_name = "思栢"
        elif d1 == "1":
            class_name = "星动"
        elif d1 == "2":
            class_name = "俏丽人"
        d2 = request.POST.get("start_date")
        d3 = request.POST.get("end_date")
        if d2 == "" or d3 == "":
            error_msg = "请选择日期!"
        else:
            d_d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
            d_d3 = datetime.datetime.strptime(d3, "%Y-%m-%d").date()
            search_result = models.Events.objects.filter(Q(start_date__range=(d_d2, d_d3)) & Q(event_name=class_name))
            c_result = search_result.count()
            c_price = search_result.aggregate(Sum("price"))
    return render(request, "search_class.html",
                  {"result": search_result, "c_result": c_result, "c_price": c_price, "error_msg": error_msg})


# 上传平台测试
@csrf_exempt
def apitest(request):
    wx_code = request.GET.get('key')
    code2Session_api = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxb70d9f0ef843f5ed&secret=1bb571a20b5b05b2f62b5827be06af4b&grant_type=authorization_code&js_code=' + wx_code
    if wx_code:
        wx_openid = requests.get(code2Session_api)
        # print(wx_openid.json())
        wx_data = wx_openid.json()
        openid = wx_data['openid']
        # openid_test = models.user_info.objects.filter(openid=openid)
        # print(openid)
        if models.user_info.objects.filter(openid=openid):
            wx_data['old_user'] = True
        else:
            wx_data['new_user'] = True
        # print(wx_data)
        return JsonResponse(wx_data)
    else:
        return HttpResponse('get openid error')


@csrf_exempt
def dz_car(request):
    wx_code = request.GET.get('key')
    code2Session_api = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxc1b87c1402da1955&secret=0ba2e7f57ba53cb137f939d806328d45&grant_type=authorization_code&js_code=' + wx_code
    if wx_code:
        wx_openid = requests.get(code2Session_api)
        wx_data = wx_openid.json()
        openid = wx_data['openid']
        if openid:
            return JsonResponse(wx_data)
    else:
        return HttpResponse('get openid error')


# 微信报餐--创建用户
@csrf_exempt
def create_user(request):
    openid = request.GET.get('openid')
    user_name = request.GET.get('name')
    tel = request.GET.get('tel')
    line = request.GET.get('line')
    print(openid, user_name, tel, line)
    if models.user_info.objects.filter(openid=openid):
        return HttpResponse('xxx')
    else:
        if models.user_info.objects.create(openid=openid, user_name=user_name, tel=tel, line=line):
            return HttpResponse('done')
        else:
            return HttpResponse('tryagain')


# 微信报餐--周菜单
@csrf_exempt
def week_menu(request):
    menu_data = models.week_menu.objects.all()
    week_menu = []
    for i in menu_data:
        day_menu = {}
        day_menu['week_day'] = i.week_day
        day_menu['breakfast'] = i.breakfast
        day_menu['lunch'] = i.lunch
        day_menu['dinner'] = i.dinner
        week_menu.append(day_menu)
    return HttpResponse(json.dumps(week_menu))


@login_required
@csrf_exempt
def updata_menu_data(request):
    breakfast = request.POST.getlist('breakfast')
    for index, item in enumerate(breakfast):
        if item != '':
            models.week_menu.objects.filter(id=(int(index) + 1)).update(breakfast=item)
    lunch = request.POST.getlist('lunch')
    for index, item in enumerate(lunch):
        if item != '':
            models.week_menu.objects.filter(id=(int(index) + 1)).update(lunch=item)
    dinner = request.POST.getlist('dinner')
    for index, item in enumerate(dinner):
        if item != '':
            models.week_menu.objects.filter(id=(int(index) + 1)).update(dinner=item)
    return HttpResponse('ok')


# 微信报餐--获取用户信息
@csrf_exempt
def user_list(request):
    openid = request.GET.get('openid')
    user_list = models.user_info.objects.filter(openid=openid)
    user_info = {}
    for i in user_list:
        user_info["openid"] = i.openid
        user_info["name"] = i.user_name
        user_info["line"] = i.line
    return JsonResponse(user_info)


# 微信报餐--操作记录
@csrf_exempt
def edit_log(request):
    openid = request.GET.get('openid')
    log_data = models.edit_log.objects.filter(openid=openid).order_by("edit_date").reverse()
    edit_log = []
    for i in log_data:
        log = {}
        log['edit_time'] = i.edit_time.strftime('%Y-%m-%d %H:%M:%S')
        log['edit_type'] = i.edit_type
        log['edit_date'] = str(i.edit_date)
        log['breakfast'] = i.breakfast
        log['lunch'] = i.lunch
        log['dinner'] = i.dinner
        edit_log.append(log)
    return HttpResponse(json.dumps(edit_log))


# 微信报餐后台--饭堂统计
@login_required
@csrf_exempt
def count_order(request):
    if request.POST:
        line = request.POST.get("line")
        date = request.POST.get("date")
        if date:
            date = request.POST.get("date")
        else:
            date = datetime.datetime.now().date().strftime("%Y-%m-%d")
        if line != '全部':
            result = models.Meal_offer.objects.filter(order_date=date, uid__line=line).order_by('uid__line',
                                                                                                'uid__user_name')
            b_result = models.Meal_offer.objects.filter(order_date=date, breakfast="1", uid__line=line).count()
            l_result = models.Meal_offer.objects.filter(order_date=date, lunch="1", uid__line=line).count()
            d_result = models.Meal_offer.objects.filter(order_date=date, dinner="1", uid__line=line).count()
        else:
            result = models.Meal_offer.objects.filter(order_date=date).order_by('uid__line', 'uid__user_name')
            b_result = models.Meal_offer.objects.filter(order_date=date, breakfast="1").count()
            l_result = models.Meal_offer.objects.filter(order_date=date, lunch="1").count()
            d_result = models.Meal_offer.objects.filter(order_date=date, dinner="1").count()
            b_c = models.Meal_offer.objects.filter(order_date=date, breakfast="1", breakfast_check="1").count()
            l_c = models.Meal_offer.objects.filter(order_date=date, lunch="1", lunch_check="1").count()
            d_c = models.Meal_offer.objects.filter(order_date=date, dinner="1", dinner_check="1").count()
    return render(request, "meal_order.html",
                  {"result": result, "b_result": b_result, "l_result": l_result, "d_result": d_result, "date": date,
                   "b_c": b_c, "l_c": l_c, "d_c": d_c})


# 微信报餐后台--财务统计
@login_required
@csrf_exempt
def finance_count(request):
    if request.POST:
        date1 = request.POST.get("date_from")
        date2 = request.POST.get("date_to")
        if date1:
            date_from = date1
        else:
            date_from = datetime.datetime.now().date().strftime("%Y-%m-%d")
        if date2:
            date_to = date2
        else:
            date_to = datetime.datetime.now().date().strftime("%Y-%m-%d")
        result = models.Meal_offer.objects.filter(order_date__range=(date_from, date_to))
        result_count = result.values("uid").annotate(b_count=Sum("breakfast"), l_count=Sum("lunch"),
                                                     d_count=Sum("dinner")).values("uid__user_name",
                                                                                   "uid__line", "b_count",
                                                                                   "l_count", "d_count").order_by(
            'uid__line', 'uid__user_name')
        all_b_count = models.Meal_offer.objects.filter(order_date__range=(date_from, date_to), breakfast="1").count()
        all_l_count = models.Meal_offer.objects.filter(order_date__range=(date_from, date_to), lunch="1").count()
        all_d_count = models.Meal_offer.objects.filter(order_date__range=(date_from, date_to), dinner="1").count()
    return render(request, "finance_count.html",
                  {"result_count": result_count, "all_b_count": all_b_count, "all_l_count": all_l_count,
                   "all_d_count": all_d_count, "date_from": date_from, "date_to": date_to})


# 微信报餐后台--选择列表获取
@csrf_exempt
def c_select(request):
    select = models.c_select.objects.all().order_by('Rank')
    select_data = []
    for i in select:
        line = i.select
        select_data.append(line)
    return HttpResponse(json.dumps(select_data))


@login_required
@csrf_exempt
def meal_order(request):
    return render(request, "meal_order.html")


@login_required
@csrf_exempt
def finance(request):
    return render(request, "finance_count.html")


# 微信报餐--报餐统计
@csrf_exempt
def user_order(request):
    openid = request.GET.get('openid')
    check_month = request.GET.get('check_month').split('-')
    year = int(check_month[0])
    month = int(check_month[1])
    order_arr = []
    uid = models.user_info.objects.filter(openid=openid).distinct()[0].id
    user_order = models.Meal_offer.objects.filter(uid=uid, order_date__year=year, order_date__month=month).order_by(
        'order_date').reverse()
    if user_order:
        for u in user_order:
            order_sub_arr = {}
            order_sub_arr["id"] = u.id
            order_sub_arr["openid"] = u.uid.openid
            order_sub_arr["name"] = u.uid.user_name
            order_sub_arr["order_date"] = str(u.order_date)
            order_sub_arr["breakfast"] = u.breakfast
            order_sub_arr["lunch"] = u.lunch
            order_sub_arr["dinner"] = u.dinner
            order_arr.append(order_sub_arr)
        return HttpResponse(json.dumps(order_arr))
    else:
        return HttpResponse('none')


# 微信报餐--报餐合计
@csrf_exempt
def user_order_count(request):
    openid = request.GET.get('openid')
    check_month = request.GET.get('check_month').split('-')
    year = int(check_month[0])
    month = int(check_month[1])
    # order_arr = []
    uid = models.user_info.objects.filter(openid=openid).distinct()[0].id
    b_c = models.Meal_offer.objects.filter(uid=uid, breakfast="1", order_date__year=year,
                                           order_date__month=month).count()
    l_c = models.Meal_offer.objects.filter(uid=uid, lunch="1", order_date__year=year,
                                           order_date__month=month).count()
    d_c = models.Meal_offer.objects.filter(uid=uid, dinner="1", order_date__year=year,
                                           order_date__month=month).count()
    return HttpResponse(json.dumps({"b_c": b_c, "l_c": l_c, "d_c": d_c}))


# 微信报餐--删除报餐
@csrf_exempt
def del_order(request):
    order_date = datetime.datetime.strptime(request.GET.get('order_date'), "%Y-%m-%d").date()
    id = request.GET.get('id')
    openid = request.GET.get('openid')
    if models.Meal_offer.objects.filter(order_date=order_date, id=id).delete():
        models.edit_log.objects.create(edit_date=order_date, edit_type="删除", openid=openid, breakfast="报餐")
        return HttpResponse('complete')
    else:
        return HttpResponse('error')


# 微信报餐--报餐
@csrf_exempt
def order_meal(request):
    order_data = request.GET.get('checkboxItems')
    # user_name = request.GET.get('user_name')
    openid = request.GET.get('openid')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    order_json = json.loads(order_data)
    d_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    d_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    uid = models.user_info.objects.get(openid=openid)
    edit_date = start_date + "至" + end_date
    d1 = start_date.split('-')
    s_d = ''.join(d1)
    d2 = str(datetime.date.today()).split('-')
    e_d = ''.join(d2)
    check_time = int(s_d) - int(e_d)
    print(check_time, int(time.strftime("%H%M%S")))
    if int(time.strftime("%H%M%S")) > 210000:
        return HttpResponse('error-001')
    else:
        if order_json[0]['checked'] == True:
            breakfast = '1'
            breakfast2 = '早餐'
        else:
            breakfast = breakfast2 = ''
        if order_json[1]['checked'] == True:
            lunch = '1'
            lunch2 = '午餐'
        else:
            lunch = lunch2 = ''
        if order_json[2]['checked'] == True:
            dinner = '1'
            dinner2 = '晚餐'
        else:
            dinner = dinner2 = ''

        for dt in rrule(DAILY, dtstart=d_start_date, until=d_end_date):
            if models.Meal_offer.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d")):
                if order_json[0]['checked'] == True:
                    b1 = '1'
                    b2 = '早餐'
                else:
                    b1 = b2 = models.Meal_offer.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d"))[0].breakfast
                if order_json[1]['checked'] == True:
                    l1 = '1'
                    l2 = '午餐'
                else:
                    l1 = l2 = models.Meal_offer.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d"))[0].lunch
                if order_json[2]['checked'] == True:
                    d1 = '1'
                    d2 = '晚餐'
                else:
                    d1 = d2 = models.Meal_offer.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d"))[0].dinner

                models.Meal_offer.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d")).update(breakfast=b1,
                                                                                                     lunch=l1,
                                                                                                     dinner=d1)
                models.edit_log.objects.create(edit_type="修改", edit_date=dt.strftime("%Y-%m-%d"), breakfast=b2,
                                               lunch=l2, dinner=d2, openid=openid)
            else:
                models.Meal_offer.objects.create(uid=uid, order_date=dt.strftime("%Y-%m-%d"), breakfast=breakfast,
                                                 lunch=lunch,
                                                 dinner=dinner)
        else:
            models.edit_log.objects.create(edit_date=edit_date, edit_type="新增", breakfast=breakfast2, lunch=lunch2,
                                           dinner=dinner2, openid=openid)
        return HttpResponse('done')
    #     print (dt.strftime("%Y-%m-%d"),breakfast,lunch,dinner)
    # print(order_json,user_name,start_date,end_date,openid)
    # return HttpResponse('xxkk')


# 微信报餐--验餐
@csrf_exempt
def order_check(request):
    openid = request.GET.get('openid')
    today = datetime.date.today()
    if 50000 <= int(time.strftime("%H%M%S")) <= 84500:
        if models.Meal_offer.objects.filter(uid__openid=openid, order_date=today, breakfast="1"):
            edit_info = models.Meal_offer.objects.get(uid__openid=openid, order_date=today, breakfast="1")
            edit_info.breakfast_check = "1"
            edit_info.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    if 100000 <= int(time.strftime("%H%M%S")) <= 124500:
        if models.Meal_offer.objects.filter(uid__openid=openid, order_date=today, lunch="1"):
            edit_info = models.Meal_offer.objects.get(uid__openid=openid, order_date=today, lunch="1")
            edit_info.lunch_check = "1"
            edit_info.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    if 160000 <= int(time.strftime("%H%M%S")) <= 180000:
        if models.Meal_offer.objects.filter(uid__openid=openid, order_date=today, dinner="1"):
            edit_info = models.Meal_offer.objects.get(uid__openid=openid, order_date=today, dinner="1")
            edit_info.dinner_check = "1"
            edit_info.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    else:
        return HttpResponse('3')


# 获取课程(个人项目)
@login_required
@csrf_exempt
def get_list(request):
    # all_events = models.Events.objects.all()
    if request.GET:
        event_arr = []
        all_events = models.Events.objects.all()
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['id'] = i.even_id
            event_sub_arr['title'] = i.event_name
            str_start_date = str(i.start_date)
            if str_start_date == "" or i.end_time == "":
                start_date = datetime.datetime.strptime(str_start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                event_sub_arr['start'] = start_date
                event_arr.append(event_sub_arr)
            else:
                start_time = datetime.datetime.strptime(str_start_date + "T" + i.start_time, "%Y-%m-%dT%H:%M").strftime(
                    "%Y-%m-%dT%H:%M")
                end_time = datetime.datetime.strptime(str_start_date + "T" + i.end_time, "%Y-%m-%dT%H:%M").strftime(
                    "%Y-%m-%dT%H:%M")
                event_sub_arr['start'] = start_time
                event_sub_arr['end'] = end_time
                event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))
    return render(request, "today_class.html")


# 获取课程(个人项目)
@login_required
@csrf_exempt
def event(request):
    if request.GET:
        d1 = request.GET.get("title")
        d2 = request.GET.get("start")
        t1 = request.GET.get("start_time")
        t2 = request.GET.get("end_time")
        # models.Events.objects.create(event_name=d1, start_date=d2, start_time=t1, end_time=t2)
        if d1 == "俏丽人":
            price = 120
            models.Events.objects.create(event_name=d1, start_date=d2, start_time=t1, end_time=t2, price=price)
        elif d1 == "星动":
            price = 100
            models.Events.objects.create(event_name=d1, start_date=d2, start_time=t1, end_time=t2, price=price)
        else:
            price = 90
            models.Events.objects.create(event_name=d1, start_date=d2, start_time=t1, end_time=t2, price=price)
        event_arr = []
        all_events = models.Events.objects.all()
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['id'] = i.even_id
            event_sub_arr['title'] = i.event_name
            str_start_date = str(i.start_date)
            if i.start_time == "" or i.end_time == "":
                start_date = datetime.datetime.strptime(str_start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                event_sub_arr['start'] = start_date
                event_arr.append(event_sub_arr)
            else:
                start_time = datetime.datetime.strptime(str_start_date + "T" + i.start_time, "%Y-%m-%dT%H:%M").strftime(
                    "%Y-%m-%dT%H:%M")
                end_time = datetime.datetime.strptime(str_start_date + "T" + i.end_time, "%Y-%m-%dT%H:%M").strftime(
                    "%Y-%m-%dT%H:%M")
                event_sub_arr['start'] = start_time
                event_sub_arr['end'] = end_time
                event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))
    return render(request, "today_class.html")


# 删除课程(个人项目)
@login_required
@csrf_exempt
def del_val(request):
    if request.GET:
        del_val = request.GET.get("del_val")
        models.Events.objects.filter(even_id=del_val).delete()
        event_arr = []
        all_events = models.Events.objects.all()
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['id'] = i.even_id
            event_sub_arr['title'] = i.event_name
            str_start_date = str(i.start_date)
            if i.start_time == "" or i.end_time == "":
                start_date = datetime.datetime.strptime(str_start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                event_sub_arr['start'] = start_date
                event_arr.append(event_sub_arr)
            else:
                start_time = datetime.datetime.strptime(str_start_date + "T" + i.start_time, "%Y-%m-%dT%H:%M").strftime(
                    "%Y-%m-%dT%H:%M")
                end_time = datetime.datetime.strptime(str_start_date + "T" + i.end_time, "%Y-%m-%dT%H:%M").strftime(
                    "%Y-%m-%dT%H:%M")
                event_sub_arr['start'] = start_time
                event_sub_arr['end'] = end_time
                event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))
    return render(request, "today_class.html")


# 测试接口
@csrf_exempt
def strong_test(request):
    q1 = request.body
    # q2 = request.content_type
    # q3 = request.META
    print(q1)
    return HttpResponse(q1)


# 思创里程接收接口
@csrf_exempt
def strong_mileage_info(request):
    request_data2 = json.loads(str(request.body, 'utf-8'))
    car_id = request_data2['car_id']
    car_num = request_data2['car_num']
    YunYingRiQi = request_data2['YunYingRiQi']
    today_mileage = request_data2['today_mileage']
    data_create_time = request_data2['data_create_time']
    d = datetime.datetime.strptime(YunYingRiQi, '%Y-%m-%d')
    yesterday = d + datetime.timedelta(days=-1)
    # yesterday = (datetime.datetime.strptime(YunYingRiQi, "%Y-%m-%d") + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    if models.strong_mileage_info.objects.filter(car_num=car_num, YunYingRiQi=YunYingRiQi):
        new_data = models.strong_mileage_info.objects.get(car_num=car_num, YunYingRiQi=YunYingRiQi)
        new_data.today_mileage = today_mileage
        new_data.data_create_time = data_create_time
        new_data.save()
    else:
        models.strong_mileage_info.objects.create(car_id=car_id, car_num=car_num, YunYingRiQi=YunYingRiQi,
                                                  today_mileage=today_mileage, data_create_time=data_create_time)
    if models.strong_mileage_info.objects.filter(car_num=car_num, YunYingRiQi=yesterday):
        yesterday_mileage = models.strong_mileage_info.objects.get(car_num=car_num, YunYingRiQi=yesterday).total_mileage
        today_data = models.strong_mileage_info.objects.get(car_num=car_num, YunYingRiQi=YunYingRiQi)
        today_data.total_mileage = int(today_mileage) + int(yesterday_mileage)
        today_data.save()
        return HttpResponse('done')
    else:
        today_data = models.strong_mileage_info.objects.get(car_num=car_num, YunYingRiQi=YunYingRiQi)
        today_data.total_mileage = today_mileage
        today_data.save()
        return HttpResponse('done')


@csrf_exempt
def get_bus_status_info_new(request):
    busline_name = request.POST.get('lname')
    roadid = models.RoadID_to_BusLine.objects.filter(BusLine=busline_name)[0].RoadID
    roadtype = request.POST.get('roadtype')
    headers_one = {'Content-type': 'application/x-www-form-urlencoded'}
    headers = {'Content-type': 'application/json;charset=UTF-8'}
    body = {"userName": "transmitDev", "passWord": "dR3QG3gI831dFpZi"}
    body1 = {"RoadID": roadid}
    get_jsessionid = requests.post('http://113.107.137.16:58088/app/login', headers=headers_one, data=body)
    jsessionid = get_jsessionid.json()['data']
    ret = requests.post(
        'http://113.107.137.16:58088/app/getAppStatusInfoData;jsessionid=' + jsessionid,
        headers=headers, json=body1)
    data = ret.json()
    bus_stop = []
    if roadtype == '0':
        for i in data['data']:
            gps_info_item = {}
            busstate = i['BusState']
            roadtype_info = i['RoadType']
            gps_info_item['id'] = i['SiteId']
            if busstate == '1':
                if roadtype_info == '0' or roadtype_info == '2':
                    bus_stop.append(gps_info_item)
    if roadtype == '1':
        for i in data['data']:
            gps_info_item = {}
            busstate = i['BusState']
            roadtype_info = i['RoadType']
            gps_info_item['id'] = i['SiteId']
            if busstate == '1':
                if roadtype_info == '1' or roadtype_info == '3':
                    bus_stop.append(gps_info_item)
    return HttpResponse(json.dumps(bus_stop))


@csrf_exempt
def get_bus_status_info(request):
    busline_name = request.POST.get('select')
    roadid = models.RoadID_to_BusLine.objects.filter(BusLine=busline_name)[0].RoadID
    roadtype = models.RoadID_to_BusLine.objects.filter(BusLine=busline_name)[0].RoadType
    headers_one = {'Content-type': 'application/x-www-form-urlencoded'}
    headers = {'Content-type': 'application/json;charset=UTF-8'}
    body = {"userName": "transmitDev", "passWord": "dR3QG3gI831dFpZi"}
    body1 = {"RoadID": roadid}
    get_jsessionid = requests.post('http://113.107.137.16:58088/app/login', headers=headers_one, data=body)
    jsessionid = get_jsessionid.json()['data']
    ret = requests.post(
        'http://113.107.137.16:58088/app/getAppStatusInfoData;jsessionid=' + jsessionid,
        headers=headers, json=body1)
    data = ret.json()
    bus_stop = []
    if roadtype == '0':
        for i in data['data']:
            gps_info_item = {}
            roadtype_info = i['RoadType']
            gps_info_item['id'] = int(i['SiteId'])
            if roadtype_info == '0' or roadtype_info == '2':
                bus_stop.append(gps_info_item)
    if roadtype == '1':
        for i in data['data']:
            gps_info_item = {}
            roadtype_info = i['RoadType']
            gps_info_item['id'] = int(i['SiteId'])
            if roadtype_info == '1' or roadtype_info == '3':
                bus_stop.append(gps_info_item)
    return HttpResponse(json.dumps(bus_stop))


@csrf_exempt
def get_road_line_info_new(request):
    busline_name = request.POST.get('lname')
    roadtype = request.POST.get('roadtype')
    roadid = models.RoadID_to_BusLine.objects.filter(BusLine=busline_name)[0].RoadID
    bus_line = []
    if models.RoadSite_info.objects.all():
        for e in models.RoadSite_info.objects.filter(RoadID=roadid, RoadType=roadtype).order_by('SiteNo'):
            line_info_item = {}
            line_info_item['id'] = e.SiteID
            line_info_item['name'] = e.SiteName
            line_info_item['achievement'] = ''
            bus_line.append(line_info_item)
        return HttpResponse(json.dumps(bus_line))
    else:
        return HttpResponse({'error': 'none'})


@csrf_exempt
def get_road_line_info(request):
    busline_name = request.POST.get('select')
    roadtype = models.RoadID_to_BusLine.objects.filter(BusLine=busline_name)[0].RoadType
    roadid = models.RoadID_to_BusLine.objects.filter(BusLine=busline_name)[0].RoadID
    bus_line = []
    if models.RoadSite_info.objects.all():
        for e in models.RoadSite_info.objects.filter(RoadID=roadid, RoadType=roadtype).order_by('SiteNo'):
            line_info_item = {}
            line_info_item['id'] = e.SiteID
            line_info_item['name'] = e.SiteName
            line_info_item['achievement'] = ''
            bus_line.append(line_info_item)
        return HttpResponse(json.dumps(bus_line))
    else:
        return HttpResponse({'error': 'none'})


# 微信报餐后台--饭堂统计导出EXCEL
@csrf_exempt
def export_excel(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')  # 设置HTTPResponse的类型
    response['Content-Disposition'] = 'attachment;filename=order.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')
    # 写入文件标题
    sheet.write(0, 0, '报餐日期')
    sheet.write(0, 1, '姓名')
    sheet.write(0, 2, '线路')
    sheet.write(0, 3, '早餐')
    sheet.write(0, 4, '午餐')
    sheet.write(0, 5, '晚餐')
    # 写入数据
    data_row = 1
    s_date = request.POST.get('s_date')
    select = request.POST.get('select')
    if select == '全部':
        r_info = models.Meal_offer.objects.filter(order_date=s_date).order_by('uid__line', 'uid__user_name')
        c1 = models.Meal_offer.objects.filter(order_date=s_date, breakfast="1").count()
        c2 = models.Meal_offer.objects.filter(order_date=s_date, lunch="1").count()
        c3 = models.Meal_offer.objects.filter(order_date=s_date, dinner="1").count()
    else:
        r_info = models.Meal_offer.objects.filter(uid__line=select, order_date=s_date)
        c1 = models.Meal_offer.objects.filter(order_date=s_date, uid__line=select, breakfast="1").count()
        c2 = models.Meal_offer.objects.filter(order_date=s_date, uid__line=select, lunch="1").count()
        c3 = models.Meal_offer.objects.filter(order_date=s_date, uid__line=select, dinner="1").count()
    for i in r_info:
        sheet.write(data_row, 0, s_date)
        sheet.write(data_row, 1, i.uid.user_name)
        sheet.write(data_row, 2, i.uid.line)
        sheet.write(data_row, 3, i.breakfast)
        sheet.write(data_row, 4, i.lunch)
        sheet.write(data_row, 5, i.dinner)
        data_row = data_row + 1
    sheet.write(data_row, 0, "早餐总数")
    sheet.write(data_row, 1, c1)
    sheet.write(data_row + 1, 0, "午餐总数")
    sheet.write(data_row + 1, 1, c2)
    sheet.write(data_row + 2, 0, "晚餐总数")
    sheet.write(data_row + 2, 1, c3)

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


# 微信报餐后台--财务统计导出EXCEL
@csrf_exempt
def export_excel_finance(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')  # 设置HTTPResponse的类型
    response['Content-Disposition'] = 'attachment;filename=count.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('count-sheet')
    # 写入文件标题
    sheet.write(0, 0, '报餐日期')
    sheet.write(0, 1, '姓名')
    sheet.write(0, 2, '线路')
    sheet.write(0, 3, '早餐')
    sheet.write(0, 4, '午餐')
    sheet.write(0, 5, '晚餐')
    # 写入数据
    data_row = 1
    date_from = request.POST.get("date_from")
    date_to = request.POST.get("date_to")

    result = models.Meal_offer.objects.filter(order_date__range=(date_from, date_to))
    result_count = result.values("uid").annotate(b_count=Sum("breakfast"), l_count=Sum("lunch"),
                                                 d_count=Sum("dinner")).values("uid__user_name",
                                                                               "uid__line", "b_count",
                                                                               "l_count", "d_count").order_by(
        'uid__line', 'uid__user_name')
    all_b_count = models.Meal_offer.objects.filter(order_date__range=(date_from, date_to), breakfast="1").count()
    all_l_count = models.Meal_offer.objects.filter(order_date__range=(date_from, date_to), lunch="1").count()
    all_d_count = models.Meal_offer.objects.filter(order_date__range=(date_from, date_to), dinner="1").count()
    count_date = str(date_from) + '-' + str(date_to)
    for i in result_count:
        sheet.write(data_row, 0, count_date)
        sheet.write(data_row, 1, i["uid__user_name"])
        sheet.write(data_row, 2, i["uid__line"])
        sheet.write(data_row, 3, i["b_count"])
        sheet.write(data_row, 4, i["l_count"])
        sheet.write(data_row, 5, i["d_count"])
        data_row = data_row + 1
    sheet.write(data_row, 0, "早餐合计")
    sheet.write(data_row, 1, all_b_count)
    sheet.write(data_row + 1, 0, "午餐合计")
    sheet.write(data_row + 1, 1, all_l_count)
    sheet.write(data_row + 2, 0, "晚餐合计")
    sheet.write(data_row + 2, 1, all_d_count)

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


@csrf_exempt
def c_busline(request):
    select = models.RoadID_to_BusLine.objects.all().order_by('Rank').distinct()
    select_data = []
    for i in select:
        line_item = {}
        line_item['line'] = i.BusLine
        line_item['info'] = i.Line_info
        select_data.append(line_item)
    return HttpResponse(json.dumps(select_data))


@csrf_exempt
def c_busline_new(request):
    select = models.RoadID_to_BusLine_new.objects.all().order_by('Rank').distinct()
    select_data = []
    for i in select:
        line_item = {}
        line_item['line'] = i.BusLine
        line_item['info'] = i.Line_info
        select_data.append(line_item)
    return HttpResponse(json.dumps(select_data))


@csrf_exempt
def select_busline(request):
    select = models.RoadID_to_BusLine.objects.all().order_by('Rank')
    select_data = []
    for i in select:
        line = i.BusLine
        select_data.append(line)
    # l_data = list(set(select_data))
    return HttpResponse(json.dumps(select_data))


@login_required
@csrf_exempt
def copy_info(request):
    headers_one = {'Content-type': 'application/x-www-form-urlencoded'}
    headers = {'Content-type': 'application/json;charset=UTF-8'}
    body = {"userName": "transmitDev", "passWord": "dR3QG3gI831dFpZi"}
    body1 = {"RoadID": ""}
    get_jsessionid = requests.post('http://113.107.137.16:58088/app/login', headers=headers_one, data=body)
    jsessionid = get_jsessionid.json()['data']
    ret = requests.post(
        'http://113.107.137.16:58088/app/getAppRoadSiteInfoData;jsessionid=' + jsessionid,
        headers=headers, json=body1)
    data = ret.json()
    for i in data['data']:
        models.RoadSite_info.objects.create(RoadID=i['RoadID'], RoadName=i['RoadName'], RoadType=i['RoadType'],
                                            SiteID=i['SiteID'], SiteNo=i['SiteNo'], SiteName=i['SiteName'])
    return HttpResponse('done!')


@csrf_exempt
def service(request):
    if request.GET.get('code'):
        code = request.GET.get('code')
        get_accesstoken_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx8af98cd4e28747a1&secret=d0b2cfc39add4c10cea685bc25bfb6b2&code=' + code + '&grant_type=authorization_code'
        get_accesstoken = requests.get(get_accesstoken_url)
        accesstoken = get_accesstoken.json()
        openid = accesstoken['openid']
    else:
        openid = request.GET.get('openid')
    return render(request, "service.html", {"openid": openid})


@csrf_exempt
def my_service(request):
    openid = request.GET.get('openid')
    if models.customer_service.objects.filter(openid=openid):
        service_data = models.customer_service.objects.filter(openid=openid)
    else:
        service_data = 'empty'
    return render(request, "my_service.html", {"openid": openid, "service_data": service_data})


@csrf_exempt
def upload_file(request):
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    openid = request.POST.get('openid')
    service_data = {}
    service_data['openid'] = openid
    service_data['name'] = request.POST.get('name')
    service_data['phone_num'] = request.POST.get('phone_num')
    service_data['line'] = request.POST.get('line')
    service_data['car_num'] = request.POST.get('car_num')
    service_data['opinion'] = request.POST.get('opinion')
    service_data['happen_date'] = datetime.datetime.strptime(request.POST.get('happen_date'), "%Y-%m-%d %H:%M")
    service_data['start_stop'] = request.POST.get('start_stop')
    service_data['end_stop'] = request.POST.get('end_stop')
    service_data['system_id'] = now_time
    file = request.FILES.get('upload_file')
    service_count = models.customer_service.objects.filter(Q(openid=openid) & Q(reply="")).count()
    if service_count >= 3:
        resp = {'receive': 'error'}
        return JsonResponse(resp)
    else:
        if file:
            file_type = str(request.FILES.get('upload_file').name).split('.')[-1]
            rename = now_time + '.' + file_type
            file.name = rename
            if file_type == 'jpg':
                img = customer_service(img=file)
                img.save()
            else:
                video = customer_service(video=file)
                video.save()
            models.customer_service.objects.filter(Q(img__contains=now_time) | Q(video__contains=now_time)).update(
                **service_data)
        else:
            models.customer_service.objects.create(**service_data)
        resp = {'receive': 'complete'}
        return JsonResponse(resp)


@login_required
@csrf_exempt
def reply_service(request):
    if models.customer_service.objects.all():
        if models.customer_service.objects.filter(~Q(reply='')):
            service_data = models.customer_service.objects.filter(~Q(reply=''))
        else:
            service_data = 'no_reply'
        if models.customer_service.objects.filter(reply=''):
            wait_reply = models.customer_service.objects.filter(reply='')
        else:
            wait_reply = 'no_data'
    else:
        service_data = 'empty'
        wait_reply = 'no_data'
    return render(request, "reply_service.html", {"service_data": service_data, "wait_reply": wait_reply})


@login_required
@csrf_exempt
def check_open(request):
    uid = request.GET.get('uid')
    resp_data = models.customer_service.objects.filter(id=uid)
    resp = {}
    if resp_data.values('video')[0]['video']:

        resp['file'] = 'video'
        resp['src'] = resp_data.values('video')[0]['video']
    elif resp_data.values('img')[0]['img']:

        resp['file'] = 'img'
        resp['src'] = resp_data.values('img')[0]['img']
    else:
        resp['file'] = 'none'

    request.close()
    return JsonResponse(resp)


@login_required
def upload_reply(request):
    uid_data = request.POST.get('uid_data')
    reply_data = request.POST.get('reply_data')
    now_time = datetime.datetime.now()
    if models.customer_service.objects.filter(id=uid_data).update(reply=reply_data, reply_time=now_time):
        return HttpResponse('done')
    else:
        return HttpResponse('error')


# 义祠报餐获取openid
@csrf_exempt
def get_openid_yc(request):
    wx_code = request.GET.get('key')
    code2Session_api = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx2aa9664260efde3e&secret=ae9c8c98b11d75d077aa0aef80157fa0&grant_type=authorization_code&js_code=' + wx_code
    if wx_code:
        wx_openid = requests.get(code2Session_api)
        # print(wx_openid.json())
        wx_data = wx_openid.json()
        openid = wx_data['openid']

        if models.user_info_yc.objects.filter(openid=openid):
            wx_data['old_user'] = True
        else:
            wx_data['new_user'] = True

        return JsonResponse(wx_data)
    else:
        return HttpResponse('get openid error')


# 义祠报餐--创建用户
@csrf_exempt
def create_user_yc(request):
    openid = request.GET.get('openid')
    user_name = request.GET.get('name')
    tel = request.GET.get('tel')
    line = request.GET.get('line')
    print(openid, user_name, tel, line)
    if models.user_info_yc.objects.filter(openid=openid):
        return HttpResponse('xxx')
    else:
        if models.user_info_yc.objects.create(openid=openid, user_name=user_name, tel=tel, line=line):
            return HttpResponse('done')
        else:
            return HttpResponse('tryagain')


# 义祠报餐--周菜单
@csrf_exempt
def week_menu_yc(request):
    menu_data = models.week_menu_yc.objects.all()
    week_menu = []
    for i in menu_data:
        day_menu = {}
        day_menu['week_day'] = i.week_day
        day_menu['breakfast'] = i.breakfast
        day_menu['lunch'] = i.lunch
        day_menu['dinner'] = i.dinner
        week_menu.append(day_menu)
    return HttpResponse(json.dumps(week_menu))


# 义祠报餐--获取用户信息
@csrf_exempt
def user_list_yc(request):
    openid = request.GET.get('openid')
    user_list = models.user_info_yc.objects.filter(openid=openid)
    user_info = {}
    for i in user_list:
        user_info["openid"] = i.openid
        user_info["name"] = i.user_name
        user_info["line"] = i.line
        if i.activation == 'pass':
            user_info["activation"] = True
        else:
            user_info["activation"] = False
    return JsonResponse(user_info)


# 义祠报餐--操作记录
@csrf_exempt
def edit_log_yc(request):
    openid = request.GET.get('openid')
    log_data = models.edit_log_yc.objects.filter(openid=openid).order_by("edit_date").reverse()
    edit_log = []
    for i in log_data:
        log = {}
        log['edit_time'] = i.edit_time.strftime('%Y-%m-%d %H:%M:%S')
        log['edit_type'] = i.edit_type
        log['edit_date'] = str(i.edit_date)
        log['breakfast'] = i.breakfast
        log['lunch'] = i.lunch
        log['dinner'] = i.dinner
        edit_log.append(log)
    return HttpResponse(json.dumps(edit_log))


# 义祠报餐后台--饭堂统计
@login_required
@csrf_exempt
def count_order_yc(request):
    if request.POST:
        line = request.POST.get("line")
        date = request.POST.get("date")
        if date:
            date = request.POST.get("date")
        else:
            date = datetime.datetime.now().date().strftime("%Y-%m-%d")
        if line != '全部':
            result = models.Meal_offer_yc.objects.filter(order_date=date, uid__line=line).order_by('uid__line',
                                                                                                   'uid__user_name')
            b_result = models.Meal_offer_yc.objects.filter(order_date=date, breakfast="1", uid__line=line).count()
            l_result = models.Meal_offer_yc.objects.filter(order_date=date, lunch="1", uid__line=line).count()
            d_result = models.Meal_offer_yc.objects.filter(order_date=date, dinner="1", uid__line=line).count()
        else:
            result = models.Meal_offer_yc.objects.filter(order_date=date).order_by('uid__line', 'uid__user_name')
            b_result = models.Meal_offer_yc.objects.filter(order_date=date, breakfast="1").count()
            l_result = models.Meal_offer_yc.objects.filter(order_date=date, lunch="1").count()
            d_result = models.Meal_offer_yc.objects.filter(order_date=date, dinner="1").count()
    return render(request, "meal_order_yc.html",
                  {"result": result, "b_result": b_result, "l_result": l_result, "d_result": d_result, "date": date})


# 义祠报餐后台--财务统计
@login_required
@csrf_exempt
def finance_count_yc(request):
    if request.POST:
        date1 = request.POST.get("date_from")
        date2 = request.POST.get("date_to")
        if date1:
            date_from = date1
        else:
            date_from = datetime.datetime.now().date().strftime("%Y-%m-%d")
        if date2:
            date_to = date2
        else:
            date_to = datetime.datetime.now().date().strftime("%Y-%m-%d")
        result = models.Meal_offer_yc.objects.filter(order_date__range=(date_from, date_to))
        result_count = result.values("uid").annotate(b_count=Sum("breakfast"), l_count=Sum("lunch"),
                                                     d_count=Sum("dinner")).values("uid__user_name",
                                                                                   "uid__line", "b_count",
                                                                                   "l_count", "d_count").order_by(
            'uid__line', 'uid__user_name')
        all_b_count = models.Meal_offer_yc.objects.filter(order_date__range=(date_from, date_to), breakfast="1").count()
        all_l_count = models.Meal_offer_yc.objects.filter(order_date__range=(date_from, date_to), lunch="1").count()
        all_d_count = models.Meal_offer_yc.objects.filter(order_date__range=(date_from, date_to), dinner="1").count()
    return render(request, "finance_count_yc.html",
                  {"result_count": result_count, "all_b_count": all_b_count, "all_l_count": all_l_count,
                   "all_d_count": all_d_count, "date_from": date_from, "date_to": date_to})


# 义祠报餐后台--选择列表获取
@csrf_exempt
def c_select_yc(request):
    select = models.c_select_yc.objects.all().order_by('Rank')
    select_data = []
    for i in select:
        line = i.select
        select_data.append(line)
    return HttpResponse(json.dumps(select_data))


@login_required
@csrf_exempt
def meal_order_yc(request):
    return render(request, "meal_order_yc.html")


@login_required
@csrf_exempt
def finance_yc(request):
    return render(request, "finance_count_yc.html")


# 义祠报餐--报餐统计
@csrf_exempt
def user_order_yc(request):
    openid = request.GET.get('openid')
    check_month = request.GET.get('check_month').split('-')
    year = int(check_month[0])
    month = int(check_month[1])
    order_arr = []
    uid = models.user_info_yc.objects.filter(openid=openid).distinct()[0].id
    user_order = models.Meal_offer_yc.objects.filter(uid=uid, order_date__year=year, order_date__month=month).order_by(
        'order_date').reverse()
    if user_order:
        for u in user_order:
            order_sub_arr = {}
            order_sub_arr["id"] = u.id
            order_sub_arr["openid"] = u.uid.openid
            order_sub_arr["name"] = u.uid.user_name
            order_sub_arr["order_date"] = str(u.order_date)
            order_sub_arr["breakfast"] = u.breakfast
            order_sub_arr["lunch"] = u.lunch
            order_sub_arr["dinner"] = u.dinner
            order_arr.append(order_sub_arr)
        return HttpResponse(json.dumps(order_arr))
    else:
        return HttpResponse('none')


# 义祠报餐--报餐合计
@csrf_exempt
def user_order_count_yc(request):
    openid = request.GET.get('openid')
    check_month = request.GET.get('check_month').split('-')
    year = int(check_month[0])
    month = int(check_month[1])
    # order_arr = []
    uid = models.user_info_yc.objects.filter(openid=openid).distinct()[0].id
    b_c = models.Meal_offer_yc.objects.filter(uid=uid, breakfast="1", order_date__year=year,
                                              order_date__month=month).count()
    l_c = models.Meal_offer_yc.objects.filter(uid=uid, lunch="1", order_date__year=year,
                                              order_date__month=month).count()
    d_c = models.Meal_offer_yc.objects.filter(uid=uid, dinner="1", order_date__year=year,
                                              order_date__month=month).count()
    return HttpResponse(json.dumps({"b_c": b_c, "l_c": l_c, "d_c": d_c}))


# 义祠报餐--删除报餐
@csrf_exempt
def del_order_yc(request):
    order_date = datetime.datetime.strptime(request.GET.get('order_date'), "%Y-%m-%d").date()
    id = request.GET.get('id')
    openid = request.GET.get('openid')
    if models.Meal_offer_yc.objects.filter(order_date=order_date, id=id).delete():
        models.edit_log_yc.objects.create(edit_date=order_date, edit_type="删除", openid=openid, breakfast="报餐")
        return HttpResponse('complete')
    else:
        return HttpResponse('error')


# 义祠报餐--报餐
@csrf_exempt
def order_meal_yc(request):
    order_data = request.GET.get('checkboxItems')
    # user_name = request.GET.get('user_name')
    openid = request.GET.get('openid')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    order_json = json.loads(order_data)
    d_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    d_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    uid = models.user_info_yc.objects.get(openid=openid)
    edit_date = start_date + "至" + end_date
    if order_json[0]['checked'] == True:
        breakfast = '1'
        breakfast2 = '早餐'
    else:
        breakfast = breakfast2 = ''
    if order_json[1]['checked'] == True:
        lunch = '1'
        lunch2 = '午餐'
    else:
        lunch = lunch2 = ''
    if order_json[2]['checked'] == True:
        dinner = '1'
        dinner2 = '晚餐'
    else:
        dinner = dinner2 = ''

    for dt in rrule(DAILY, dtstart=d_start_date, until=d_end_date):
        if models.Meal_offer_yc.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d")):
            if order_json[0]['checked'] == True:
                b1 = '1'
                b2 = '早餐'
            else:
                b1 = b2 = models.Meal_offer_yc.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d"))[0].breakfast
            if order_json[1]['checked'] == True:
                l1 = '1'
                l2 = '午餐'
            else:
                l1 = l2 = models.Meal_offer_yc.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d"))[0].lunch
            if order_json[2]['checked'] == True:
                d1 = '1'
                d2 = '晚餐'
            else:
                d1 = d2 = models.Meal_offer_yc.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d"))[0].dinner

            models.Meal_offer_yc.objects.filter(uid=uid, order_date=dt.strftime("%Y-%m-%d")).update(breakfast=b1,
                                                                                                    lunch=l1,
                                                                                                    dinner=d1)
            models.edit_log_yc.objects.create(edit_type="修改", edit_date=dt.strftime("%Y-%m-%d"), breakfast=b2,
                                              lunch=l2, dinner=d2, openid=openid)
        else:
            models.Meal_offer_yc.objects.create(uid=uid, order_date=dt.strftime("%Y-%m-%d"), breakfast=breakfast,
                                                lunch=lunch,
                                                dinner=dinner)
    else:
        models.edit_log_yc.objects.create(edit_date=edit_date, edit_type="新增", breakfast=breakfast2, lunch=lunch2,
                                          dinner=dinner2, openid=openid)
    return HttpResponse('done')


# 义祠报餐--验餐
@csrf_exempt
def order_check_yc(request):
    openid = request.GET.get('openid')
    today = datetime.date.today()
    if 50000 <= int(time.strftime("%H%M%S")) <= 84500:
        if models.Meal_offer_yc.objects.filter(uid__openid=openid, order_date=today, breakfast="1"):
            edit_info = models.Meal_offer_yc.objects.get(uid__openid=openid, order_date=today, breakfast="1")
            edit_info.breakfast_check = "1"
            edit_info.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    if 100000 <= int(time.strftime("%H%M%S")) <= 124500:
        if models.Meal_offer_yc.objects.filter(uid__openid=openid, order_date=today, lunch="1"):
            edit_info = models.Meal_offer_yc.objects.get(uid__openid=openid, order_date=today, lunch="1")
            edit_info.lunch_check = "1"
            edit_info.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    if 160000 <= int(time.strftime("%H%M%S")) <= 180000:
        if models.Meal_offer_yc.objects.filter(uid__openid=openid, order_date=today, dinner="1"):
            edit_info = models.Meal_offer_yc.objects.get(uid__openid=openid, order_date=today, dinner="1")
            edit_info.dinner_check = "1"
            edit_info.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    else:
        return HttpResponse('3')


@login_required
def updata_menu_yc(request):
    return render(request, "updata_menu_yc.html")


@login_required
@csrf_exempt
def updata_menu_data_yc(request):
    breakfast = request.POST.getlist('breakfast')
    for index, item in enumerate(breakfast):
        if item != '':
            models.week_menu_yc.objects.filter(id=(int(index) + 1)).update(breakfast=item)
    lunch = request.POST.getlist('lunch')
    for index, item in enumerate(lunch):
        if item != '':
            models.week_menu_yc.objects.filter(id=(int(index) + 1)).update(lunch=item)
    dinner = request.POST.getlist('dinner')
    for index, item in enumerate(dinner):
        if item != '':
            models.week_menu_yc.objects.filter(id=(int(index) + 1)).update(dinner=item)
    return HttpResponse('ok')


# 义祠报餐后台--财务统计导出EXCEL
@csrf_exempt
def export_excel_finance_yc(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')  # 设置HTTPResponse的类型
    response['Content-Disposition'] = 'attachment;filename=count.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('count-sheet')
    # 写入文件标题
    sheet.write(0, 0, '报餐日期')
    sheet.write(0, 1, '姓名')
    sheet.write(0, 2, '线路')
    sheet.write(0, 3, '早餐')
    sheet.write(0, 4, '午餐')
    sheet.write(0, 5, '晚餐')
    # 写入数据
    data_row = 1
    date_from = request.POST.get("date_from")
    date_to = request.POST.get("date_to")

    result = models.Meal_offer_yc.objects.filter(order_date__range=(date_from, date_to))
    result_count = result.values("uid").annotate(b_count=Sum("breakfast"), l_count=Sum("lunch"),
                                                 d_count=Sum("dinner")).values("uid__user_name",
                                                                               "uid__line", "b_count",
                                                                               "l_count", "d_count").order_by(
        'uid__line', 'uid__user_name')
    all_b_count = models.Meal_offer_yc.objects.filter(order_date__range=(date_from, date_to), breakfast="1").count()
    all_l_count = models.Meal_offer_yc.objects.filter(order_date__range=(date_from, date_to), lunch="1").count()
    all_d_count = models.Meal_offer_yc.objects.filter(order_date__range=(date_from, date_to), dinner="1").count()
    count_date = str(date_from) + '-' + str(date_to)
    for i in result_count:
        sheet.write(data_row, 0, count_date)
        sheet.write(data_row, 1, i["uid__user_name"])
        sheet.write(data_row, 2, i["uid__line"])
        sheet.write(data_row, 3, i["b_count"])
        sheet.write(data_row, 4, i["l_count"])
        sheet.write(data_row, 5, i["d_count"])
        data_row = data_row + 1
    sheet.write(data_row, 0, "早餐合计")
    sheet.write(data_row, 1, all_b_count)
    sheet.write(data_row + 1, 0, "午餐合计")
    sheet.write(data_row + 1, 1, all_l_count)
    sheet.write(data_row + 2, 0, "晚餐合计")
    sheet.write(data_row + 2, 1, all_d_count)

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


# 义祠报餐后台--饭堂统计导出EXCEL
@csrf_exempt
def export_excel_yc(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')  # 设置HTTPResponse的类型
    response['Content-Disposition'] = 'attachment;filename=order.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')
    # 写入文件标题
    sheet.write(0, 0, '报餐日期')
    sheet.write(0, 1, '姓名')
    sheet.write(0, 2, '线路')
    sheet.write(0, 3, '早餐')
    sheet.write(0, 4, '午餐')
    sheet.write(0, 5, '晚餐')
    # 写入数据
    data_row = 1
    s_date = request.POST.get('s_date')
    select = request.POST.get('select')
    if select == '全部':
        r_info = models.Meal_offer_yc.objects.filter(order_date=s_date).order_by('uid__line', 'uid__user_name')
        c1 = models.Meal_offer_yc.objects.filter(order_date=s_date, breakfast="1").count()
        c2 = models.Meal_offer_yc.objects.filter(order_date=s_date, lunch="1").count()
        c3 = models.Meal_offer_yc.objects.filter(order_date=s_date, dinner="1").count()
    else:
        r_info = models.Meal_offer_yc.objects.filter(uid__line=select, order_date=s_date)
        c1 = models.Meal_offer_yc.objects.filter(order_date=s_date, uid__line=select, breakfast="1").count()
        c2 = models.Meal_offer_yc.objects.filter(order_date=s_date, uid__line=select, lunch="1").count()
        c3 = models.Meal_offer_yc.objects.filter(order_date=s_date, uid__line=select, dinner="1").count()
    for i in r_info:
        sheet.write(data_row, 0, s_date)
        sheet.write(data_row, 1, i.uid.user_name)
        sheet.write(data_row, 2, i.uid.line)
        sheet.write(data_row, 3, i.breakfast)
        sheet.write(data_row, 4, i.lunch)
        sheet.write(data_row, 5, i.dinner)
        data_row = data_row + 1
    sheet.write(data_row, 0, "早餐总数")
    sheet.write(data_row, 1, c1)
    sheet.write(data_row + 1, 0, "午餐总数")
    sheet.write(data_row + 1, 1, c2)
    sheet.write(data_row + 2, 0, "晚餐总数")
    sheet.write(data_row + 2, 1, c3)

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


@login_required
@csrf_exempt
def user_console_yc(request):
    result = models.user_info_yc.objects.all()
    print(result)
    return render(request, 'user_console_yc.html', {'result': result})


@csrf_exempt
def pass_ban_yc(request):
    edit_tpye = request.GET.get('edit_tpye')
    openid = request.GET.get('openid')
    if models.user_info_yc.objects.filter(openid=openid).update(activation=edit_tpye):
        print(edit_tpye, openid)
        return HttpResponse('done')
    else:
        return HttpResponse('error')


@csrf_exempt
def warehouse_data(request):
    data1 = models.warehouse_data.objects.all()
    data_arr = []
    if data1:
        for u in data1:
            data_sub_arr = {}
            data_sub_arr["id"] = u.id
            data_sub_arr["company"] = u.company
            data_sub_arr["name"] = u.equipment
            data_sub_arr["stock"] = u.stock
            data_arr.append(data_sub_arr)
        return HttpResponse(json.dumps(data_arr))
    else:
        return HttpResponse('error')


@csrf_exempt
def userecord_data(request):
    data1 = models.userecord.objects.all().order_by("-rep_time")
    data_arr = []
    if data1:
        for u in data1:
            data_sub_arr = {}
            data_sub_arr["fid"] = u.id
            data_sub_arr["fdate"] = u.rep_time.strftime('%Y-%m-%d %H:%M')
            data_sub_arr["car_num"] = u.car_num
            data_sub_arr["falut"] = u.falut
            data_sub_arr["user_item"] = u.use_item
            data_sub_arr["company"] = u.company
            data_arr.append(data_sub_arr)
        return HttpResponse(json.dumps(data_arr))

    else:
        return HttpResponse('error')


@csrf_exempt
def get_detail(request):
    if request.POST:
        company = request.POST.get('company')
        name = request.POST.get('name')
        data1 = models.detail_data.objects.filter(company=company, item=name)
        data_arr = []
        if data1:
            for u in data1:
                data_sub_arr = {}
                data_sub_arr["id"] = u.id
                data_sub_arr["company"] = u.company
                data_sub_arr["item"] = u.item
                data_sub_arr["incomeDate"] = u.in_time.strftime('%Y-%m-%d')
                data_sub_arr["incomeNum"] = u.num
                data_sub_arr["remark"] = u.remark
                data_arr.append(data_sub_arr)
            return HttpResponse(json.dumps(data_arr))
        else:
            return HttpResponse('error')
    else:
        return HttpResponse('error')
