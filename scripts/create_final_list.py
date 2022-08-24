#!/usr/bin/env python3
# coding: utf-8

# Description: Criar a lista de final dos projetos

import requests
import json
from datetime import date

def execute():
    print(f'Criando lista de projetos.\n')


    # 2008 to current year 
    period = range (2008, date.today().year)
    
    for year in period:
        url = f'https://api.github.com/search/repositories?q=stars%3A%3E5000%20created%3A{year}-01-01..{year}-12-31%20&sort=created&order=asc&page=1&per_page=100'
        r = requests.get(url)
        j = json.loads(r.text)
        print(f'{year}: {j["total_count"]}')
    
    # print(len(j["items"]))

if __name__ == "__main__":
    execute()
