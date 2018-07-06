# -*- coding: utf-8 -*-
import scrapy
from jianshu_article.items import JianshuArticleItem


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    user_id = "1b4c832fb2ca" #替换此用户ID可获取你需要的数据，或者放开下一行的注释
    #user_id = input('请输入作者id：\n')
    url = "https://www.jianshu.com/u/{0}?page=1".format(user_id)
    start_urls = [
        url,
    ]

    def parse(self, response):
        # [关注,粉丝,文章]
        a = response.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li/div/a/p/text()').extract()
        print(a)
        # [字数,收获喜欢]
        b = response.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li/div/p/text()').extract()
        print(b)
        # 大头像
        c = response.xpath('//div[@class="main-top"]/a[@class="avatar"]/img/@src').extract_first()
        print(c)
        # 用户名
        d = response.xpath('//div[@class="main-top"]/div[@class="title"]/a/text()').extract_first()
        print(d)
        # 性别
        e = response.xpath('//div[@class="main-top"]/div[@class="title"]/i/@class').extract_first()
        print(e)

        # 获取文章总数，计算页数。（简书网站默认每页是9组数据）
        temp = int(a[2])
        if (temp % 9 > 0):
            count = temp // 9 + 1
        else:
            count = temp // 9
        print("总共" + str(count) + "页")

        base_url = "https://www.jianshu.com/u/{0}?page={1}"
        for i in range(1, count + 1):
            i = count + 1 - i  #理论上正序1~count就是按顺序获取的，但是获取的数据是倒置的，所以我们获取count~1的数据，得到的数组就是按照网页形式1~count页码排序的了
            yield scrapy.Request(base_url.format(self.user_id, i), dont_filter=True, callback=self.parse_page)

    #迭代返回每页的内容
    def parse_page(self, response):
        for sel in response.xpath('//div[@id="list-container"]/ul/li'):
            item = JianshuArticleItem()
            item['wrap_img'] = sel.xpath('a/img/@src').extract_first()
            item['avatar'] = sel.xpath('div//a[@class="avatar"]/img/@src').extract_first()
            item['nickname'] = sel.xpath('div//a[@class="nickname"]/text()').extract_first()
            item['time'] = sel.xpath('div//span[@class="time"]/@data-shared-at').extract_first()
            item['title'] = sel.xpath('div/a[@class="title"]/text()').extract_first()
            item['abstract'] = sel.xpath('div/p[@class="abstract"]/text()').extract_first()
            item['read'] = sel.xpath('div/div[@class="meta"]/a[1]/text()').extract()[1]
            item['comments'] = sel.xpath('div/div[@class="meta"]/a[2]/text()').extract()[1]
            item['like'] = sel.xpath('div/div[@class="meta"]/span/text()').extract_first()
            item['detail'] = sel.xpath('div/a[@class="title"]/@href').extract_first()
            yield item
