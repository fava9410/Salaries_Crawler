from crawler import Crawler
import requests
from lxml import html
import json
import re
import csv
import pandas as pd

class Neuvoo(Crawler):
    cookies = {
        'uet_uuid': '5ddbb1e81c',
        'CUID': 'NYnfc4yiinNh',
    }

    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-User': '?1',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Referer': 'https://neuvoo.com.ar/calculadora-de-impuesto/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'iam': '',
        'uet_calculate': 'calculate',
        'salary': '',
        'from': 'month',
        'region': ''
    }

    def __init__(self, nc_value):
        self.data = []
        self.set_columns = False
        self.columns = ["Salary", "Net pay", "Total tax", "Marginal tax rate", "Average tax rate", "Real tax rate"]

        self.country = nc_value["country"]
        self.salaries = nc_value["salaries"]
        self.url_site = nc_value["url"]

    def formatData(self, tree):
        pago_neto = tree.xpath('//*[@id="deductions"]/div[2]/div[3]/div/div[1]/div[1]/text()')[0]
        impuesto_total = tree.xpath('//*[@id="deductions"]/div[2]/div[3]/div/div[2]/div[1]/text()')[0]
        tasa_tributaria_marginal = tree.xpath('//*[@id="deductions"]/div[2]/div[1]/div[2]/div[5]/div[2]/text()')[0]
        tasa_tributaria_promedio = tree.xpath('//*[@id="deductions"]/div[2]/div[1]/div[2]/div[6]/div[2]/text()')[0]

        deductions_labels = tree.xpath('//*[contains(@class,"taxes")]/div[1]/*/div[1]/text()')
        deductions_values = tree.xpath('//*[contains(@class,"taxes")]/div[1]/*/div[2]/text()')

        deductions_labels.pop(0)
        salario = deductions_values.pop(0)

        tasa_impositiva_real = ''
        picture_url = tree.xpath('//iframe[@data="taxberg-month"]/@src')
        if picture_url != []:
            aux_url = self.url_site.split('/')
            picture_url = 'http://{}{}'.format(aux_url[2], picture_url[0])
            try:
                response = requests.get(picture_url)
                picture_tree = html.fromstring(response.text)
                tasa_impositiva_real = picture_tree.xpath('//*[@id="real-tax-pay"]/div[2]/text()')[0]
            except Exception as e:
                print(e)

        aux_data= [salario, pago_neto, impuesto_total, tasa_tributaria_marginal, tasa_tributaria_promedio, tasa_impositiva_real]

        for i, dec in enumerate(deductions_labels):
            if self.set_columns == False:
                self.columns.append(dec)
            aux_data.append(deductions_values[i][2:])

        self.set_columns = True
        self.data.append(aux_data)

    def run(self):
        for salary in self.salaries:            
            self.params['salary'] = salary
            self.params['region'] = self.country
            self.getConnection()

        self.df = pd.DataFrame(self.data, columns = self.columns)

def clean(f):
    k = f.replace('k','000')
    n = re.findall('[\d]*',k)
    return "".join(n)