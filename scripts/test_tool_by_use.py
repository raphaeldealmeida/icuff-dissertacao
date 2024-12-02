#!/usr/bin/env python3
# coding: utf-8
from test_tool_by_descriptor import _get_owner_from_repo

# Descripton: Verifica em cada projeto, quais ferramentas de teste utilizada pelos projetos

# ===== Configuration variables ======
PROG_LANG = "PHP"
# REPO_PATH = "../repos"
REPO_PATH = "/media/raphaelrsa/Seagate Expansion Drive/tcc-mocking/repos"
DATASET_PATH_TEST_PROJECTS = f"../dataset/{PROG_LANG}_projects_tests_tools2.csv"

import os
import re
import csv

# Padrões para identificar chamadas específicas de várias ferramentas
TOOL_PATTERNS = {
    "PHP": {
        "PHPUnit": [
            r"(createStub\((.*?)\))",
            r"(createStubForIntersectionOfInterfaces\((.*?)\))",
            r"(createConfiguredStub\((.*?)\))",
            r"(createMock\((.*?)\))",
            r"(createMockForIntersectionOfInterfaces\((.*?)\))",
            r"(createConfiguredMock\((.*?)\))",
            r"(getMockForAbstractClass\((.*?)\))",
            r"(getMockForTrait\((.*?)\))",
            r"(getMockFromWsdl\((.*?)\))",
            r"(getMockBuilder\((.*?)\))",
            r"(setMockClassName\((.*?)\))",
        ],
        "Mockery": [
            r"([Mockery|m]::mock\((.*?)\))",
            r"([Mockery|m]::spy\((.*?)\))",
            r"([Mockery|m]::namedMock\((.*?)\))",
            r"([Mockery|m]::any\((.*?)\))",
        ],
        "vfsStream": [
            r"(vfsStream::setup\((.*?)\))",
            r"(vfsStream::inspect\((.*?)\))",
            r"(vfsStream::newFile\((.*?)\))",
            r"(vfsStream::newDirectory\((.*?)\))",
            r"(vfsStream::url\((.*?)\))",
            r"(vfsStream::create\((.*?)\))",
            r"(vfsStreamFile\((.*?)\))",
            r"(vfsStreamDirectory\((.*?)\))",
            r"(vfsStreamContent::chmod\((.*?)\))",
            r"(vfsStreamContent::chmod\((.*?)\))",
            r"(vfsStreamContent::chmod\((.*?)\))",
            r"(vfsStream::copyFromFileSystem\((.*?)\))",
            r"(vfsStream::newBlock\((.*?)\))",
        ],
        "phpspec": [
            r'class\s+\w+\s+extends\s+ObjectBehavior\s*{[^}]*?\$[\w]+\s*->\s*beADoubleOf\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
        ],
        "prophecy": [
            r"(this->prophet->prophesize\((.*?)\))",
            r"(prophecy->willExtend\((.*?)\))",
            r"(prophecy->willImplement\((.*?)\))",
        ],
        "easymock": [
            r"(this->easyMock\((.*?)\))",
        ],
        "codeception/stub": [
            r"Codeception\\Stub::make\((\w+)\)",
            r"Codeception\\Test\\Feature\Stub::make\((\w+)\)",
            r"use\s+Codeception\\Test\\Feature\\Stub;.*?Stub::make\((.+?)\)",
            r"use\s+Codeception\\Stub;.*?Stub::make\((.+?)\)",
        ],
        "php-mock": [
            r"(new MockBuilder\((.*?)\))",
        ],
    }
}


def find_tool_occurrences(project_path, language):
    """
    Identifica ocorrências de chamadas específicas para diferentes ferramentas em arquivos do projeto.

    Args:
        project_path (str): Caminho para o diretório do projeto.
        language (str): Linguagem de programação do projeto.

    Returns:
        dict: Um dicionário com informações das ferramentas encontradas e suas ocorrências.
    """
    occurrences = {tool: [] for tool in TOOL_PATTERNS.get(language, {})}

    # Verifica a extensão dos arquivos com base na linguagem
    file_extension = ".php" if language == "PHP" else ""

    # Caminha pelo diretório e verifica arquivos com a extensão correspondente
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
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
