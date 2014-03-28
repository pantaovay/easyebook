#coding: utf-8
#工具类
from spider.models import TotalPage, OriginBook
from sae.storage import Bucket, Connection
from bs4 import BeautifulSoup
import datetime, urllib2, re, json, hashlib, math

class Tool:
    def __init__(self):
        self.amazonUrlMap = dict(
            xiaoshuo = '144154071&bbn=144154071&ie=UTF8&qid=1377705794',
            wenxue = '144180071&bbn=116169071&ie=UTF8&qid=1377706146',
            yishuyusheying = '143174071&bbn=116169071&ie=UTF8&qid=1377706210',
            zhuanji = '143175071&bbn=116169071&ie=UTF8&qid=1377706210',
            lizhiyuchenggong = '143192071&bbn=116169071&ie=UTF8&qid=1377706210',
            kaoshi = '143193071&bbn=116169071&ie=UTF8&qid=1377706210',
            jingjiguanli = '143231071&bbn=116169071&ie=UTF8&qid=1377706210',
            jiaocaijiaofu = '143215071&bbn=116169071&ie=UTF8&qid=1377706210',
            shaoer = '143276071&bbn=116169071&ie=UTF8&qid=1377706210',
            yunchanyuer = '143290071&bbn=116169071&ie=UTF8&qid=1377706210',
            jiatingjiaoyu = '143291071&bbn=116169071&ie=UTF8&qid=1377706826',
            shishang = '143254071&bbn=116169071&ie=UTF8&qid=1377706826',
            yule = '143267071&bbn=116169071&ie=UTF8&qid=1377706826',
            jiankangyangsheng = '143292071&bbn=116169071&ie=UTF8&qid=1377706826',
            jiajuxiuxian = '143293071&bbn=116169071&ie=UTF8&qid=1377706826',
            lvyouditu = '143304071&bbn=116169071&ie=UTF8&qid=1377706826',
            dongmanhuiben = '143305071&bbn=116169071&ie=UTF8&qid=1377706826',
            pengrenmeishi = '143306071&bbn=116169071&ie=UTF8&qid=1377706826',
            yingyuwaiyu = '143324071&bbn=116169071&ie=UTF8&qid=1377706826',
            hunlianliangxing = '143354071&bbn=116169071&ie=UTF8&qid=1377707089',
            jisuanjihulianwang = '143359071&bbn=116169071&ie=UTF8&qid=1377707089',
            shehuikexue = '143381071&bbn=116169071&ie=UTF8&qid=1377707089',
            falv = '143387071&bbn=116169071&ie=UTF8&qid=1377707089',
            xinlixue = '143411071&bbn=116169071&ie=UTF8&qid=1377707089',
            lishi = '143428071&bbn=116169071&ie=UTF8&qid=1377707089',
            guoxue = '143442071&bbn=116169071&ie=UTF8&qid=1377707089',
            zhexuezongjiao = '143452071&bbn=116169071&ie=UTF8&qid=1377707089',
            zhengzhijunshi = '143468071&bbn=116169071&ie=UTF8&qid=1377707089',
            yixue = '143478071&bbn=116169071&ie=UTF8&qid=1377707291',
            kexueziran = '143509071&bbn=116169071&ie=UTF8&qid=1377707291',
            keji = '143528071&bbn=116169071&ie=UTF8&qid=1377707291',
            tiyuyundong = '143552071&bbn=116169071&ie=UTF8&qid=1377707291',
            cidiangongjushu = '143553071&bbn=116169071&ie=UTF8&qid=1377707291',
            qikanzazhi = '143579071&bbn=116169071&ie=UTF8&qid=1377707291',
            shijiejingdian = '116170071&bbn=116169071&ie=UTF8&qid=1377707291'
        )

        self.amazonUrlBase = 'http://www.amazon.cn/s/?rh=n%3A116087071%2Cn%3A!116088071%2Cn%3A116169071%2Cn%3A'
        self.amazonUrlTail = '&lo=none&page='

        self.duokanUrl = 'http://www.duokan.com/%E5%85%A8%E9%83%A8%E5%9B%BE%E4%B9%A6/c/1-'
        self.doubanUrl = 'http://read.douban.com/category/all/?cat=all&sort=top&start='
        self.ikandouUrl = 'http://ikandou.com/g/popular/?page='

        self.defaults = {
            'name': '',
            'author': '',
            'price': 0,
            'rate': 0,
            'rate_num': 0,
            'update_time': datetime.datetime.now(),
            'image_url': '',
            'url': ''
        }

    def saveTotal(self):
        sites = ['amazon', 'duokan', 'douban', 'ikandou']
        p = TotalPage()
        for site in sites:
            if site == 'amazon':
                #nums = self.resolvePageTotalAmazon()
                nums = self.resolvePageTotalAmzonNew()
                p.amazon = json.dumps(nums)
            else:
                url = getattr(self, site + 'Url')
                if site == 'douban':
                    url += '0'
                else:
                    url += '1'
                page = self.getPage(url)
                num = self.resolvePageTotalExceptAmazon(page, site)
                if hasattr(p, site):
                    setattr(p, site, num)
        p.update_time = datetime.datetime.now()
        p.save()

    # 基础获得页面的函数
    def getPage(self, url, header={}):
        try:
            request = urllib2.Request(url, headers=header)
            #sae默认超时是5s
            response = urllib2.urlopen(request, timeout= 5)
            return response.read()
        except Exception, e:
            print e
        return

    # 封装解析页面函数
    def resolvePage(self, page, site):
        getattr(self, 'resolvePage' + site.capitalize())(page)

    def resolvePageAmazon(self, page):
        soup = BeautifulSoup(page)
        books = soup.select('div[id^="result_"]')
        for book in books:
            url = book.select('h3.newaps > a')[0]['href']
            url_hash = hashlib.sha1(url).hexdigest()
            amazonbook, created = OriginBook.objects.get_or_create(url_hash=url_hash, source='amazon', defaults=self.defaults)
            if created == False:
                amazonbook.update_time = datetime.datetime.now()
            amazonbook.url = url
            name = book.select('h3.newaps > a > span.lrg')
            if name:
                amazonbook.name = name[0].get_text().strip()
            author = book.select('h3.newaps > span.med')
            if author:
                amazonbook.author = author[0].get_text().strip()
            rawstr = r"""<span\s+class=".*?bld.*?">\s*￥(?P<price>.*?)</span>"""
            compile_obj = re.compile(rawstr)
            match_obj = compile_obj.search(str(book))
            if match_obj:
                amazonbook.price = match_obj.group('price')
            rawstr = r"""平均(?P<score>.*?)星"""
            compile_obj = re.compile(rawstr)
            match_obj = compile_obj.search(str(book))
            if match_obj:
                amazonbook.rate = match_obj.group('score')
            rawstr = r"""<a.*?href="http://www.amazon.cn/.*?product-reviews/.*?">(?P<amount>.*?)条评论</a>"""
            compile_obj = re.compile(rawstr)
            match_obj = compile_obj.search(str(book))
            if match_obj:
                amount = match_obj.group('amount')
            else:
                amount = 0
            amazonbook.rate_num = self.dealNum(amount)
            rawstr = r"""<img.*?class="productImage"\s+src="(?P<img_url>.*?)"/></a>"""
            compile_obj = re.compile(rawstr)
            match_obj = compile_obj.search(str(book))
            if match_obj:
                amazonbook.image_url = match_obj.group('img_url')
            amazonbook.save()

    def resolvePageDuokan(self, page):
        soup = BeautifulSoup(page)
        books = soup.select('ul.j-list > li.w-bookitm')
        for book in books:
            cover = book.select('div.cover')[0]
            info = book.select('div.info')[0]
            url = cover.select('div.img > a')[0]['href']
            url_hash = hashlib.sha1(url).hexdigest()
            duokanbook, created = OriginBook.objects.get_or_create(url_hash=url_hash, source='duokan', defaults=self.defaults)
            if created == False:
                duokanbook.update_time = datetime.datetime.now()
            duokanbook.url = url
            duokanbook.image_url = cover.select('div.img > a > img')[0]['src']
            duokanbook.name = info.select('div.wrap > a.title')[0].get_text().strip()
            duokanbook.rate = info.select('div.w-starfive > span[itemprop="ratingValue"]')[0].get_text().strip()
            if info.select('div.w-starfive > span.num > span[itemprop="reviewCount"]'):
                duokanbook.rate_num = info.select('div.w-starfive > span.num > span[itemprop="reviewCount"]')[0].get_text().strip()
            duokanbook.author = info.select('p.author > span')[0].get_text().strip()
            price = cover.select('div.w-price > em')
            if price:
                price = price[0].get_text().split()[1]
            else:
                price = 0
            duokanbook.price = price
            duokanbook.save()

    def resolvePageDouban(self, page):
        soup = BeautifulSoup(page)
        books = soup.select('ul.ebook-list > li[id^="ebook-"]')
        for book in books:
            url = book.select('div.cover > a.pic')[0]['href']
            url_hash = hashlib.sha1(url).hexdigest()
            doubanbook, created = OriginBook.objects.get_or_create(url_hash=url_hash, source='douban', defaults=self.defaults)
            if created == False:
                doubanbook.update_time = datetime.datetime.now()
            doubanbook.url = url
            doubanbook.name = self.soupSelect(book, 'div.info > div.title > a')
            doubanbook.price = book.select('div.info > div.article-actions')[0]['data-readable-price']
            doubanbook.rate = self.soupSelect(book, 'div.info > div.rating > span.rating-average', num=1)

            rawstr = r'<span.*?class="rating-amount">.*?(?P<rate_num>\d+)人评价.*?</span>'
            compile_obj = re.compile(rawstr)
            match_obj = compile_obj.search(str(book))
            if match_obj:
                doubanbook.rate_num = match_obj.group('rate_num')
            doubanbook.image_url = book.select('div.cover > a.pic > img')[0]['src']
            doubanbook.author = self.soupSelect(book, 'span.labeled-text')
            doubanbook.save()

    def resolvePageIkandou(self, page):
        soup = BeautifulSoup(page)
        books = soup.select('ol.mbooks > li[id^="mbook"]')
        for book in books:
            url = book.select('div.mbook-img > a')[0]['href']
            url_hash = hashlib.sha1(url).hexdigest()
            ikandoubook, created = OriginBook.objects.get_or_create(url_hash=url_hash, source='ikandou', defaults=self.defaults)
            if created == False:
                ikandoubook.update_time = datetime.datetime.now()
            ikandoubook.url = url
            ikandoubook.image_url = book.select('div.mbook-img > a > img')[0]['src']
            ikandoubook.name = self.soupSelect(book, 'h5 > a')
            rawstr = r"""<h5>.*?</a>(?P<author>.*?)</h5>"""
            compile_obj = re.compile(rawstr)
            match_obj = compile_obj.search(str(book))
            if match_obj:
                ikandoubook.author = match_obj.group('author')
            ikandoubook.save()

    # 解析全部页数
    def resolvePageTotalExceptAmazon(self, page, site):
        if site == 'duokan':
            rawstr = r"""<li class="ellipsis">.*?</li>.*?<li class="">.*?<a.*?>(?P<num>\d+)</a>"""
            match_obj = re.compile(rawstr, re.MULTILINE | re.DOTALL).search(page)
            if match_obj:
                return match_obj.group('num')
            else:
                return 0
        elif site == 'douban':
            rawstr = r""">(?P<num>\d+)</a></li>(?=<li class="next">.*?<a.*?>.*?</a>)"""
            match_obj = re.compile(rawstr, re.MULTILINE | re.DOTALL).search(page)
            if match_obj:
                return match_obj.group('num')
            else:
                return 0
        elif site == 'ikandou':
            rawstr = r""">(?P<num>\d+)</a>\s*(=?<a href="\?page=2" class="next">.*?</a>)"""
            match_obj = re.compile(rawstr, re.MULTILINE | re.DOTALL).search(page)
            if match_obj:
                return match_obj.group('num')
            else:
                return 0
        else:
            return 0

    # amazon分类获取
    def resolvePageTotalAmazon(self):
        nums = dict()
        for key, value in self.amazonUrlMap.iteritems():
            page = self.getPage(self.amazonUrlBase + value + self.amazonUrlTail + '1')
            rawstr = r"""<span class="pagnDisabled">(?P<num>\d+)</span>"""
            compile_obj = re.compile(rawstr)
            match_obj = compile_obj.search(page)
            if match_obj:
                num = match_obj.group('num')
            else:
                num = 0
            nums[key] = num
        return nums

    # amazon 分类获取页面新的计算方法
    def resolvePageTotalAmzonNew(self):
        nums = dict()
        for key, value in self.amazonUrlMap.iteritems():
            page = self.getPage(self.amazonUrlBase + value + self.amazonUrlTail + '1')
            rawstr = r"""<div class="topBarCol"><h2 class="resultCount" id="resultCount"><span>显示.*?共(?P<num>\d+)条</span>"""
            compile_obj = re.compile(rawstr)
            match_obj = compile_obj.search(page)
            if match_obj:
                num = match_obj.group('num')
            else:
                num = 0
            nums[key] = int(math.ceil(float(num) / 48))
        return nums


    # 保存页面到storage中
    def savePageExceptAmazon(self, site, id):
        url = getattr(self, site + 'Url')
        if site == 'douban':
            url += str( (int(id) - 1) * 10 )
        else:
            url += str(id)
        page = self.getPage(url)
        try:
            conn = Connection(accesskey='ym51nzx10z', secretkey='h0kxmzj2ly13jjj1m0jjly41li1wimizzz2w2m32', retries=3)
            spider = Bucket(site, conn)
            spider.put_object(str(id), page)
        except Exception, e:
            print e

    def savePageAmazon(self, params):
        url = self.amazonUrlBase + self.amazonUrlMap.get(params['category']) + self.amazonUrlTail + params['id']
        page = self.getPage(url)
        try:
            conn = Connection(accesskey='ym51nzx10z', secretkey='h0kxmzj2ly13jjj1m0jjly41li1wimizzz2w2m32', retries=3)
            spider = Bucket('amazon', conn)
            spider.put_object(params['category'] + '/' + params['id'], page)
        except Exception, e:
            print e

    # 解析页面将书入库
    def inPage(self, site, filename):
        try:
            conn = Connection(accesskey='ym51nzx10z', secretkey='h0kxmzj2ly13jjj1m0jjly41li1wimizzz2w2m32', retries=3)
            bucket = Bucket(site, conn)
            page = bucket.get_object_contents(filename)
        except Exception, e:
            print e
        self.resolvePage(page, site)

    def inPageAmazon(self, params):
        try:
            conn = Connection(accesskey='ym51nzx10z', secretkey='h0kxmzj2ly13jjj1m0jjly41li1wimizzz2w2m32', retries=3)
            bucket = Bucket('amazon', conn)
            page = bucket.get_object_contents(params['category'] + '/' + params['in_page'])
        except Exception, e:
            print e
        self.resolvePage(page, 'amazon')

    # 超过三个数字去掉,
    def dealNum(self, num):
        nums = str(num).split(',')
        return ''.join(nums)

    def soupSelect(self, book, pattern, num = 0):
        result = book.select(pattern)
        if result:
            return result[0].get_text().strip()
        elif num == 1:
            return 0
        else:
            return ''



    # 字符串距离
    def levenshtein(self, s1, s2):
        l1 = len(s1)
        l2 = len(s2)
        matrix = [range(l1 + 1)] * (l2 + 1)
        for zz in range(l2 + 1):
            matrix[zz] = range(zz,zz + l1 + 1)
        for zz in range(0, l2):
            for sz in range(0, l1):
                if s1[sz] == s2[zz]:
                    matrix[zz + 1][sz + 1] = min(matrix[zz + 1][sz] + 1, matrix[zz][sz + 1] + 1, matrix[zz][sz])
                else:
                    matrix[zz + 1][sz + 1] = min(matrix[zz + 1][sz] + 1, matrix[zz][sz + 1] + 1, matrix[zz][sz] + 1)
        return matrix[l2][l1]
