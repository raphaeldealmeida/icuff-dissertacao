#!/usr/bin/env python3
# coding: utf-8

# Description: Criar a lista de final dos projetos

import requests
import json, io, codecs, re, math
from datetime import date
from os import listdir
from os.path import isfile, join
import pandas as pd

FIELD_NAMES = ['owner','name','createdAt','pushedAt','isMirror','diskUsage','primaryLanguage','languages','contributors','watchers','stargazers','forks','issues','commits','pullRequests','branches','tags','releases','url','idSoftware','discardReason','domain','description']
DATASET_PATH = '../dataset/projects_2022.xlsx'
user = 'raphaelrsa'
password = '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'

def execute():
    print(f'Criando lista de projetos.\n')

    
    
    page = 1
    # 2008 to current year 
    #period = range (2008, date.today().year)
    period = range (2022, 2023)
    
    for year in period:
        
        
        
        page = 1
        while( page != -1):
            url = f'https://api.github.com/search/repositories?q=stars%3A%3E5000%20created%3A{year}-01-01..{year}-12-31%20&sort=created&order=asc&page={page}&per_page=100'
            r = requests.get(url, auth=(user, password))
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

                if not r['language'] in ['Java', 'PHP', 'Python', 'JavaScript']:
                    continue

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
                    'commits':commit_count2(r['owner']['login'], r['name']), #
                    'pullRequests': '', #
                    'branches': '', #
                    'tags': '', #
                    'releases': '', #
                    'url': r['html_url'],
                    'idSoftware': 'Y',
                    'discardReason': '',
                    'domain': '',
                    'description': r['description'],
                }
                if (repo['commits'] < 5000):
                    continue
                print(f"{repo['owner']}/{repo['name']}: {repo['commits']}")
                repos.append(repo)    

    df = pd.DataFrame(data=repos, columns=FIELD_NAMES)
    df.to_excel(DATASET_PATH)

    # count commits git rev-list --all --count

    #loop to read and write on var
    #save var to xlsx

def commit_count(user_repo, repo):
    return int(re.search('\d+$', requests.get(f'https://api.github.com/repos/{user_repo}/{repo}/commits?per_page=1'.format(user_repo, repo), auth=(user, password)).links['last']['url']).group())

def fill_commit_amount():
    df = pd.read_excel(DATASET_PATH)
    print(df.info())
    dados = df.T.to_dict().values()
    for row in dados:
        owner, name, commits = row['owner'], row['name'], row['commits']

        commits = commits if not (math.isnan(commits)) else commit_count2(owner, name)

        print(f'{owner}/{name}: {commits}')
        row['commits'] = commits
        # dados[index] = row

    df = pd.DataFrame(dados)
    df.to_excel(DATASET_PATH) 

def commit_count2(user_repo, repo):
    from urllib.parse import urlparse, parse_qs
    """
    Return the number of commits to a project
    """
    url = f'https://api.github.com/repos/{user_repo}/{repo}/commits?per_page=1'

    resp = requests.get(url, auth=(user, password))

    if (resp.status_code // 100) != 2:
        raise Exception(f'invalid github response: {resp.content}')
    # check the resp count, just in case there are 0 commits
    commit_count = len(resp.json())
    last_page = resp.links.get('last')

    # if there are no more pages, the count must be 0 or 1
    if last_page:
        # extract the query string from the last page url
        parse_result = urlparse(last_page['url'])
        dict_result = parse_qs(parse_result.query)
        
        # extract the page number from the query string
        commit_count = int(dict_result['page'][0])
    return commit_count



if __name__ == "__main__":
    # execute()
    create_excel()
    # fill_commit_amount()