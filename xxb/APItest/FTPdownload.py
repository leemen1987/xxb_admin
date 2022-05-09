#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ftplib
import ssl
import socket
import xlrd
import sys
import os
import django
from datetime import datetime, timedelta
import time
from dateutil.rrule import rrule, DAILY

django.setup()

from xxb import models
from django.db.models import Q

sys.path.extend(r'C:\Users\leemen\Desktop\xxb_admin')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxb_admin.settings")

FTPTLS_OBJ = ftplib.FTP_TLS


# Class to manage implicit FTP over TLS connections, with passive transfer mode
# - Important note:
#   If you connect to a VSFTPD server, check that the vsftpd.conf file contains
#   the property require_ssl_reuse=NO
class FTPTLS(FTPTLS_OBJ):
    host = "127.0.0.1"
    port = 990
    user = "anonymous"
    timeout = 60

    logLevel = 0

    # Init both this and super
    def __init__(self, host=None, user=None, passwd=None, acct=None, keyfile=None, certfile=None, context=None,
                 timeout=60):
        FTPTLS_OBJ.__init__(self, host, user, passwd, acct, keyfile, certfile, context, timeout)

    # Custom function: Open a new FTPS session (both connection & login)
    def openSession(self, host="127.0.0.1", port=990, user="anonymous", password=None, timeout=60):
        self.user = user
        # connect()
        ret = self.connect(host, port, timeout)
        # prot_p(): Set up secure data connection.
        try:
            ret = self.prot_p()
            if (self.logLevel > 1): self._log("INFO - FTPS prot_p() done: " + ret)
        except Exception as e:
            if (self.logLevel > 0): self._log("ERROR - FTPS prot_p() failed - " + str(e))
            raise e
        # login()
        try:
            ret = self.login(user=user, passwd=password)
            if (self.logLevel > 1): self._log("INFO - FTPS login() done: " + ret)
        except Exception as e:
            if (self.logLevel > 0): self._log("ERROR - FTPS login() failed - " + str(e))
            raise e
        if (self.logLevel > 1): self._log("INFO - FTPS session successfully opened")

    # Override function
    def connect(self, host="127.0.0.1", port=990, timeout=60):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)
            self.af = self.sock.family
            self.sock = ssl.wrap_socket(self.sock, self.keyfile, self.certfile)
            self.file = self.sock.makefile('r')
            self.welcome = self.getresp()
            if (self.logLevel > 1): self._log("INFO - FTPS connect() done: " + self.welcome)
        except Exception as e:
            if (self.logLevel > 0): self._log("ERROR - FTPS connect() failed - " + str(e))
            raise e
        return self.welcome

    # Override function
    def makepasv(self):
        host, port = FTPTLS_OBJ.makepasv(self)
        # Change the host back to the original IP that was used for the connection
        host = socket.gethostbyname(self.host)
        return host, port

    # Custom function: Close the session
    def closeSession(self):
        try:
            self.close()
            if (self.logLevel > 1): self._log("INFO - FTPS close() done")
        except Exception as e:
            if (self.logLevel > 0): self._log("ERROR - FTPS close() failed - " + str(e))
            raise e
        if (self.logLevel > 1): self._log("INFO - FTPS session successfully closed")

    # Private method for logs
    def _log(self, msg):
        # Be free here on how to implement your own way to redirect logs (e.g: to a console, to a file, etc.)
        print(msg)


def get_xls():
    host = '218.19.140.180'
    port = 990
    user = '004-KPZHGJ'
    password = 'cFbLzxU!MQGE'

    myFtps = FTPTLS()
    myFtps.logLevel = 2
    myFtps.openSession(host, port, user, password)
    # print(myFtps.retrlines("LIST"))
    myFtps.cwd('/20200412')
    bufsize = 1024
    file_handle = open('./download/KPZHGJ_20200412.xls', 'wb').write
    filename = 'RETR ' + 'KPZHGJ_20200412.xls'
    myFtps.retrbinary(filename, file_handle, bufsize)
    time.sleep(5)
    myFtps.closeSession()


