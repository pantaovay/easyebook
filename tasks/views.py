#-*-encoding=utf-8-*-
from django.shortcuts import render_to_response
from spider.models import TotalPage
from sae.taskqueue import Task, TaskQueue
import spider.util as util
import json
import random

tool = util.Tool()
newTotal = TotalPage.objects.order_by('update_time')[0]

def amazon(request):
    categories = json.loads(newTotal.amazon)
    for key, value in categories.iteritems():
        queue = TaskQueue('amazon_' + str(random.randint(1, 7)))
        amazon_total = int(value)
        if 'inpage' in request.GET:
            tasks = [Task('/spider/amazon/' + key + '/?inpage=' + str(inpage)) for inpage in range(1, amazon_total + 1)]
        else:
            tasks = [Task('/spider/amazon/' + key + '/?id=' + str(id)) for id in range(1, amazon_total + 1)]
        queue.add(tasks)
    return render_to_response('hello.html')

def duokan(request):
    duokan_total = newTotal.duokan
    queue = TaskQueue('duokan')
    if 'inpage' in request.GET:
        tasks = [Task('/spider/duokan/?inpage=' + str(inpage)) for inpage in range(1, duokan_total + 1)]
    else:
        tasks = [Task('/spider/duokan/?id=' + str(id)) for id in range(1, duokan_total + 1)]
    queue.add(tasks)
    return render_to_response('hello.html')

def douban(request):
    douban_toal = newTotal.douban
    queue = TaskQueue('douban')
    if 'inpage' in request.GET:
        tasks = [Task('/spider/douban/?inpage=' + str(inpage)) for inpage in range(1, douban_toal + 1)]
    else:
        tasks = [Task('/spider/douban/?id=' + str(id)) for id in range(1, douban_toal + 1)]
    queue.add(tasks)
    return render_to_response('hello.html')

def ikandou(request):
    ikandou_total = newTotal.ikandou
    queue = TaskQueue('ikandou')
    if 'inpage' in request.GET:
        tasks = [Task('/spider/ikandou/?inpage=' + str(inpage)) for inpage in range(1, ikandou_total + 1)]
    else:
        tasks = [Task('/spider/ikandou/?id=' + str(id)) for id in range(1, ikandou_total + 1)]
    queue.add(tasks)
    return render_to_response('hello.html')
