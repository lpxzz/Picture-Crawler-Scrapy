import scrapy
import os,sys
import re
import urllib.request
import time

class nvshen(scrapy.Spider):

    uri = input("请输入网址：")
    name = "nvshen"
    allowed_domains = ["www.nvshens.net","t1.onvshen.com","t1.onvshen.com:85","nvshens.net"]
    start_urls = [
        uri,
    ]

    #选择器
    def parse(self, response):
        yield {"name": response.xpath('//*[@id="htilte"]/text()').extract()} #标题
        #yield {"description": response.xpath('//*[@id="ddesc"]/text()').extract()} #描述
        imgs =  response.xpath('//*[@id="hgallery"]/img/@src[/]').getall() #图片组
        for img in imgs:
            self.createDir(response.xpath('//*[@id="htilte"]/text()').extract(),img)
        nextUrl = response.css(".a1::attr(href)").extract()
        num = nextUrl[1].find("html")
        if num <= 0 :
            print("不存在下一页,爬取完成")
        else :
            print("存在下一页,继续爬取")
            yield scrapy.Request("https://www.nvshens.net/"+nextUrl[1], self.parse)

    #创建文件夹
    def createDir(self,title,img):
        dirName = img.split('/')[5]
        path = os.path.join(os.getcwd(),dirName)
        if os.path.isdir(path) :
            #存在文件夹 下载图片
            self.downloadImg(path,img)
        else : 
            #不存在文件夹，创建
            os.makedirs(path)
            self.downloadImg(path,img)
            
    #下载图片
    def downloadImg(self,path,url):
        fileName = url.split('/')[7] #文件名
        i = time.time()
        urllib.request.urlretrieve(url , path+'/'+fileName)
        print('下载成功,耗时：'+str(int(time.time() - i))+'s')