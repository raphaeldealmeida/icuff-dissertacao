#!/usr/bin/env python3
# coding: utf-8

# Description: Verifica se o código fonte da dependencia está no projeto

# ===== Configuration variables ======
PROG_LANG = 'JavaScript'
DATASET_PATH_MOCK_FILES = f'../dataset/{PROG_LANG}_mock_files.csv'
REPO_PATH = '../repos'
FILE_EXT = {
    'PHP': '.php',
    'Java': '.java',
    'Python': '.py',
    'JavaScript': '.js',
}

# =====================================

import csv
import os
import pandas as pd

def _open_dataset():
    #data = pd.read_csv(DATASET_PATH_MOCK_FILES)
    #return data.to_numpy()
    results = []
    with open(DATASET_PATH_MOCK_FILES, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', dialect='unix')
        for row in reader: 
            results.append({'lang': row[0], 'owner': row[1], 'name': row[2], 'file': row[3], 'mock': row[4], 'dep': row[5]})
    return results


def _clean_dep(raw_dep):
    raw_dep = raw_dep.replace('::class', '').replace("'", '').replace('"', '').replace('.class', '')
    raw_dep = raw_dep.split("\\")[-1]
    #print(raw_dep)
    return False if raw_dep == 'None' else raw_dep.replace('`', r'\`').replace('$', r'\$').replace('*', r'\*')

def _type_of_dep(path, dep):
    file_ext = FILE_EXT[PROG_LANG]
    dep = _clean_dep(dep)    


    if (dep == False):
        return 'indefinida'
    if (PROG_LANG == 'Python'):
        return 'interno' if (len(dep.split(".")) > 1 and dep.split(".")[0] in path ) else ('externo' if dep.split(".")[0] else 'indefinida')
    if (PROG_LANG == 'JavaScript'):

        if (dep.startswith('/') or  dep.startswith('./') or dep.startswith('../') or dep.startswith('@')):
            return 'interno' 
        if (dep.startswith('http')):
            return 'externo' 
        if (dep.startswith('()') or dep.startswith('function') or dep.startswith('{')):
            return 'indefinida' 
        return 'interno' if (int(os.popen(f'grep --include=\*{file_ext} -rnw "{path}" -e "class {dep}" -o -e "interface {dep}" | wc -l || 0').read()) == 1) else 'externo'
    else:
        print(f'grep --include=\*{file_ext} -rnw "{path}" -e "class {dep}" -o -e "interface {dep}" | wc -l || 0')
        return 'interno' if (int(os.popen(f'grep --include=\*{file_ext} -rnw "{path}" -e "class {dep}" -o -e "interface {dep}" | wc -l || 0').read()) == 1) else 'externo'


def _write_csv(result):
    with open(DATASET_PATH_MOCK_FILES, mode='w') as csv_file:
        fieldnames = ['lang', 'owner', 'name', 'file', 'mock', 'dep', 'origin']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, dialect='unix')
        writer.writeheader()
        for li in result:
            writer.writerow(li)

#lista dependencia
#busca na pasta do projeto arquivo com o nome
# se tiver interna
# se não tiver externa 
def execute_analisys():
    print('Verificando dependencias')
    dados = _open_dataset()
    for i, row in enumerate(dados):
        proj_name = row['name']
        path = f'{REPO_PATH}/{PROG_LANG}/{proj_name}'
        row['origin'] = _type_of_dep(path, row['dep']) 
        dados[i] = row
        print(dados[i])
    _write_csv(dados)          

if __name__ == "__main__":
    execute_analisys()
