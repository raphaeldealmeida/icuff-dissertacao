# experiment 
import os
import radon.complexity as rdc

def calcular_media_cc(diretorio_projeto):
    total_complexity = 0
    total_funcoes = 0

    for raiz, _, arquivos in os.walk(diretorio_projeto):
        for arquivo in arquivos:
            if arquivo.endswith('.py'):
                arquivo_path = os.path.join(raiz, arquivo)
                with open(arquivo_path, 'r', encoding='utf-8') as file:
                    codigo_fonte = file.read()
                    complexidade_funcoes = rdc.cc_visit(codigo_fonte)
                    total_complexity += sum(func.complexity for func in complexidade_funcoes)
                    total_funcoes += len(complexidade_funcoes)

    if total_funcoes > 0:
        media_cc = total_complexity / total_funcoes
        return media_cc
    else:
        return None

def execute_analisys():
    diretorio_projeto = 'repos/Python/tvm'
    media_cc = calcular_media_cc(diretorio_projeto)

    if media_cc is not None:
        print(f"Média da Complexidade Ciclomática: {media_cc:.2f}")
    else:
        print("Nenhum arquivo Python encontrado no diretório do projeto.")

if __name__ == "__main__":
    execute_analisys()
