# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import Vin
import CheckVin
import os

# 表单


# 解析vin
def vin_parse(request):
    result = {}
    if request.POST:
        vin = request.POST['vin']
        result['vin'] = vin
        if CheckVin.CheckVin().checkVin(vin) is True:
            wmi = str(vin[0:3])
            # 根据wmi查找对应的VIN编码规则JSON文件
            filename = ''
            # JSON 文件目录
            JSON_DIR = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'static\\json')

            dirlist = os.listdir(JSON_DIR)
            for item in dirlist:
                if item.find("_"+wmi) != -1:
                    if item.endswith('.json') is True:
                        filename = item
            try:
                tt = Vin.Vin(os.path.join(JSON_DIR, filename), request.POST['vin'])
                # 动态获取函数名
                fun = filename.split('_')[0]
                fun = 'get'+fun
                result['content'] = getattr(tt, fun)
            except Exception, e:
                result['rlt'] = e.message
        else:
            result['rlt'] = 'VIN码不正确'
    return render(request, "vinparse.html", result)

# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET:
        message = '你搜索的内容为: ' + request.GET['q'].encode('utf-8')
    else:
        message = '你提交了空表单'
    return HttpResponse(message)
