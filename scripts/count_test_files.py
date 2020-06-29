#!/usr/bin/env python3
# coding: utf-8

# Description: Script que verifica quantos arquivos de teste o projeto possui

# ===== Configuration variables ======
PROG_LANG = 'Java'
REPO_PATH = '../repos'
DATASET_PATH = '../dataset/projects_final.xlsx'
TEST_TOOL_PATH = '../docs/testing_frameworks.xlsx'
FILE_EXT = {
    'Python': ['*test_*.py'],
    'Ruby': ['*_test.rb', '*_spec.rb'],
    'JavaScript': ['*Spec.js', '*Test.js', '*spec.js', '*test.js', '*tests.js'],
    'PHP' : ['*test.php', '*Test.php'],
    'Java': ['*Test.java'],
    'TEST': ['*Test*.java', '*Tests*.java'],
    'Java': ['*Test*.java', '*Tests*.java'],
}
# =====================================

import os
import pandas as pd

def _apply_filters(df):
    if len(PROG_LANGS) > 0:
        df = df[df['primaryLanguage'].isin(PROG_LANGS)]
    if LIMIT:
        df = df.head(LIMIT)
    return df


def _get_proj_names():
    dirname = f'{REPO_PATH}/{PROG_LANG}/'
    if not os.path.exists(dirname):
        print(f'Error: Directory for {PROG_LANG} does not exists!\n')
        return None
    proj_names = os.popen(f'ls {dirname}').read()
    return proj_names.split('\n')


def _count_test_files(dir_name):
    file_exts = FILE_EXT[PROG_LANG]
    result = {}
    for file_ext in file_exts:
        temp_result = os.popen(f'find {dir_name} -name "{file_ext}" | wc -l').read()
        result[file_ext] = int(temp_result)
    return result

def execute_count_test_files():
    proj_names = _get_proj_names()
    print('(Project) - (Test files by extension)')
    for proj_name in proj_names:
        dir_name = f'{REPO_PATH}/{PROG_LANG}/{proj_name}/'
        result = _count_test_files(dir_name)
        print(f'{proj_name} - {result}') 

if __name__ == "__main__":
    execute_count_test_files()
