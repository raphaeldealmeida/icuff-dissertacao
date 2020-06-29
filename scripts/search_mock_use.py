#!/usr/bin/env python3
# coding: utf-8

# Description: Procura arquivos de teste com a palavra mock

# ===== Configuration variables ======
PROG_LANG = 'Java'
REPO_PATH = '../repos'
DATASET_PATH = '../dataset/projects_final.xlsx'
DATASET_PATH_MOCK_FILES = f'../dataset/{PROG_LANG}_mock_files.csv'
DATASET_PATH_MOCK_FILES2 = f'../dataset/{PROG_LANG}_RQ2.csv'

DESC_FILE = {
    'Ruby': 'Gemfile',
    'Python': 'requirements.txt',
    'JavaScript': 'package.json',
    'PHP': 'composer.json'	
}
TEST_TOOLS = {
    'Ruby': ['rspec', 'minitest', 'test-unit', 'cucumber-ruby'],
    'Python': ['robot', 'pytest', 'unittest'],
    'JavaScript': ['jest', 'jasmine', 'mocha', 'puppeteer', 'cypress'],
    'PHP': ['phpunit', 'codeception', 'SimpleTest', 'Behat']
}
MOCK_TOOLS = {
    'PHP': ["createMock[^(]*\(([^)]*)\)", "getMock[^(]*\(([^)]*)\)", "getMockBuilder[^(]*\(([^)]*)\)", "getMockForTrait[^(]*\(([^)]*)\)", "getMockForAbstractClass[^(]*\(([^)]*)\)", "getMockFromWsdl[^(]*\(([^)]*)\)", "vfsStream::setup[^(]*\(([^)]*)\)","prophesize[^(]*\(([^)]*)\)","::mock[^(]*\(([^)]*)\)", "::spy[^(]*\(([^)]*)\)"],
    'TEST': [".mock[^(]*\(([^)]*)\)", "mock[^(]*\(([^)]*)\)", "spy[^(]*\(([^)]*)\)"],
    'Java': [".mock[^(]*\(([^)]*)\)", "mock[^(]*\(([^)]*)\)", "spy[^(]*\(([^)]*)\)"]
}

FILE_EXT = {
    'Python': ['*test_*.py'],
    'Ruby': ['*_test.rb', '*_spec.rb'],
    'JavaScript': ['*Spec.js', '*Test.js', '*spec.js', '*test.js', '*tests.js'],
    'PHP' : ['*test.php', '*Test.php', 'Spec.php'],
    'TEST' : ['*Test*.java', '*Tests*.java'], 	 	
    'Java' : ['*Test*.java', '*Tests*.java']
}
# =====================================

from test_tool_by_descriptor import _get_proj_names
from test_tool_by_descriptor import _read_descriptor
import os
import csv
import re

def _get_test_files(dir_name):
    file_exts = FILE_EXT[PROG_LANG]
    result = []
    for file_ext in file_exts:
        temp_result = os.popen(f'find {dir_name} -name "{file_ext}"').read()
        result = result + temp_result.split('\n')
    result = list(filter(lambda x : x != '', result))
    
    # projeto fora do padrão para identificar testes
    # if dir_name == '../repos/PHP/YOURLS':
    #     print('sem testes buscando na pasta tests')
    #     print(f'find {dir_name} -wholename "*tests/*.php"')
    #     temp_result = os.popen(f'find {dir_name} -wholename "*tests/*.php"').read()
    #     result = result + temp_result.split('\n')

    return result

def _write_csv(result):
    with open(DATASET_PATH_MOCK_FILES, mode='w') as csv_file:
        fieldnames = ['lang', 'owner', 'name', 'file', 'mock', 'dep']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, dialect='unix')
        writer.writeheader()
        for li in result:
            writer.writerow(li)

def _write_csv2(result):
    with open(DATASET_PATH_MOCK_FILES2, mode='w') as csv_file:
        fieldnames = ['lang', 'owner', 'name', 'total_mocks', 'qtr_test_files', 'total_files_com_mocks', 'razao_mocks']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, dialect='unix')
        writer.writeheader()
        for li in result:
            writer.writerow(li)            

def _get_owner_from_repo(path_repo):
    remote = os.popen(f'cd {path_repo} && git remote -v').read().split('\n')[0]
    pattern = '^origin	http[s]*:\/\/[www.]*[github|gitlab]*\.com\/(.*)\/(.*)\.git \(fetch\)$'
    m = re.search(pattern, remote)
    print(path_repo)
    return str(m.group(1))

