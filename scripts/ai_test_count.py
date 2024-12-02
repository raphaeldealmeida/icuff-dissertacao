import os, json
import subprocess

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

template = """
Diga quantos testes foram realizados, assertions, skipped, falhas e tempo de execução (em segundos)
Retorne APENAS o JSON com o seguinte padrão:
{{
  "tests": X,
  "assertions": X,
  "skipped": X,
  "failures": X,
  "elapsed time": X
}}


Teste é o conteúdo do log:
{text}
"""

prompt = PromptTemplate.from_template(template=template)
chat = ChatGroq(model="llama-3.1-8b-instant")
chain = prompt | chat


def run_gh_command(command):
    """Executa um comando do GitHub CLI e retorna a saída em formato JSON."""
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, shell=True
        )
        return result.stdout  # Retorna a saída como um dicionário
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return None


repo_owner = "sebastianbergmann"
repo_name = "phpunit"
job_id = 30788640339


# Listar todas as issues com título e conteúdo
def get_log(owner, repo, jobid):
    """Obtém o título e o corpo das issues de um repositório."""
    # Lista todas as issues com título e corpo
    issues_command = f"gh run view --log --job={jobid} -R sebastianbergmann/phpunit  --repo {owner}/{repo}"
    issues = run_gh_command(issues_command)
    return issues


# log_file = get_log(repo_owner, repo_name, job_id)
with open("../dataset/phpunit.log", "r") as file:
    log_file = file.read()

print(chain.invoke({"text": log_file}).content)
