#!/usr/bin/env python3
# coding: utf-8

import utils
import helper
import setting as st

import os
import pandas as pd 
import radon.complexity as rdc

import lizard



def count_conditionals(code, conditionals):
    total_conditionals = 0
    for conditional in conditionals:
        total_conditionals += code.count(conditional)
    return total_conditionals


def count_logical_operators(code, logical_operators):
    total_operators = 0
    for operator in logical_operators:
        total_operators += code.count(operator)
    return total_operators


def get_cyclomatic_complexity(code, lang_info):
    if not code:
        return 0
    conditionals = count_conditionals(code, lang_info['conditionals'])
    logical_operators = count_logical_operators(code, lang_info['logical_operators'])
    CC = conditionals + logical_operators + 1
    return CC


def get_project_files(project_path, file_extension):
    response = os.popen(f'find {project_path} -type f -name "*{file_extension}"')
    files = response.read().split("\n")
    files = list(filter(lambda file: file.endswith(file_extension), files)) # filtra arquivos pela extensão desejada
    return files


def get_code(file_path):
    if not os.path.isfile(file_path):
        return None
    with open(file_path, 'r') as file:
        return file.read()


def get_project_ciclomatic_complexity(project_name, programming_language, owner):
    try:
        language_info = utils.load_language_info()[programming_language]
    except:
        print(f'Warning: info was not configured to {programming_language}')
        return None
    
    project_path = f"{st.REPO_PATH}/{owner}/{project_name}"
    project_files = get_project_files(project_path, language_info['file_extension'])
    
    total_cc = 0
    for file in project_files:
        try:
            code = get_code(file)
            cc = get_cyclomatic_complexity(code, language_info)
            total_cc += cc
        except:
            continue
    
    return total_cc


def execute_analysis(data):    
    repos = []

    for _, row in data.iterrows(): 
        project_path = f"{st.REPO_PATH}/{row['owner']}/{row['name']}"

        if not os.path.exists(project_path):
            print(f"Warning: the {row['owner']}/{row['name']} project was not cloned!")
            continue

        print(f"Collecting ciclomatic complexity for {row['owner']}/{row['name']} ...")

        try:
            ciclomatic_complexity = calcular_media_cc2(
                row['name'], 
                row['primaryLanguage'],
                row['owner']
            )
        except:
            print(f"Error...")
            ciclomatic_complexity = None

        repos.append(
            {
                'owner': row['owner'],
                'name': row['name'],
                'primaryLanguage': row['primaryLanguage'],
                'ciclomaticComplexity':  ciclomatic_complexity,
            }
        )


    return repos

def calcular_media_cc(project_name, programming_language, owner):
    total_complexity = 0
    total_funcoes = 0

    diretorio_projeto = f"{st.REPO_PATH}/{owner}/{project_name}"

    try:
        language_info = utils.load_language_info()[programming_language]
    except:
        print(f'Warning: info was not configured to {programming_language}')
        return None
    for raiz, _, arquivos in os.walk(diretorio_projeto):
        for arquivo in arquivos:
            if arquivo.endswith(language_info['file_extension']):
                arquivo_path = os.path.join(raiz, arquivo)
                with open(arquivo_path, 'r', encoding='utf-8') as file:
                    codigo_fonte = file.read()
                    complexidade_funcoes = rdc.cc_visit(codigo_fonte)
                    total_complexity += sum(func.complexity for func in complexidade_funcoes)
                    total_funcoes += len(complexidade_funcoes)

    if total_funcoes > 0:
        media_cc = total_complexity / total_funcoes
        print(media_cc)
        return media_cc
    else:
        return None

def calcular_media_cc2(project_name, programming_language, owner):
    total_complexity = 0
    total_funcoes = 0

    diretorio_projeto = f"{st.REPO_PATH}/{owner}/{project_name}"

    try:
        language_info = utils.load_language_info()[programming_language]
    except:
        print(f'Warning: info was not configured to {programming_language}')
        return None

    for raiz, _, arquivos in os.walk(diretorio_projeto):
        for arquivo in arquivos:
            if arquivo.endswith(language_info['file_extension']):
                arquivo_path = os.path.join(raiz, arquivo)
                with open(arquivo_path, 'r', encoding='utf-8') as file:
                    codigo_fonte = file.read()
                    arquivo_nome = os.path.basename(arquivo_path)
                    try:
                        complexity_info = lizard.analyze_file.analyze_source_code(arquivo_nome,codigo_fonte)
                        total_complexity += sum(func.cyclomatic_complexity for func in complexity_info.function_list)
                        total_funcoes += len(complexity_info.function_list)
                    except Exception as e:
                        print(f"Error analyzing file '{arquivo}': {str(e)}")

    if total_funcoes > 0:
        average_complexity = total_complexity / total_funcoes
    else:
        average_complexity = 0

    print(average_complexity)
    return average_complexity

def calculate(code, extension):
    file_info = lizard.analyze_file.analyze_source_code(extension, code)
    complexity = sum(func.cyclomatic_complexity for func in file_info.function_list)
    functions = len(file_info.function_list)
    
    return {'complexity': complexity, 'functions': functions}


def run():
    dataset = pd.read_excel(st.DATASET_PATH)
    dataset = helper.filter_dataset(dataset)
    dataset_grouped = dataset.groupby('primaryLanguage')
    
    print('-> Collecting ciclomatic complexity <-\n')

    if not os.path.exists(st.OUTPUT_PATH):
        os.makedirs(st.OUTPUT_PATH)

    for programming_language, data in dataset_grouped:

        print(f'Analyzing {programming_language} projects ... \n')
        result = execute_analysis(data)

        print(f'Saving the result of {programming_language} projects ... \n')
        df = pd.DataFrame(result)

        output_file_path = f'{st.OUTPUT_PATH}/ciclomatic_complexity_{programming_language}2.xlsx'

        with pd.ExcelWriter(output_file_path) as writer:
            df.to_excel(writer, index=False)


if __name__ == "__main__":
    run()