from glassdoor import Glassdoor
from neuvoo import Neuvoo
from wowhead import Wowhead
import datetime
import pandas as pd
import json

with open('salaries_glassdoor.json', 'r') as f:
    glassdoor_conf = json.load(f)

def import_from_json(key_word):
    aux_data = []
    for gc in glassdoor_conf:
        aux_data.append(gc[key_word])    
    return aux_data

with open('salaries_neuvoo.json', 'r') as f:
    neuvoo_conf = json.load(f)

t1 = datetime.datetime.now()

with pd.ExcelWriter('Salaries.xlsx') as writer:
    #salaries per country
    location_countries = import_from_json("country_code")
    gd_countries = Glassdoor(location_countries)
    gd_countries.run()
    gd_countries.df.to_excel(writer, sheet_name = "Countries", index = False)

    #salaries per city
    for gc in glassdoor_conf:
        try:
            gd_cities = Glassdoor(gc['cities'])
            gd_cities.run()
            gd_cities.df.to_excel(writer, sheet_name = gc['country'], index = False)
        except Exception as e:
            print(e)

with pd.ExcelWriter("Country tax.xlsx") as writer:
    for nc in neuvoo_conf:
        try:
            neuvoo = Neuvoo(nc)
            neuvoo.run()
            neuvoo.df.to_excel(writer, sheet_name = nc["country"], index = False)
        except Exception as e:
            print(e)

print(datetime.datetime.now() - t1)