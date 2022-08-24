#!/usr/bin/env python3
# coding: utf-8

# Description: Criar a lista de final dos projetos

import requests
import json, io, codecs, re
from datetime import date
from os import listdir
from os.path import isfile, join
import pandas as pd

FIELD_NAMES = ['owner','name','createdAt','pushedAt','isMirror','diskUsage','primaryLanguage','languages','contributors','watchers','stargazers','forks','issues','commits','pullRequests','branches','tags','releases','url','idSoftware','discardReason','domain','description']

proxies = {
            'http': 'http://09840070754:_Habaco56_@10.52.132.215:8080/',
            'https': 'http://09840070754:_Habaco56_@10.52.132.215:8080/',
        }

user = 'raphaelrsa'
password = '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'

def execute():
    print(f'Criando lista de projetos.\n')

    
    
    page = 1
    # 2008 to current year 
    period = range (2008, date.today().year)
    #period = range (2008, 2009)
    
    for year in period:
        
        
        
        page = 1
        while( page != -1):
            url = f'https://api.github.com/search/repositories?q=stars%3A%3E5000%20created%3A{year}-01-01..{year}-12-31%20&sort=created&order=asc&page={page}&per_page=100'
            r = requests.get(url, auth=(user, password), proxies=proxies)
            j = json.loads(r.text)
            
            print(len(j["items"]))
            print(f'page: {page}')
            if ( len(j["items"]) == 0 ): 
                page = -1
                break

            with open(f'../dataset/github/{year}-{page}.json', 'wb') as f:
                json.dump(j, codecs.getwriter('utf-8')(f), ensure_ascii=False)

            page += 1
            
        print(f'{year}: {j["total_count"]}')       

def create_excel():
    #get files in folder
    mypath = '../dataset/github/'
    jfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    repos = []
    commits = []

    for jfile in jfiles:

        with open(f'{mypath}{jfile}') as jf:

            data = json.load(jf)
            #print(data['items'])

            for r in data['items']:

                repo = {
                    'owner': r['owner']['login'],
                    'name': r['name'],
                    'createdAt': r['created_at'],
                    'pushedAt': r['pushed_at'],
                    'isMirror': r['mirror_url'],
                    'diskUsage': '',
                    'primaryLanguage': r['language'],
                    'languages': '',
                    'contributors': '', # contributors_url
                    'watchers': r['watchers_count'],
                    'stargazers': r['stargazers_count'],
                    'forks': r['forks_count'],
                    'issues': r['open_issues_count'],
                    'commits':'', #
                    'pullRequests': '', #
                    'branches': r['pushed_at'], #
                    'tags': '', #
                    'releases': '', #
                    'url': r['html_url'],
                    'idSoftware': 'Y',
                    'discardReason': '',
                    'domain': '',
                    'description': r['description'],
                }
                print(f"{r['owner']['login']}/{r['name']}: {commitCount(r['owner']['login'], r['name'])}")
                #repos.append(repo)    

    #df = pd.DataFrame(data=repos, columns=FIELD_NAMES)
    #df.to_excel('../dataset/projects_2022.xlsx')

    #loop to read and write on var
    #save var to xlsx

def commitCount(user, repo):
    return re.search('\d+$', requests.get(f'https://api.github.com/repos/{user}/{repo}/commits?per_page=1'.format(user, repo), auth=(user, password), proxies=proxies).links['last']['url']).group()

if __name__ == "__main__":
    create_excel()
    
