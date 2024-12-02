import os
import re

# Padrões para identificar chamadas específicas de várias ferramentas
TOOL_PATTERNS = {
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
    ],
    "vfsStream": [
        r"(vfsStream::setup\((.*?)\))",
        r"(vfsStream::inspect\((.*?)\))",
        r"(vfsStream::newFile\((.*?)\))",
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
    # "codeception/stub": [
    #     r"(Codeception\\Stub::make\((.*?)\))",
    #     r"(Codeception\\Test\\Feature\Stub::make\((.*?)\))",
    #     r"(Codeception\\Test\\Feature\Stub::makeEmpty\((.*?)\))",
    #     r"(Codeception\\Test\\Feature\Stub::makeEmptyExcept\((.*?)\))",
    #     r"(Codeception\\Test\\Feature\Stub::construct\((.*?)\))",
    #     r"(Codeception\\Test\\Feature\Stub::constructEmpty\((.*?)\))",
    #     r"(Codeception\\Test\\Feature\Stub::constructEmptyExcept\((.*?)\))",
    # ],
    "php-mock": [
        r"(new MockBuilder\((.*?)\))",
    ],
}


def find_tool_occurrences(project_path):
    """
    Identifica ocorrências de chamadas específicas para diferentes ferramentas em arquivos PHP.

    Args:
        project_path (str): Caminho para o diretório do projeto.

    Returns:
        dict: Um dicionário com informações das ferramentas encontradas e suas ocorrências.
    """
    occurrences = {tool: [] for tool in TOOL_PATTERNS}

    # Caminha pelo diretório e verifica arquivos com extensão .php
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".php"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    for line_number, line_content in enumerate(lines, start=1):
                        for tool, patterns in TOOL_PATTERNS.items():
                            for pattern in patterns:
                                match = re.search(pattern, line_content)
                                if match:
                                    full_call = match.group(1)  # Chamada completa
                                    params = match.group(2)  # Parâmetros extraídos
                                    occurrences[tool].append(
                                        (file_path, line_number, full_call, params)
                                    )

    return occurrences


def summarize_results(occurrences, project_name, list_individual=False):
    """
    Gera um sumário das ocorrências por ferramenta.

    Args:
        occurrences (dict): Ocorrências de ferramentas.
        project_name (str): Nome do projeto.
        list_individual (bool): Se True, lista cada ocorrência detalhadamente.
    """
    print(f"\n--- Sumário do Projeto: {project_name} ---")
    total_tools = 0

    for tool, tool_occurrences in occurrences.items():
        if tool_occurrences:
            total_tools += 1
            method_counts = {}
            for _, _, method_call, _ in tool_occurrences:
                method_name = method_call.split("(")[0]
                method_counts[method_name] = method_counts.get(method_name, 0) + 1

            print(f"\nFerramenta detectada: {tool}")
            print(f"Total de chamadas: {len(tool_occurrences)}")
            for method, count in method_counts.items():
                print(f"  {method}: {count} ocorrências")

            if list_individual:
                print("\nDetalhes das ocorrências:")
                for file_path, line_number, method_call, params in tool_occurrences:
                    print(f"  Arquivo: {file_path}, Linha: {line_number}")
                    print(f"    Chamada: {method_call}")
                    print(f"    Parâmetros: {params}\n")
        else:
            print(f"\nFerramenta {tool}: Nenhuma ocorrência encontrada.")

    if total_tools == 0:
        print("\nNenhuma ferramenta detectada no projeto.")


if __name__ == "__main__":
    # Caminho para o diretório do projeto
    project_directory = input("Digite o caminho do projeto para verificar: ").strip()
    project_name = os.path.basename(project_directory)

    # Flag para listar detalhes de cada ocorrência
    list_individual = (
        input("Deseja listar cada ocorrência individualmente? (s/n): ").strip().lower()
        == "s"
    )

    results = find_tool_occurrences(project_directory)
    summarize_results(results, project_name, list_individual)
