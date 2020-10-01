import scrapy
import time
import os
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from correios.items import CorreiosItem



class ZipCodeSpider(scrapy.Spider):
    name = 'zip_code'

    start_urls = [
        'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm'
    ]

    def start_requests(self):
        option = Options()
        option.headless = True

        driver = webdriver.Firefox(options=option)
        driver.get(self.start_urls[0])

        driver.find_element_by_xpath('//div[@class="contentform"]//select//option[text()="SC"]').click()
        driver.find_element_by_xpath('//*[@id="Geral"]/div/div/span[3]/label/a').click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        driver.find_element_by_xpath(f'//*[@id="Geral"]/div/div/span/a[1]').click()

        with open('./correios/webpages/page.html', 'w') as page_html:
            page_html.write(driver.page_source)

        file_path = 'file:///home/david/Pessoal/neoway/correios/correios/webpages/page.html'

        yield scrapy.Request(file_path, callback=self.parse)

        driver.quit()

    def parse(self, response):
        item = CorreiosItem()

        for tr in response.css('tbody tr')[1:].getall():
            tr = ''.join(tr.split('\t'))

            city = re.findall('value="(.*?)"', tr)
            zip_code = re.findall('[0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9]', tr)
            
            item['city'] = city
            if zip_code:
                item['zip_code'] = zip_code
            else:
                item['zip_code'] = '-'
            
            yield item