def create_log():
    excel_obj = xlrd.open_workbook('./download/KPZHGJ_20200412.xls').sheet_by_name('1')
    time.sleep(1)
    dt = models.unionpay_log.__doc__
    title_list = dt[dt.find('(') + 1:dt.find(')')].split(",")
    title_list.pop(0)

    for item in range(1, excel_obj.nrows):
        dic = {}
        item_row = excel_obj.row_values(item)
        settlement_date = datetime.strptime(item_row[0], "%Y%m%d").strftime("%Y-%m-%d")  # 格式化第一列的日期格式
        settlement_time = datetime.strptime(item_row[3], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

        for col in range(0, excel_obj.ncols):
            dic[title_list[0].strip()] = settlement_date
            dic[title_list[3].strip()] = settlement_time
            dic[title_list[col].strip()] = item_row[col]
        print(dic)
        models.unionpay_log.objects.create(**dic)
    print('done')


# get_xls()
# time.sleep(10)

def updata_log():  #待更新条件修改
    data = models.unionpay_log.objects.all()
    for i in data:
        tty = i.tty
        filter_data = models.tty_info.objects.filter(Q(bankcard_id=tty) | Q(pos_id=tty) | Q(oda_id=tty))
        for x in filter_data:
            car_id = x.car_id
            busline = x.link
        models.unionpay_log.objects.filter(tty=tty).update(car_id=car_id, bus_line=busline)


def batch_get_xls():  # 批量下载
    host = '218.19.140.180'
    port = 990
    user = '004-KPZHGJ'
    password = 'cFbLzxU!MQGE'

    myFtps = FTPTLS()
    myFtps.logLevel = 2
    myFtps.openSession(host, port, user, password)

    day1 = '20200101'
    start = datetime.strptime(day1, '%Y%d%m').date()
    end = datetime.today().date() - timedelta(days=3)   # 当天日期的前3天

    for dt in rrule(DAILY, dtstart=start, until=end):
        date_str = dt.date().strftime('%Y%m%d')
        ftp_path = '/' + date_str
        xls_name = 'KPZHGJ_' + date_str + '.xls'
        file_path = './download/' + xls_name
        file_name = 'RETR ' + xls_name
        myFtps.cwd(ftp_path)
        bufsize = 1024
        file_handle = open(file_path, 'wb').write
        filename = file_name
        myFtps.retrbinary(filename, file_handle, bufsize)
        time.sleep(3)

    myFtps.closeSession()


def batch_create_log():
    day1 = '20200101'
    start = datetime.strptime(day1, '%Y%d%m').date()
    end = datetime.today().date() - timedelta(days=3)

    for dt in rrule(DAILY, dtstart=start, until=end):
        date_str = dt.date().strftime('%Y%m%d')
        xls_name = 'KPZHGJ_' + date_str + '.xls'
        file_path = './download/' + xls_name
        excel_obj = xlrd.open_workbook(file_path).sheet_by_name('1')
        time.sleep(1)
        dt = models.unionpay_log.__doc__
        title_list = dt[dt.find('(') + 1:dt.find(')')].split(",")
        title_list.pop(0)

        for item in range(1, excel_obj.nrows):
            dic = {}
            item_row = excel_obj.row_values(item)
            settlement_date = datetime.strptime(item_row[0], "%Y%m%d").strftime("%Y-%m-%d")  # 格式化第一列的日期格式
            settlement_time = datetime.strptime(item_row[3], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

            for col in range(0, excel_obj.ncols):
                dic[title_list[0].strip()] = settlement_date
                dic[title_list[3].strip()] = settlement_time
                dic[title_list[col].strip()] = item_row[col]
            print(dic)
            models.unionpay_log.objects.create(**dic)


# batch_create_log()
updata_log()
# day1 = '20200101'
# start = datetime.strptime(day1, '%Y%m%d').date()
# end = (datetime.today().date() - timedelta(days=3))
# for dt in rrule(DAILY, dtstart=start, until=end):
#     date_str = dt.date().strftime('%Y%m%d')
#     ftp_path = '/' + date_str
#     xls_name = 'KPZHGJ_' + date_str + '.xls'
#     file_path = './download/' + xls_name
#     file_name = 'RETR ' + xls_name
#     print(ftp_path)
#     print(file_path)
#     print(file_name)
# print(start)
# print(end)
# for dt in rrule(DAILY, dtstart=start, until=end):
#     print(dt.date().strftime("%Y%m%d"))
