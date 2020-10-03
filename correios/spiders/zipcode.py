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

    def __init__(self, state='', *args, **kwargs):
        super(ZipCodeSpider, self).__init__(*args, **kwargs)
        self.state = state

    def start_requests(self):
        if not self.state:
            raise Exception('Pass a valid state "-a state=SC"')

        option = Options()
        option.headless = True

        driver = webdriver.Firefox(options=option)
        driver.get(self.start_urls[0])

        driver.find_element_by_xpath(f'//div[@class="contentform"]//select//option[text()="{self.state}"]').click()
        driver.find_element_by_xpath('//*[@id="Geral"]/div/div/span[3]/label/a').click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        number_of_letters = len(driver.find_elements_by_xpath(f'//*[@id="Geral"]/div/div/span/a'))

        for index in range(number_of_letters):
            index += 1
            driver.find_element_by_xpath(f'//*[@id="Geral"]/div/div/span/a[{index}]').click()

            with open(f'./correios/webpages/page{index}.html', 'w') as page_html:
                page_html.write(driver.page_source)

            file_path = f'file:///home/david/Pessoal/neoway/correios/correios/webpages/page{index}.html'

            yield scrapy.Request(file_path, callback=self.parse)

            driver.back()
            time.sleep(1)

        driver.quit()

    def parse(self, response):
        item = CorreiosItem()

        for tr in response.css('tbody tr')[1:].getall():
            tr = ''.join(tr.split('\t'))
            try:
                tr = tr.encode(response.encoding).decode()
            except:
                tr = tr.encode('utf-8').decode()

            city = re.findall('value="(.*?)"', tr)
            zip_code = re.findall('[0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9]', tr)

            item['localidade'] = city[0]
            item['faixa_de_cep'] = zip_code[0] if zip_code else '-'
            yield item
