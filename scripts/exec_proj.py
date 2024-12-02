# script.py

import os
import subprocess
import re
import json
import yaml
import argparse
import sys
import logging


def setup_logging():
    """Configura o logging para exibir mensagens detalhadas."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )


def find_readme(project_path):
    """Procura o arquivo README com diferentes extensões e variações de letras."""
    possible_names = [
        "README.md",
        "README.rst",
        "README.txt",
        "README",
        "readme.md",
        "readme.rst",
        "readme.txt",
        "readme",
    ]
    for name in possible_names:
        readme_path = os.path.join(project_path, name)
        if os.path.exists(readme_path):
            return readme_path
    return None


def read_readme(project_path):
    """Analisa o README em busca de comandos de teste."""
    logging.info("Analisando o README em busca de comandos de teste.")
    test_commands = []
    readme_path = find_readme(project_path)
    if readme_path:
        logging.info(f"README encontrado: {readme_path}")
        with open(readme_path, "r") as file:
            content = file.read()
            matches = re.findall(r"```bash\n(.*?)\n```", content, re.DOTALL)
            for match in matches:
                if "test" in match:
                    test_commands.extend(match.strip().split("\n"))
    else:
        logging.info("README não encontrado.")
    return test_commands


def analyze_config_files(project_path):
    """Procura por comandos de teste em arquivos de configuração comuns."""
    logging.info("Analisando arquivos de configuração em busca de comandos de teste.")
    test_commands = []
    # Analisando package.json
    package_json_path = os.path.join(project_path, "package.json")
    if os.path.exists(package_json_path):
        logging.info("Encontrado package.json, extraindo comandos de teste.")
        with open(package_json_path, "r") as file:
            data = json.load(file)
            scripts = data.get("scripts", {})
            for key, command in scripts.items():
                if "test" in key.lower():
                    logging.info(
                        f"Comando de teste encontrado no package.json: npm run {key}"
                    )
                    test_commands.append(f"npm run {key}")
    # Analisando Makefile
    makefile_path = os.path.join(project_path, "Makefile")
    if os.path.exists(makefile_path):
        logging.info("Encontrado Makefile, extraindo targets de teste.")
        with open(makefile_path, "r") as file:
            content = file.read()
            targets = re.findall(r"^(.*test.*):", content, re.MULTILINE)
            for target in targets:
                logging.info(
                    f"Target de teste encontrado no Makefile: make {target.strip()}"
                )
                test_commands.append(f"make {target.strip()}")
    # Analisando setup.py
    setup_py_path = os.path.join(project_path, "setup.py")
    if os.path.exists(setup_py_path):
        logging.info("Encontrado setup.py, adicionando comando de teste.")
        logging.info("Comando de teste encontrado no setup.py: python setup.py test")
        test_commands.append("python setup.py test")
    return test_commands


def analyze_github_actions(project_path):
    """Extrai comandos de teste dos workflows do GitHub Actions."""
    logging.info("Analisando workflows do GitHub Actions.")
    test_commands = []
    workflows_path = os.path.join(project_path, ".github", "workflows")
    if os.path.exists(workflows_path):
        for root, _, files in os.walk(workflows_path):
            for filename in files:
                if filename.endswith((".yml", ".yaml")):
                    filepath = os.path.join(root, filename)
                    logging.info(f"Analisando workflow: {filepath}")
                    with open(filepath, "r") as file:
                        content = yaml.safe_load(file)
                        if content is None:
                            continue
                        jobs = content.get("jobs", {})
                        for job_name, job in jobs.items():
                            logging.debug(f"Analisando job: {job_name}")
                            steps = job.get("steps", [])
                            for step in steps:
                                if "run" in step and "test" in step["run"]:
                                    logging.info(
                                        f"Comando de teste encontrado no workflow {filename}: {step['run']}"
                                    )
                                    test_commands.append(step["run"])
    else:
        logging.info("Nenhum workflow do GitHub Actions encontrado.")
    return test_commands


def deduplicate_commands(commands):
    """Remove comandos duplicados mantendo a ordem."""
    logging.info("Removendo comandos duplicados.")
    seen = set()
    deduped_commands = []
    for cmd in commands:
        if cmd not in seen:
            seen.add(cmd)
            deduped_commands.append(cmd)
    return deduped_commands


def detect_project_type(project_path):
    """Detecta o tipo de projeto (Python, Node.js, etc.) com base nos arquivos presentes."""
    logging.info("Detectando o tipo de projeto.")
    if os.path.exists(os.path.join(project_path, "requirements.txt")) or os.path.exists(
        os.path.join(project_path, "setup.py")
    ):
        return "python"
    elif os.path.exists(os.path.join(project_path, "package.json")):
        return "node"
    else:
        return "unknown"


def install_dependencies(docker_image, project_path):
    """Gera o comando para instalar dependências dentro do Docker."""
    if docker_image.startswith("python"):
        logging.info("Preparando comando para instalar dependências Python.")
        if os.path.exists(os.path.join(project_path, "requirements.txt")):
            return "pip install -r requirements.txt"
        elif os.path.exists(os.path.join(project_path, "setup.py")):
            return "pip install ."
    elif docker_image.startswith("node"):
        logging.info("Preparando comando para instalar dependências Node.js.")
        return "npm install"
    return ""


def execute_tests_in_docker(commands, project_path, language, version):
    """Executa os comandos de teste dentro de um contêiner Docker."""
    logging.info("Executando testes dentro de um contêiner Docker.")
    results = {}

    if language:
        project_type = language
        logging.info(f"Linguagem especificada pelo usuário: {language}")
    else:
        project_type = detect_project_type(project_path)
        logging.info(f"Linguagem detectada: {project_type}")

    if version:
        logging.info(f"Versão especificada pelo usuário: {version}")

    if project_type == "python":
        docker_image = f"python:{version}" if version else "python:3.10"
    elif project_type == "node":
        docker_image = f"node:{version}-alpine" if version else "node:14-alpine"
    else:
        logging.error(
            "Tipo de projeto desconhecido. Não é possível instalar dependências."
        )
        return {}

    install_cmd = install_dependencies(docker_image, project_path)
    if not install_cmd:
        logging.warning("Nenhum comando de instalação de dependências encontrado.")

    for cmd in commands:
        logging.info(f"Executando comando de teste: {cmd}")
        docker_command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.path.abspath(project_path)}:/app",
            "-w",
            "/app",
            docker_image,
            "bash",
            "-c",
            f'"{install_cmd} && {cmd}"',
        ]
        logging.debug(f"Comando Docker: {' '.join(docker_command)}")
        try:
            output = subprocess.check_output(docker_command, stderr=subprocess.STDOUT)
            logging.info(f"Saída do comando Docker:\n{output.decode('utf-8')}")
            results[cmd] = ("Sucesso", output.decode("utf-8"))
            logging.info(f"Teste '{cmd}' executado com sucesso.")
        except subprocess.CalledProcessError as e:
            logging.error(
                f"Saída do comando Docker (erro):\n{e.output.decode('utf-8')}"
            )
            results[cmd] = ("Falha", e.output.decode("utf-8"))
            logging.error(f"Teste '{cmd}' falhou.")

    return results


def summarize_results(results):
    """Gera um sumário dos resultados dos testes."""
    logging.info("Gerando sumário dos resultados dos testes.")
    print("\nResumo dos Resultados dos Testes:")
    for cmd, (status, output) in results.items():
        print(f"\nComando: {cmd}\nStatus: {status}\nSaída:\n{output}\n{'-'*60}")


def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Executa testes de um projeto clonado."
    )
    parser.add_argument("project_path", help="Caminho para o diretório do projeto")
    parser.add_argument(
        "--language",
        choices=["python", "node"],
        help="Linguagem do projeto (python, node)",
    )
    parser.add_argument("--version", help="Versão da linguagem do projeto")
    args = parser.parse_args()

    project_path = args.project_path
    language = args.language
    version = args.version

    if not os.path.isdir(project_path):
        logging.error(
            f"O caminho especificado não é um diretório válido: {project_path}"
        )
        sys.exit(1)

    logging.info(f"Iniciando análise do projeto em: {project_path}")

    test_commands = []
    test_commands.extend(read_readme(project_path))
    test_commands.extend(analyze_config_files(project_path))
    test_commands.extend(analyze_github_actions(project_path))
    test_commands = deduplicate_commands(test_commands)

    if not test_commands:
        logging.warning("Nenhum comando de teste encontrado.")
        print("Nenhum comando de teste encontrado.")
        return

    results = execute_tests_in_docker(test_commands, project_path, language, version)
    summarize_results(results)


if __name__ == "__main__":
    main()