def execute_analisys():
    result = []
    proj_names = _get_proj_names()
    for proj_name in proj_names:
        test_files = _get_test_files(f'{REPO_PATH}/{PROG_LANG}/{proj_name}')
        owner = _get_owner_from_repo(f'{REPO_PATH}/{PROG_LANG}/{proj_name}')
        qtr_test_files = len(test_files)
        print('==========================================================')
        print(f'Project: {owner}/{proj_name}')
        if (qtr_test_files == 0):
            print('Não é possível identifiar testes neste projeto')
            continue
        total_mocks = 0
        total_files_com_mocks = 0
        for test_file in test_files:
            fingerprint = '|'.join(MOCK_TOOLS[PROG_LANG])
            mocks = os.popen(f'cat {test_file} | grep -E \'{fingerprint}\'').read().split('\n')
            mocks = list(filter(lambda x : x != '', mocks))
            for mock in mocks:
                m = re.search(fingerprint, mock)
                dependencia = "None"
                for i in range(1, len(MOCK_TOOLS[PROG_LANG])):
                    dependencia = str(m.group(i))
                    #print(f'{mock}: {dependencia}')
                    if dependencia != "None":
                        break
                result.append({'lang': PROG_LANG, 'owner': owner, 'name': proj_name, 'file': test_file, 'mock': mock.strip(), 'dep': dependencia.strip()})
            qtd_mocks = len(mocks)
            #print(f'{test_file}: {qtd_mocks} mock')
            total_mocks = total_mocks + qtd_mocks
            if (qtd_mocks > 0):
                total_files_com_mocks = total_files_com_mocks + 1    
        print(f'total de arquivos de test: {qtr_test_files}')        
        print(f'total de arquivos de test com mocks: {total_files_com_mocks}')
        print(f'total de mocks no projeto: {total_mocks}')
        razao_mocks = round((total_files_com_mocks / qtr_test_files) * 100, 2)
        print(f'razão de testes com mocks no projeto: {razao_mocks}%')
    _write_csv(result)

def execute_rq1():
    result = []
    proj_names = _get_proj_names()
    for proj_name in proj_names:
        test_files = _get_test_files(f'{REPO_PATH}/{PROG_LANG}/{proj_name}')
        owner = _get_owner_from_repo(f'{REPO_PATH}/{PROG_LANG}/{proj_name}')
        qtr_test_files = len(test_files)
        print('==========================================================')
        print(f'Project: {owner}/{proj_name}')
        if (qtr_test_files == 0):
            print('Não é possível identifiar testes neste projeto')
            continue
        total_mocks = 0
        total_files_com_mocks = 0
        for test_file in test_files:
            fingerprint = '|'.join(MOCK_TOOLS[PROG_LANG])
            mocks = os.popen(f'cat {test_file} | grep -E \'{fingerprint}\'').read().split('\n')
            mocks = list(filter(lambda x : x != '', mocks))
            # for mock in mocks:
            #     m = re.search(fingerprint, mock)
            #     dependencia = "None"
            #     for i in range(1, len(MOCK_TOOLS[PROG_LANG])):
            #         dependencia = str(m.group(i))
            #         #print(f'{mock}: {dependencia}')
            #         if dependencia != "None":
            #             break
            #     result.append({'lang': PROG_LANG, 'owner': owner, 'name': proj_name, 'file': test_file, 'mock': mock.strip(), 'dep': dependencia.strip()})
            qtd_mocks = len(mocks)
            total_mocks = total_mocks + qtd_mocks
            if (qtd_mocks > 0):
                total_files_com_mocks = total_files_com_mocks + 1    
        print(f'total de arquivos de test: {qtr_test_files}')        
        print(f'total de arquivos de test com mocks: {total_files_com_mocks}')
        print(f'total de mocks no projeto: {total_mocks}')
        razao_mocks = round((total_files_com_mocks / qtr_test_files) * 100, 2)
        print(f'razão de testes com mocks no projeto: {razao_mocks}%')
        
        filtro = "awk '/  Classes/{print $2}' | tail -1"
        #padrao = f'phploc --count-tests {REPO_PATH}/{PROG_LANG}/{proj_name} | {filtro}'
        #print(padrao)
        #qtr_test_files2 = os.popen(padrao).read().strip()
        
        result.append({'lang': PROG_LANG, 'owner': owner, 'name': proj_name, 'total_mocks': total_mocks, 
        'qtr_test_files': qtr_test_files, 'total_files_com_mocks': total_files_com_mocks, 'razao_mocks': razao_mocks })
    _write_csv2(result)


if __name__ == "__main__":
    execute_analisys()
    #execute_rq1()
