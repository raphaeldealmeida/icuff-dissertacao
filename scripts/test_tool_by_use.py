#!/usr/bin/env python3
# coding: utf-8
from test_tool_by_descriptor import _get_owner_from_repo

# Descripton: Verifica em cada projeto, quais ferramentas de teste utilizada pelos projetos

# ===== Configuration variables ======
PROG_LANG = "JavaScript"
REPO_PATH = "/media/raphaelrsa/de61512f-e8e6-4e0a-9cbc-168ddd77ff20/repos"
DATASET_PATH_TEST_PROJECTS = f"../dataset/{PROG_LANG}_projects_tests_tools2.csv"

import os
import re
import csv
from joblib import Parallel, delayed

# Padrões para identificar chamadas específicas de várias ferramentas
TOOL_PATTERNS = {
    "PHP": {
        "PHPUnit": [
            r"(createStub\((.*?)\))",
            r"(createMock\((.*?)\))",
            # Outros padrões omitidos por brevidade
        ],
        "Mockery": [
            r"([Mockery|m]::mock\((.*?)\))",
            # Outros padrões omitidos por brevidade
        ],
    },
    "JavaScript": {
        "jest": [
            r"(jest.mock\((.*?)\))",
        ],
        "sinon": [
            r"(sinon.spy\((.*?)\))",
            r"(sinon.mock\((.*?)\))",
        ],
        # Outros padrões omitidos por brevidade
    },
}


def process_file(file_path, language):
    occurrences = {tool: [] for tool in TOOL_PATTERNS.get(language, {})}

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for line_number, line_content in enumerate(lines, start=1):
                for tool, patterns in TOOL_PATTERNS.get(language, {}).items():
                    for pattern in patterns:
                        match = re.search(pattern, line_content)
                        if match:
                            full_call = match.group(1)  # Chamada completa
                            params = match.group(2)  # Parâmetros extraídos
                            occurrences[tool].append(
                                (file_path, line_number, full_call, params)
                            )
    except (FileNotFoundError, PermissionError):
        # Ignora arquivos que não foram encontrados ou sem permissão
        pass

    return occurrences


def find_tool_occurrences(project_path, language):
    # Verifica a extensão dos arquivos com base na linguagem
    file_extension = ".php" if language == "PHP" else ".js"

    # Encontra todos os arquivos correspondentes no diretório
    all_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(file_extension):
                all_files.append(os.path.join(root, file))

    # Paraleliza o processamento dos arquivos usando joblib
    results = Parallel(n_jobs=-1)(
        delayed(process_file)(file, language) for file in all_files
    )

    # Mescla os resultados
    occurrences = {tool: [] for tool in TOOL_PATTERNS.get(language, {})}
    for file_occurrences in results:
        for tool, occurrences_list in file_occurrences.items():
            occurrences[tool].extend(occurrences_list)

    return occurrences


def export_results(occurrences, project_name):
    """
    Exporta os resultados das ocorrências para um arquivo CSV.

    Args:
        occurrences (dict): Ocorrências de ferramentas.
        project_name (str): Nome do projeto.
    """
    tools_detected = [
        tool.lower()
        for tool, tool_occurrences in occurrences.items()
        if tool_occurrences
    ]

    _, proj_name = project_name.split("/")
    owner = _get_owner_from_repo(f"{REPO_PATH}/{PROG_LANG}/{proj_name}")

    with open(
        DATASET_PATH_TEST_PROJECTS, mode="a", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)
        if csv_file.tell() == 0:
            writer.writerow(["lang", "owner", "name", "test_tools"])
        writer.writerow([PROG_LANG, owner, proj_name, tools_detected])


if __name__ == "__main__":
    # Verifica todos os repositórios definidos em REPO_PATH para a linguagem especificada em PROG_LANG
    language_path = os.path.join(REPO_PATH, PROG_LANG)
    if os.path.isdir(language_path):
        for project_directory in os.listdir(language_path):
            project_path = os.path.join(language_path, project_directory)
            if os.path.isdir(project_path):
                project_name = f"{PROG_LANG}/{project_directory}"
                results = find_tool_occurrences(project_path, PROG_LANG)
                export_results(results, project_name)
