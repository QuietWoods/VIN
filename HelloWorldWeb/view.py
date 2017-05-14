# -*- coding: utf-8 -*-


from django.shortcuts import render

def hello(request):
    context = {}
    athlete_list ={'zhangsan', 'xiaoming','dabaojain'}
    context['hello'] = 'Hello World! In templates'
    context['athlete']= athlete_list
    return render(request, 'hello.html', context)

