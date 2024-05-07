import scrapy
from bs4 import BeautifulSoup
from scrapy import FormRequest
import requests
import json
from AISpider.items.geelongaustralia_items import Geelongaustralia
import time
from datetime import datetime   

class GeelongaustraliaSpider(scrapy.Spider):
    name = "geelongaustralia"
    # allowed_domains = ["geelongaustralia"]
    start_urls = ["https://www.geelongaustralia.com.au/planningregister/default.aspx"]
    custom_settings = {
        'LOG_STDOUT': True,
        #'LOG_FILE': 'scrapy_geelongaustraliaSpider.log',
        'DOWNLOAD_TIMEOUT': 1200
    }
    
    def __init__(self, *args, **kwargs):
        super(GeelongaustraliaSpider, self).__init__(*args, **kwargs)
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cache-Control': 'no-cache',
            'Host': 'www.geelongaustralia.com.au',
            'Connection': 'keep-aliv'
        }
        self.cookies={

        }
        self.url_interface1 = 'https://www.geelongaustralia.com.au/planningregister/default.aspx'
        self.proxy = {'https': 'http://127.0.0.1:8888'}

    def deal_formdata(self, response,page_num):
        soup = BeautifulSoup(response.text,'html.parser')
        __VIEWSTATE = str(soup).split('__VIEWSTATE')[1].split('|')[1]
        __VIEWSTATEGENERATOR = str(soup).split('__VIEWSTATEGENERATOR')[1].split('|')[1]
        __EVENTVALIDATION = str(soup).split('__EVENTVALIDATION')[1].split('|0|')[0].strip('|')
        formdata ={
            'ctl00$bootstrapSM': 'ctl00$ContentBody$UpdatePanel1|ctl00$ContentBody$GV_CURRENT',
            'ctl00$ctl13$TB_Search': '',
            'ctl00$ctl13$TB_Search_M': '',
            'ctl00$ContentBody$RBL1': 'Yes',
            'ctl00$ContentBody$DD_LOCATION': 'All locations',
            'ctl00$ContentBody$DD_DECISION': 'All decisions',
            'ctl00$ContentBody$DD_VCAT': 'All VCAT decisions',
            '__EVENTTARGET': 'ctl00$ContentBody$GV_CURRENT',
            '__EVENTARGUMENT': f'Page${page_num}',
            '__LASTFOCUS':'' ,
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': __EVENTVALIDATION,
            '__ASYNCPOST': 'true',
        }
        return formdata

    def deal_first_formdata(self, response):
        soup = BeautifulSoup(response.text,'html.parser')
        __VIEWSTATE = soup.select_one('#__VIEWSTATE').get('value')
        __VIEWSTATEGENERATOR = soup.select_one('#__VIEWSTATEGENERATOR').get('value')
        __EVENTVALIDATION = soup.select_one('#__EVENTVALIDATION').get('value')
        formdata ={
            'ctl00$bootstrapSM': 'ctl00$ContentBody$UpdatePanel1|ctl00$ContentBody$RBL1$0',
            '__EVENTTARGET': 'ctl00$ContentBody$RBL1$0',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTVALIDATION':__EVENTVALIDATION,
            'ctl00$ctl13$TB_Search': '',
            'ctl00$ctl13$TB_Search_M':'' ,
            'ctl00$ContentBody$RBL1': 'Yes',
            '__ASYNCPOST': 'true',
        }
        return formdata

    def parse(self, response):
        self.cookies = {
            'ASP.NET_SessionId':str(response.headers.get('Set-Cookie')).split('=')[1].split(';')[0]
        }
        from_data = self.deal_first_formdata(response)
        resp = requests.post(url=self.url_interface1,data=from_data,headers=self.headers)
        for item in self.deal_data(resp,1):
            yield item
        page_num = 2
        while True:
            if page_num :
                from_data = self.deal_formdata(resp,page_num=page_num)
                resp = requests.post(url=self.url_interface1,data=from_data,headers=self.headers)
                for item in self.deal_data(resp,page_num):
                    yield item
                page_num +=1

    def deal_data(self,response,page_num):
        print(f'第{page_num}页')
        item = Geelongaustralia()
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.select('#ctl00_ContentBody_GV_CURRENT td')
        temp_list = []
        num = 0
        for i in tables:
            temp_list.append(i.get_text().replace('\n','').replace('\r','').replace('\t','').replace('\xa0','').replace(' ',''))
            if len(temp_list)== 14 and num != 0:
                # print(temp_list)
                item['app_num'] = temp_list[0]
                item['vic_smart'] = temp_list[1]

                lodged_date = temp_list[2]
                item['lodge_date'] = datetime.strptime(lodged_date, '%d/%m/%Y') if lodged_date else 0   

                item['address'] = temp_list[3]
                item['description'] = temp_list[4]
                item['changes_'] = temp_list[5]
                item['type_'] = temp_list[6]

                lodged_date = temp_list[7]
                item['notice_date'] = datetime.strptime(lodged_date, '%d/%m/%Y') if lodged_date else 0  
                item['authority'] = temp_list[8]

                lodged_date = temp_list[9]
                item['decision_date'] = datetime.strptime(lodged_date, '%d/%m/%Y') if lodged_date else 0  
                item['decision'] = temp_list[10]

                item['vc_refno'] = temp_list[11]
                item['vc_decision'] = temp_list[12]

                lodged_date = temp_list[13]
                item['vc_date'] = datetime.strptime(lodged_date, '%d/%m/%Y') if lodged_date else 0  
                item['metadata']={}
                del item['metadata']
                yield item
                time.sleep(0.5)
                temp_list = []  
            num += 1
        



