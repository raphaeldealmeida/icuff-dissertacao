#!/usr/bin/env python3
# coding: utf-8

# Description: Verifica cobertura de código no principais sites

# ===== Configuration variables ======
LIMIT = 130
PROG_LANG = 'Java'
REPO_PATH = '../repos'
DATASET_PATH = '../dataset/2_filtered_projects.xlsx'
DATASET_PATH_OUT = f'../dataset/{PROG_LANG}_3_filtered_projects.xlsx'
#DATASET_PATH = '../dataset/filtered_projects.xlsx'
# =====================================

import pandas as pd
import requests
import re

def _apply_filters(df):
    if len(PROG_LANG) > 0:
        df = df[df['primaryLanguage'] == PROG_LANG]
    if LIMIT:
        df = df.head(LIMIT)
    return df

def get_cov(owner, name):
    result = get_coveralls(owner, name)
    if(result != False ):
        print('get_coveralls')
        return result

    result = get_codecov(owner, name)
    if(result != False):
        print('get_codecov')
        return result

    result = get_codeclimate(owner, name)
    if(result != False):
        print('get_codeclimate')
        return result

    result = get_codacy(owner, name)
    if(result != False):
        print('get_codacy')
        return result

    result = get_scrutinizer(owner, name)
    if(result != False):
        print('get_scrutinizer')
        return result
    
    return False

def get_coveralls(owner, name):
    pattern =  "<div class='coverage-(.*) coverageText' id='repoShowPercentage'>(.*)%<\/div>"
    url_cov = f'https://coveralls.io/github/{owner}/{name}'
    match_position = 2
    return get_cov_service(url_cov, pattern, match_position)

def get_codecov(owner, name):
    pattern = "<td class=\" right aligned\"\nstyle=\"background:linear-gradient\(90deg, (.*) (.*), white (.*);\">\n\n\n(.*)%\n\n<\/td>"
    url_cov = f'https://codecov.io/gh/{owner}/{name}'
    match_position = 4
    return get_cov_service(url_cov, pattern, match_position)

def get_scrutinizer(owner, name):
    pattern = "<p class=\"covered-data\">\n                    (.*) <sup class=\"coverage-percentage-superscript\">"
    url_cov = f'https://scrutinizer-ci.com/g/{owner}/{name}/code-structure/master/code-coverage'
    match_position = 1
    return get_cov_service(url_cov, pattern, match_position)

def get_codeclimate(owner, name):
    pattern = "<\/span><\/div><div class=\"measure measure--x2\"><span>(.*)%<\/span><\/div><\/div><\/div>"
    url_cov  = f'https://codeclimate.com/github/{owner}/{name}'
    match_position = 1
    return get_cov_service(url_cov, pattern, match_position)

def get_codacy(owner, name):
    pattern = "title=\"Percentage of lines of code tested\.\"><\/i><\/p>\n          <p>(.*)% \n            \n  <span class="
    url_cov = f'https://app.codacy.com/manual/{owner}/{name}/dashboard'
    match_position = 1
    return get_cov_service(url_cov, pattern, match_position)


def get_cov_service(url_cov, pattern, match_position):
    try:
        r = requests.get(url_cov)
        m = re.search(pattern, r.text)
        if (m):
            return m.group(match_position)
    except:
        print(f'Erro ao tentar obter coverage de: {url_cov}')
        pass
    return False

def execute_analisys():
    print('Verificando cobertura')
    df = pd.read_excel(DATASET_PATH)
    df = _apply_filters(df)
    dados = df.T.to_dict().values()
    for row in dados:
        owner, language, name = row['owner'], row['primaryLanguage'], row['name']
        
        #verificar se já tem a cov e usar
        df2 = pd.read_excel(DATASET_PATH_OUT)
        df2 = df2[df2['owner'] == owner]
        df2 = df2[df2['primaryLanguage'] == language]
        df2 = df2[df2['name'] == name]
        df2 = df2.head(1)
     
        cov = None   
        for row2 in df2.T.to_dict().values():
            cov = row2['coverage']
        
        cov = cov if(cov != None) else get_cov(owner, name)

        print(f'{owner}/{name}: {cov}')
        row['coverage'] = cov
        #dados[index] = row

    df = pd.DataFrame(dados)
    df.to_excel(DATASET_PATH_OUT) 

if __name__ == "__main__":
    execute_analisys()
