"""xxb_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from xxb import views
from django.views.generic.base import RedirectView
from django.views.static import serve
from django.urls import re_path
from .settings import MEDIA_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xxb/', views.xxb_index),
    path('', views.xxb_index),
    path('get_list/', views.get_list),
    path('manage-event/', views.event),
    path('del_val/', views.del_val),
    path('get_search/', views.search_class),
    path('login/', views.login),
    path('busline/', views.busline),
    path('updata_menu/', views.updata_menu),
    path('updata_menu_data', views.updata_menu_data),
    path('register/', views.register),
    path('apitest', views.apitest),
    path('dz_car', views.dz_car),
    path('order_meal', views.order_meal),
    path('finance/', views.finance),
    path('create_user', views.create_user),
    path('user_list', views.user_list),
    path('meal_order/', views.meal_order),
    path('c_select/', views.c_select),
    path('select_busline/', views.select_busline),
    # path('get_bus_status_info/', views.get_bus_status_info),
    # path('get_road_line_info/', views.get_road_line_info),
    # 义祠报餐url开始
    path('get_openid_yc', views.get_openid_yc),
    path('create_user_yc', views.create_user_yc),
    path('week_menu_yc', views.week_menu_yc),
    path('updata_menu_yc', views.updata_menu_yc),
    path('updata_menu_data_yc', views.updata_menu_data_yc),
    path('user_list_yc', views.user_list_yc),
    path('edit_log_yc', views.edit_log_yc),
    path('count_order_yc', views.count_order_yc),
    path('finance_count_yc', views.finance_count_yc),
    path('export_excel_yc', views.export_excel_yc),
    path('export_excel_finance_yc', views.export_excel_finance_yc),
    path('c_select_yc', views.c_select_yc),
    path('meal_order_yc', views.meal_order_yc),
    path('finance_yc', views.finance_yc),
    path('user_order_yc', views.user_order_yc),
    path('user_order_count_yc', views.user_order_count_yc),
    path('del_order_yc', views.del_order_yc),
    path('order_meal_yc', views.order_meal_yc),
    path('order_check_yc', views.order_check_yc),
    path('user_console_yc', views.user_console_yc),
    path('pass_ban_yc', views.pass_ban_yc),
    #义祠报餐url结束
    path('copy_info/', views.copy_info),
    path('c_busline/', views.c_busline),
    path('c_busline_new/', views.c_busline_new),
    path('count_order/', views.count_order),
    path('finance_count/', views.finance_count),
    path('user_order', views.user_order),
    path('user_order_count', views.user_order_count),
    path('del_order', views.del_order),
    path('edit_log', views.edit_log),
    path('week_menu', views.week_menu),
    path('logout/', views.logout),
    path('order_check', views.order_check),
    path('export_excel/', views.export_excel),
    path('export_excel_finance/', views.export_excel_finance),
    path('get_bus_status_info_new/', views.get_bus_status_info_new),
    path('get_road_line_info_new/', views.get_road_line_info_new),
    path('strong_test/', views.strong_test),
    path('kpbus20057/', views.kpbus),
    path('traffic/', views.traffic),
    path('traffic_count/', views.traffic_count),
    path('strong_mileage_info/', views.strong_mileage_info),
    # path(r'7OUNvL0z23.txt', RedirectView.as_view(url="/static/7OUNvL0z23.txt")),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    path('service/', views.service),
    path('my_service/', views.my_service),
    path('upload_file/', views.upload_file),
    path('reply_service/', views.reply_service),
    path('upload_reply/', views.upload_reply),
    path('check_open/', views.check_open),
    path('warehouse_data/', views.warehouse_data),
    path('userecord_data/', views.userecord_data),
    path('get_detail/', views.get_detail)
]
