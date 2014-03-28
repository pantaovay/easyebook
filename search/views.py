#coding:utf-8
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from spider.models import OriginBook
import json
from django.http import HttpResponse
def search(request):
    if 'q' in request.GET:
        q = request.GET['q'].strip()
        if len(q) > 20:
            return render_to_response('hello.html')
        book_all = OriginBook.objects.all().filter(name__istartswith=q).order_by('name', 'price')
        #book_all = OriginBook.objects.all().filter(name__icontains=q)
        num = book_all.__len__()
        page_num = 5
        before_page_num = 4
        after_page_num = 4
        paginator = Paginator(book_all, page_num)
        try:
            page = int(request.GET.get('page', '1'))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        if page >= after_page_num:
            page_range = paginator.page_range[page - after_page_num : page + before_page_num]
        else:
            page_range = paginator.page_range[:page + before_page_num]
        try:
            books = paginator.page(page)
        except (EmptyPage, InvalidPage), e:
            books = paginator.page(paginator.num_pages)
            print e
        return render_to_response('result.html', {'books': books, 'query': q, 'num': num, 'page_range': page_range})
    else:
        return render_to_response('hello.html')
def query(request):
    from django.core import serializers
    if 'q' in request.GET:
        q = request.GET['q'].strip()
        books = OriginBook.objects.filter(name__icontains=q)
        return HttpResponse(serializers.serialize('json', books))
    else:
        error = "{'error' : false}"
        return HttpResponse(json.dumps(error))
