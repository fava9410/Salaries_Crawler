from crawler import Crawler
import pandas as pd

COOKIE = 'JSESSIONID=D498FDD2EA33B76146D6C8BCA0144B22; GSESSIONID=D498FDD2EA33B76146D6C8BCA0144B22; gdId=0a700ee0-0657-4f12-9627-2a4e009dbf82; trs=direct:direct:direct:2019-09-05+07%3A24%3A28.254:undefined:undefined; _ga=GA1.2.1617134307.1567693471; _gid=GA1.2.1707406240.1567693471; _dc_gtm_UA-2595786-1=1; JSESSIONID_JX_APP=880B19EEE3574DE14D40D3E01909396B; _gcl_au=1.1.1138115249.1567693471; G_ENABLED_IDPS=google; __qca=P0-702509175-1567693472274; _gat_UA-2595786-1=1; _uac=0000016d01d01ae0a0d4fe60e1ee645a; ab.storage.userId.bbafb5ff-3006-4aaf-bbe3-179521353526=%7B%22g%22%3A%22135410154%22%2C%22c%22%3A1567693479264%2C%22l%22%3A1567693479264%7D; ab.storage.deviceId.bbafb5ff-3006-4aaf-bbe3-179521353526=%7B%22g%22%3A%22690e6d1c-4d79-b753-6478-36804a56a4c6%22%2C%22c%22%3A1567693479271%2C%22l%22%3A1567693479271%7D; _mibhv=anon-1567693479381-1718510453_6890; _micpn=esp:-1::1567693479381; uc=D9A9850D0C92C1EF344B33D6D6A738C9D5D2E006C27F512D3873D543ADBEEE801C58488D17FA732F6FA3E551DA33A846D927ABC3ECAB62A115D86225B35B8C90BC3E6AC97B01093B3836F92F9774A76CAC0CC07DE8CB9F9730C0242C0770465E26C47D7E1640610004A8700016A95B892168B804FF1483AE8FBBC7D64AA752698DA756B2EB12071AFB4005556DB9F0E059FC21B24952D19311F9FAB617693261; AWSALB=BEMvblQi57A8zUfn0bH/QHZ0sJiREN5v5BZ+uIkpHVVAQle76frYWWoRyhFpFeBiLWYb0KpH/qfrJr0GRH3KV2wPJ9AdgAL1BXrgYtj/cL1OvbORH/LP9ll+cGLSjBUC9WUdescNMGuGwRDdSc6l6GipdbiVTQCjg74DTpjS+20LRxq0tvSDpMXlv8+hQA==; cass=3; ab.storage.sessionId.bbafb5ff-3006-4aaf-bbe3-179521353526=%7B%22g%22%3A%22a4985038-777d-5bde-6acd-e7728dabf320%22%2C%22e%22%3A1567695288298%2C%22c%22%3A1567693479268%2C%22l%22%3A1567693488298%7D; __cf_bm=3815b56bd26f5c3d655f5c5864cacef94c0f58c7-1567693507-1800-AY90p9Cm32Uxegffru8D2TKERzon1+z8HhbWHCcqV7mFPc/FwdHgNNM133ECbWoMg0qPakTsV3wJAoBmxDOlljo='

class Glassdoor(Crawler):
    headers = {
        'authority': 'www.glassdoor.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'sec-fetch-site': 'same-origin',
        'referer': 'https://www.glassdoor.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'Content-Type':'text/html;charset=UTF-8',
        'cookie': COOKIE
    }

    url_site = 'https://www.glassdoor.com/Salaries/company-salaries.htm'

    titles = ['Junior Software Developer',
        'Backend Developer',
        'Backend Engineer',
        'Senior Backend Engineer',
        'Mobile Developer',
        'Senior Mobile Developer',
        'Frontend Developer',
        'Frontend Engineer',
        'Senior Frontend Developer',
        'Senior Software Engineer',
        'Quality Assurance Tester',
        'Quality Assurance Analyst',
        'Quality Assurance Engineer',
        'Quality Assurance. Technician',
        'Quality Assurance Specialist',
        'Senior Quality Assurance Engineer',
        'UX Designer',
        'Junior UX Designer',
        'Senior UX Designer',
        'UI UX Designer',
        'Devops',
        'Junior Devops Engineer',
        'Senior Devops',
        'Devops Engineer',
        'Senior Devops Engineer',
        'Digital Designer',
        'Senior Digital Designer',
        'Digital Design Engineer',
        'Product Manager',
        'Senior Product Manager',
        'Director Product Manager',
        'Technical Product Manager',
        'Technical Leader',
        'Software Technical Lead',
        'Project Manager',
        'Senior Project Manager',
        'Project Engineer',
        'Technical Project Manager',
        'Process Specialist',
        'Process Analyst',
        'Process Manager',
        'User Experience Designer',
        'Senior Designer',
        'Machine Learning Engineer',
        'Software Architect',
        'Senior Software Architect',
        'Lead Software Architect',
        'Infrastructure Analyst',
        'Software Development Manager',
        'Software Development Engineer'
    ]

    params = {
        'suggestCount': '0',
        'suggestChosen': 'false',
        'clickSource': 'searchBtn',
        'typedKeyword': 'title',
        'sc.keyword': 'title',
        'locT': 'code[0]',
        'locId': 'code[1]',
        'jobType': ''
    }

    columns = ["Country", "Title", "Lower salary", "Higher salary", "Average salary", "Total salaries", "Updated date"]

    def __init__(self, location):
        self.aux_data = []
        self.location = location

    def formatData(self, tree):
        hasResult = tree.xpath('//span[@class="occMedianModule__OccMedianBasePayStyle__payNumber"]')

        if len(hasResult) != 0:
            u = tree.xpath('//span[@class="occMedianModule__OccMedianBasePayStyle__payNumber"]')       
            averageBasePay = u[0].text
            minMax = tree.xpath('//div[@class="common__HistogramStyle__labelWrapper"]')
            min = minMax[0].text
            max = minMax[1].text
            average = tree.xpath('//div[@class="common__HistogramStyle__labelWrapper common__HistogramStyle__avgLabelWrapper center"]/text()')
            total_jobs = tree.xpath('//span[@class="common__spacingHelpers__margRt"]/text()')
            lastUpdated = tree.xpath('//span[@data-test="UpdateDate"]/text()')
            title = tree.xpath('//h1[@data-test="OccMedianHeader"]/text()')
            location = title[0].split('Salaries in ')

            self.aux_data.append([location[1], location[0], min, max, averageBasePay, total_jobs[0], lastUpdated[0]])
    
    def run(self):
        for l in self.location:
            for title in self.titles:
                self.params['typedKeyword'] = title
                self.params['sc.keyword'] = title
                aux_loc = l.split(";")
                self.params['locT'] = aux_loc[0]
                self.params['locId'] = aux_loc[1]

                self.getConnection()

        self.df = pd.DataFrame(self.aux_data, columns = self.columns)