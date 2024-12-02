import os, json
import subprocess

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

template = """
Você é um analista de testes
Seu trabalho é analisar o título de issues do github e classifica-las.

Escolha umas das categorias
- Teste de unidade
- Teste de integração
- Teste de sistema

Escolha uma catetoria para esse item:
{text}

Responda apenas com a categoria.
"""

prompt = PromptTemplate.from_template(template=template)
chat = ChatGroq(model="llama-3.1-8b-instant")
chain = prompt | chat
# print(chain.invoke("Raphael").content)


# def run_gh_command(command):
#     try:
#         result = subprocess.run(
#             command, capture_output=True, text=True, check=True, shell=True
#         )
#         print(result.stdout)  # Mostra a saída do comando
#     except subprocess.CalledProcessError as e:
#         print(f"Erro ao executar o comando: {e}")
#         print(f"Saída de erro: {e.stderr}")


# Listar issues e retornar json
# gh issue list --state all \
#     --json number,state,title,labels,updatedAt,assignees \
#     --jq '
#         map([
#             .number,
#             .state,
#             .title,
#             .updatedAt,
#             (.labels | map(.name) | join(",")),
#             (.assignees | map(.login) | join(","))
#         ])[]
#         | @csv
#     '


def run_gh_command(command):
    """Executa um comando do GitHub CLI e retorna a saída em formato JSON."""
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, shell=True
        )
        return json.loads(result.stdout)  # Retorna a saída como um dicionário
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return None


# Exemplo: listar todas as issues de um repositório
repo_owner = "dask"
repo_name = "dask"
# gh_command = f"gh issue list --repo {repo_owner}/{repo_name} --state all"
# run_gh_command(gh_command)


# Listar todas as issues com título e conteúdo
def get_issues(owner, repo):
    """Obtém o título e o corpo das issues de um repositório."""
    # Lista todas as issues com título e corpo
    issues_command = f'gh issue list --repo {owner}/{repo} --search "test" --state all --json number,title --limit 10'
    issues = run_gh_command(issues_command)

    if issues is None:
        print("Não foi possível obter as issues.")
        return
    issues_data = []

    for issue in issues:
        issue_number = issue["number"]

        # Obtém o título e o corpo da issue específica
        issue_view_command = (
            f"gh issue view {issue_number} --repo {owner}/{repo} --json title,body"
        )
        issue_details = run_gh_command(issue_view_command)

        if issue_details is not None:
            # Adiciona um dicionário com os dados da issue à lista
            issues_data.append(
                {
                    "number": issue_number,
                    "title": issue_details["title"],
                    "body": issue_details["body"],
                }
            )

    return issues_data  # Retorna a lista de issues


test_issues = get_issues(repo_owner, repo_name)


def print_issues():
    print(i)


for issue in test_issues:
    category = chain.invoke(issue["title"]).content
    print(
        f'{issue["title"]} (#{issue["number"]}) - {category} - https://github.com/{repo_owner}/{repo_name}/issues/{issue["number"]}'
    )
