#coding: utf-8
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    update_time = models.DateTimeField()
    image_url = models.URLField(max_length=4000)
    def __unicode__(self):
        return self.name

class Url(models.Model):
    book = models.ForeignKey(Book)
    amazon = models.URLField(max_length=4000)
    duokan = models.URLField(max_length=4000)
    douban = models.URLField(max_length=4000)
    ikandou = models.URLField(max_length=4000)
    def __unicode__(self):
        return self.book.name

class Price(models.Model):
    book = models.ForeignKey(Book)
    amazon = models.FloatField()
    duokan = models.FloatField()
    douban = models.FloatField()
    ikandou = models.FloatField()
    def __unicode__(self):
        return self.book.name

class Rate(models.Model):
    book = models.ForeignKey(Book)
    amazon = models.FloatField()
    amazon_num = models.IntegerField()
    duokan = models.FloatField()
    duokan_num = models.IntegerField()
    douban = models.FloatField()
    douban_num = models.IntegerField()
    ikandou = models.FloatField()
    ikandou_num = models.IntegerField()
    def __unicode__(self):
        return self.book.name

class TotalPage(models.Model):
    amazon = models.CharField(max_length=1000)
    duokan = models.IntegerField()
    douban = models.IntegerField()
    ikandou = models.IntegerField()
    update_time = models.DateTimeField()
    def __unicode__(self):
        return self.amazon

class OriginBook(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    rate = models.FloatField()
    rate_num = models.IntegerField()
    source = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    image_url = models.URLField(max_length=4000)
    url = models.URLField(max_length=4000)
    url_hash = models.CharField(max_length=40, primary_key=True)
    def __unicode__(self):
        return self.name
