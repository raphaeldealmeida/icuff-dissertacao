#!/usr/bin/env python3
# coding: utf-8

# Description: Clona os repositórios que foram coletados no dataset

# ===== Configuration variables ======
LIMIT = 200
PROG_LANG = 'Java'
REPO_PATH = '../repos'
DATASET_PATH = '../dataset/2_filtered_projects.xlsx'
# =====================================

import pandas as pd
import os

def _create_dirname(language, name):
    if not os.path.exists(REPO_PATH):
        os.mkdir(REPO_PATH)
    return f'{REPO_PATH}/{language}/{name}'

def _download_repos(df):
    for index, row in df.iterrows():


        owner, language, name = row['owner'], row['primaryLanguage'], row['name']
        url = f'https://github.com/{owner}/{name}'
        dirname = _create_dirname(language, name)
        if not os.path.exists(dirname):
            os.system(f'git clone {url}.git {dirname}')
            print(f'Successful download of {name}!\n')
        else:
            print(f'Error: The {name} repository already downloaded!\n')

def _apply_filters(df):
    if len(PROG_LANG) > 0:
        df = df[df['primaryLanguage'] == PROG_LANG]
    if LIMIT:
        df = df.head(LIMIT)
    return df

def execute_cloner():
    df = pd.read_excel(DATASET_PATH)
    df = _apply_filters(df)
    _download_repos(df)

if __name__ == "__main__":
    execute_cloner()
