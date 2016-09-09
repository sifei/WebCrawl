# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from EcigForum.items import EcigforumItem
from scrapy.exceptions import CloseSpider
import re

class EcigSpider(scrapy.Spider):
    name = "Ecig"
    allowed_domains = ["e-cigarette-forum.com"]
    start_urls = (
        'https://www.e-cigarette-forum.com/forum/',
    )

    def parse(self, response):
        items = response.xpath("//ol[@class='nodeList sectionMain']/li")
        for item in items:
            for i in item.xpath('./ol/li'):
                url = i.xpath("./div/div[@class='nodeText']/h3/a/@href").extract_first()
                forum_name = i.xpath("./div/div[@class='nodeText']/h3/a/text()").extract_first().strip()
                yield Request('http://www.e-cigarette-forum.com/forum/'+url,callback=lambda response, forum=forum_name: self.parse_thread(response,forum))

    def parse_thread(self, response, forum):
        check_subforum = response.xpath("//ol[@class='nodeList sectionMain']")
        if check_subforum is not None:
            for item in response.xpath("//ol[@class='nodeList sectionMain']/li"):
                forum_name = item.xpath("./div/div[@class='nodeText']/h3/a/text()").extract_first().strip()
                yield Request('http://www.e-cigarette-forum.com/forum/'+item.xpath("./div/div[@class='nodeText']/h3/a/@href").extract_first(), callback=lambda response, forum=forum_name: self.parse_thread(response,forum))
        items = response.xpath("//ol[@class='discussionListItems']/li")
        for item in items:
            threadID = item.xpath("./@id").extract_first().split('-')[-1]
            yield Request('https://www.e-cigarette-forum.com/forum/'+item.xpath("./div[@class='listBlock main']/div[@class='titleText']/h3/a/@href").extract_first(), callback=lambda response, typeid=threadID, forum=forum: self.parse_post(response, typeid, forum))

        try:
            next_page = response.xpath("//div[@class='PageNav']/nav/a[@class='text']/@href").extract()[-1]
            forum_name = next_page.split('/')[1]
            if next_page is not None:
                yield Request('https://www.e-cigarette-forum.com/forum/'+next_page, callback=lambda response, forum=forum_name: self.parse_thread(response,forum))
        except:
            pass
    def parse_post(self, response, typeid, forum):
        title = response.xpath("//div[@class='titleBar']/h1/text()").extract_first().strip()
        items = response.xpath("//ol/li")
        for item in items:
            postInfo = EcigforumItem()
            postInfo['forum_name'] = forum
            postInfo['threadID'] = typeid
            postInfo['title'] = title
            postInfo['postID'] = item.xpath("./@id").extract_first().split('-')[-1]
            postInfo['username'] = item.xpath("./@data-author").extract_first()
            postInfo['userTitle'] = item.xpath(".//div[@class='messageUserInfo']/div/h3/em[@class='userTitle']/text()").extract_first().strip()
            postInfo['content'] = item.xpath(".//div[@class='messageInfo primaryContent']/div/article/blockquote[@class='messageText SelectQuoteContainer ugc baseHtml']/descendant::text()").extract_first().strip()
            postInfo['userJoinDate'] = item.xpath(".//div[@class='messageUserInfo']/div/div[@class='extraUserInfo xbBoxedFA']/dl[@class='pairsJustified xbJoinDate']/dd/text()").extract_first().encode('utf8','ignore')
            postInfo['userLocation'] = item.xpath(".//div[@class='messageUserInfo']/div/div[@class='extraUserInfo xbBoxedFA']/dl[@class='pairsJustified xbLocation']/dd/a/text()").extract_first()
            postInfo['time'] = item.xpath(".//div[@class='messageInfo primaryContent']/div[@class='messageMeta ToggleTriggerAnchor']/div[@class='privateControls hiddenResponsiveMedium hiddenResponsiveNarrow']/span/a/abbr/@data-datestring").extract_first()
            if postInfo['time'] == None:
                postInfo['time'] = item.xpath(".//div[@class='messageInfo primaryContent']/div[@class='messageMeta ToggleTriggerAnchor']/div[@class='privateControls hiddenResponsiveMedium hiddenResponsiveNarrow']/span/a/span/text()").extract_first()
            print postInfo['postID']
            yield postInfo
        try:
            next_page = response.xpath("//div[@class='PageNav']/nav/a[class='text']/@href").extract_first()
            if next_page is not None:
                yield Request('https://www.e-cigarette-forum.com/forum/'+next_page, self.parse_post)
        except:
            pass
