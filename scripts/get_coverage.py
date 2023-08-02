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
        #df = df[(df['primaryLanguage'] == PROG_LANG) & (df['name'] == 'phpunit')]
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
    # é posivel ler o valor direto do SVG que é um xml
    # url_antiga = https://coveralls.io/github/{owner}/{name}
    # pattern_antigo =  "<div class='coverage-(.*) coverageText' id='repoShowPercentage'>(.*)%<\/div>"
    pattern1 = '<text\\b[^>]*>\\s*(?:(?!coverage)[^<])*\\s*<\/text>'
    url_cov = f'https://coveralls.io/repos/github/{owner}/{name}/badge.svg'
    print(url_cov)
    match_position = 0
    tag = get_cov_service(url_cov, pattern1, match_position)
    pattern2 = r'<text[^>]*>(.*?)<\/text>'
    resultado = re.search(pattern2, tag)

    if(resultado):
        texto_extraido = resultado.group(1)
        return texto_extraido if texto_extraido != 'unknown' else False
    else:
        return False

def get_codecov(owner, name):
    query = {"query":"\n    query GetRepoCoverage($name: String!, $repo: String!, $branch: String!) {\n      owner(username:$name){\n        repository: repositoryDeprecated(name:$repo){\n          branch(name:$branch) {\n            name\n            head {\n              yamlState\n              totals {\n                percentCovered\n                lineCount\n                hitsCount\n              }\n            }\n          }\n        }\n      }\n    }\n  ",
             "variables":{"name":owner,"repo":name,"branch":"master"}}
    pattern = "\"percentCovered\"\: (.*)\,"
    url_cov = "https://api.codecov.io/graphql/gh"
    print(url_cov)
    match_position = 1
    return False # get_cov_service(url_cov, pattern, match_position,query)

def get_scrutinizer(owner, name):
    pattern = "<p class=\"covered-data\">\n                    (.*) <sup class=\"coverage-percentage-superscript\">"
    url_cov = f'https://scrutinizer-ci.com/g/{owner}/{name}/code-structure/master/code-coverage'
    print(url_cov)
    match_position = 1
    return get_cov_service(url_cov, pattern, match_position)

def get_codeclimate(owner, name):
    pattern = "<\/span><\/div><div class=\"measure measure--x2\"><span>(.*)%<\/span><\/div><\/div><\/div>"
    url_cov  = f'https://codeclimate.com/github/{owner}/{name}'
    print(url_cov)
    match_position = 1
    return get_cov_service(url_cov, pattern, match_position)

def get_codacy(owner, name):
    #pattern = "<\/span><\/div><div class=\"measure measure--x2\"><span>(.*)%<\/span><\/div><\/div><\/div>"
    pattern = "\"coveragePercentage\"\:(.*)\,\"coveragePercentageWithDecimals\""
    #url_cov  = f'https://codeclimate.com/github/{owner}/{name}'
    url_cov  = f'https://app.codacy.com/api/v3/analysis/organizations/gh/{owner}/repositories/{name}'
    print(url_cov)
    match_position = 1
    return get_cov_service(url_cov, pattern, match_position)


def get_cov_service(url_cov, pattern, match_position, payload = {}):
    try:
        r = requests.get(url_cov) if payload == {} else requests.post(url_cov, json=payload)
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
        
        # cov = cov if(cov != None) else get_cov(owner, name)
        cov = get_cov(owner, name)

        print(f'{owner}/{name}: {cov}')
        row['coverage'] = cov
        #dados[index] = row

    df = pd.DataFrame(dados)
    df.to_excel(DATASET_PATH_OUT) 

if __name__ == "__main__":
    execute_analisys()
