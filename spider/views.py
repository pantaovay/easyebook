#coding:utf-8
from django.shortcuts import render_to_response
import spider.util as util

tool = util.Tool()

def amazon(request, category):
    if 'inpage' in request.GET:
        in_page = request.GET['inpage']
        tool.inPageAmazon(dict(category=category, in_page=in_page))
    if 'id' in request.GET:
        id = request.GET['id']
        tool.savePageAmazon(dict(category=category, id=id))
    return render_to_response('hello.html')

def duokan(request):
    if 'inpage' in request.GET:
        in_page = request.GET['inpage']
        tool.inPage('duokan', in_page)
    if 'id' in request.GET:
        id = request.GET['id']
        tool.savePageExceptAmazon('duokan', id)
    return render_to_response('hello.html')

def douban(request):
    if 'inpage' in request.GET:
        in_page = request.GET['inpage']
        tool.inPage('douban', in_page)
    if 'id' in request.GET:
        id = request.GET['id']
        tool.savePageExceptAmazon('douban', id)
    return render_to_response('hello.html')

def ikandou(request):
    if 'inpage' in request.GET:
        in_page = request.GET['inpage']
        tool.inPage('ikandou', in_page)
    if 'id' in request.GET:
        id = request.GET['id']
        tool.savePageExceptAmazon('ikandou', id)
    return render_to_response('hello.html')

def total(request):
    tool.saveTotal()
    return render_to_response('hello.html')