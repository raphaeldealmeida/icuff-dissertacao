import re
import json


# Função para processar o arquivo PHP usando uma única regex
def process_php_file(file_path):
    results = []

    # Regex única para capturar classes que estendem ObjectBehavior, métodos e classes usadas como parâmetros
    pattern = (
        r"class\s+\w+\s+extends\s+ObjectBehavior\s*{[^}]*?"
        r"(function\s+\w+\([^)]*?\b(\w+)\s+\$\w+\b[^)]*\))"
    )

    try:
        with open(file_path, "r") as php_file:
            php_code = php_file.read()

        # Encontrar todas as ocorrências
        matches = re.finditer(pattern, php_code)

        for match in matches:
            method_declaration = match.group(
                1
            )  # Captura a linha da declaração do método
            parameter_class = match.group(2)  # Captura a classe do parâmetro
            start_line = (
                php_code[: match.start()].count("\n") + 1
            )  # Determina a linha do match

            results.append(
                {
                    "file": file_path,
                    "line": start_line,
                    "method": method_declaration.strip(),
                    "parameter_class": parameter_class,
                }
            )

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return results


# Exemplo de uso
php_file_path = "scripts/test.php"  # Substitua pelo caminho correto do arquivo
result_data = process_php_file(php_file_path)
print(json.dumps(result_data, indent=4))
