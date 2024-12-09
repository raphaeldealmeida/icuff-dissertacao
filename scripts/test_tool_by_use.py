#!/usr/bin/env python3
# coding: utf-8
from test_tool_by_descriptor import _get_owner_from_repo

# Descripton: Verifica em cada projeto, quais ferramentas de teste utilizada pelos projetos

# ===== Configuration variables ======
PROG_LANG = "PHP"
REPO_PATH = "/media/raphaelrsa/de61512f-e8e6-4e0a-9cbc-168ddd77ff20/repos"
DATASET_PATH_TEST_PROJECTS = f"../dataset/{PROG_LANG}_projects_tests_tools2.csv"
ALL_OCCURRENCES_CSV = f"../dataset/{PROG_LANG}_projects_all_occurrences.csv"

import os
import re
import csv
from joblib import Parallel, delayed

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
    },
    "JavaScript": {
        "jest": [
            r"(jest.mock\((.*?)\))",
        ],
        "jasmine": [
            r"(jasmine.Ajax.withMock\((.*?)\))",
        ],
        "tape": [
            r"(t.equal\((.*?)\))",
        ],
        "sinon": [
            r"(sinon.spy\((.*?)\))",
            r"(sinon.mock\((.*?)\))",
        ],
        "testdouble": [
            r"(td.replace\((.*?)\))",
            r"(td.constructor\((.*?)\))",
            r"(td.instance\((.*?)\))",
        ],
        "proxyquire": [
            r"(proxyquire\((.*?)\))",
        ],
        "nock": [
            r"(nock\((.*?)\))",
        ],
    },
    "Java": {
        "powermock": [
            r"(PowerMock.createMock\((.*?)\))",
            r"(PowerMock.createMockAndExpectNew\((.*?)\))",
            r"(PowerMock.createNiceMock\((.*?)\))",
            r"(PowerMock.createNiceMockAndExpectNew\((.*?)\))",
            r"(PowerMock.createNicePartialMock\((.*?)\))",
            r"(PowerMock.createPartialMock\((.*?)\))",
            r"(PowerMock.mockStatic\((.*?)\))",
            r"(PowerMock.mock\((.*?)\))",
            r"(PowerMock.whenNew\((.*?)\))",
        ],
        "mockito": [
            # import static org.mockito.Mockito.mock; mock()
            r"(Mockito.mock\((.*?)\))",
        ],
        "easymock": [
            r"(EasyMock.createMock\((.*?)\))",
            r"(@Mock\((.*?)\))",
            # private Collaborator mock
        ],
        "jmock": [
            r"(new Mockery\((.*?)\))",
            r"(Mockery.mock\((.*?)\))",
        ],
        "wiremock": [
            r"(@WireMockTest\((.*?)\))",
            r"(new WireMockRule\((.*?)\))",
        ],
    },
    "Python": {
        "pytest": [
            r"(@pytest.fixture\((.*?)\))",
            r"(monkeypatch.setattr\((.*?)\))",
        ],
        "unittest": [
            r"(mock.patch\((.*?)\))",
            r"(mock.patch.object\((.*?)\))",
            r"(mock.patch.dict\((.*?)\))",
            r"(MagicMock\((.*?)\))",
        ],
        "mongomock": [
            r"(@mongomock.patch\((.*?)\))",
            r"(mongomock.MongoClient\((.*?)\))",
        ],
        "requests_mock": [
            r"(requests_mock.get\((.*?)\))",
            r"(requests_mock.Mocker\((.*?)\))",
            r"(requests_mock.Mocker\((.*?)\))",
        ],
        "freezegun": [
            r"(@freeze_time\((.*?)\))",
        ],
        "httmock": [
            r"(@urlmatch\((.*?)\))",
            r"(@all_requests\((.*?)\))",
        ],
        "httpretty": [
            r"(@httpretty.activate\((.*?)\))",
            r"(httpretty.register_uri\((.*?)\))",
        ],
        "mocket": [
            r"(@mocketize\((.*?)\))",
            r"(@Mocketizer\((.*?)\))",
        ],
        "responses": [
            r"(responses.patch\((.*?)\))",
            r"(@responses\.activate(?:\((.*?)\))?)",
            r"(@_recorder\.record(?:\((.*?)\))?)",
            r"(responses.RequestsMock\((.*?)\))",
        ],
        "vcrpy": [
            r"(@vcr.use_cassette\((.*?)\))",
            r"(@pytest.mark.vcr\((.*?)\))",
            r"(@pytest.mark.default_cassette\((.*?)\))",
            r"(VCRTestCase(?:\((.*?)\))?)",
            r"(MyTestMixin(?:\((.*?)\))?)",
        ],
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
                            params = (
                                match.group(2) if match.lastindex >= 2 else ""
                            )  # Parâmetros opcionais
                            occurrences[tool].append(
                                (file_path, line_number, full_call, params)
                            )
    except (FileNotFoundError, PermissionError):
        # Ignora arquivos que não foram encontrados ou sem permissão
        pass

    return occurrences


def find_tool_occurrences(project_path, language):
    # Verifica a extensão dos arquivos com base na linguagem
    language_extensions = {
        "PHP": [
            ".php",
        ],
        "JavaScript": [".js", ".ts", ".spec"],
        "Python": [".py"],
        "Java": [".java"],
    }

    file_extensions = language_extensions.get(language, [])

    # Encontra todos os arquivos correspondentes no diretório
    all_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
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


def export_all_occurrences(occurrences, project_name):
    """
    Exporta todas as ocorrências detalhadas para um arquivo CSV.

    Args:
        occurrences (dict): Ocorrências de ferramentas.
        project_name (str): Nome do projeto.
    """
    _, proj_name = project_name.split("/")
    owner = _get_owner_from_repo(f"{REPO_PATH}/{PROG_LANG}/{proj_name}")

    # Grava em CSV
    with open(ALL_OCCURRENCES_CSV, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if csv_file.tell() == 0:
            # Cabeçalho
            writer.writerow(
                [
                    "lang",
                    "owner",
                    "name",
                    "tool",
                    "file_path",
                    "line_number",
                    "full_call",
                    "params",
                ]
            )

        # Escreve todas as ocorrências detectadas
        for tool, occurrences_list in occurrences.items():
            for file_path, line_number, full_call, params in occurrences_list:
                writer.writerow(
                    [
                        PROG_LANG,
                        owner,
                        proj_name,
                        tool,
                        file_path,
                        line_number,
                        full_call,
                        params,
                    ]
                )


def _delete_file(file_path):
    try:
        # Verifica se o arquivo existe
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Arquivo '{file_path}' foi apagado com sucesso.")
        else:
            print(f"O arquivo '{file_path}' não existe.")
    except Exception as e:
        print(f"Erro ao tentar apagar o arquivo: {e}")


if __name__ == "__main__":
    _delete_file(DATASET_PATH_TEST_PROJECTS)
    _delete_file(ALL_OCCURRENCES_CSV)

    # Verifica todos os repositórios definidos em REPO_PATH para a linguagem especificada em PROG_LANG
    language_path = os.path.join(REPO_PATH, PROG_LANG)
    if os.path.isdir(language_path):
        for project_directory in os.listdir(language_path):
            project_path = os.path.join(language_path, project_directory)
            if os.path.isdir(project_path):
                project_name = f"{PROG_LANG}/{project_directory}"
                results = find_tool_occurrences(project_path, PROG_LANG)
                export_results(results, project_name)
                export_all_occurrences(results, project_name)

    # Verifica apenas um repositório
    # project_name = f"{PROG_LANG}/ghidra"
    # results = find_tool_occurrences(f"{REPO_PATH}/{project_name}", PROG_LANG)
    # export_results(results, project_name)
    # export_all_occurrences(results, project_name)
