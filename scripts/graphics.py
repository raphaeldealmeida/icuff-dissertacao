import matplotlib.pyplot as plt
import pandas as pd
import csv, glob
from collections import defaultdict

GRAPHCS_PATH = "../graphics/"

colors_contrast = {
    "Completa": "#1f77b4",  # Azul
    "DB": "#2ca02c",  # Verde
    "HTTP": "#ff7f0e",  # Laranja
    "Mock": "#d62728",  # Vermelho
    "Time": "#9467bd",  # Roxo,
    "File": "#8c564b",  # Marrom
}


def plot_test_corpus():
    # Dados da tabela de projetos com testes automatizados
    data_projetos = {
        "Linguagem": ["PHP", "Java", "JavaScript", "Python", "Total"],
        "Projetos": [44, 163, 137, 135, 479],
        "Projetos c/ testes": [41, 157, 119, 124, 441],
    }

    # Criar DataFrame para os projetos
    df_projetos = pd.DataFrame(data_projetos)

    # Calcular a parte que corresponde aos projetos sem testes
    df_projetos["Projetos s/ testes"] = (
        df_projetos["Projetos"] - df_projetos["Projetos c/ testes"]
    )

    # Plotar gráfico de barras empilhadas com cores mais escuras e adicionar porcentagens
    plt.figure(figsize=(10, 6))
    plt.bar(
        df_projetos["Linguagem"],
        df_projetos["Projetos s/ testes"],
        label="Projetos s/ Testes",
        color="#d62728",
    )
    plt.bar(
        df_projetos["Linguagem"],
        df_projetos["Projetos c/ testes"],
        label="Projetos c/ Testes",
        bottom=df_projetos["Projetos s/ testes"],
        color="#2ca02c",
    )

    # Adicionar porcentagens em cada segmento
    for idx, row in df_projetos.iterrows():
        total = row["Projetos"]
        c_testes = row["Projetos c/ testes"]
        s_testes = row["Projetos s/ testes"]
        plt.text(
            idx,
            s_testes / 2,
            f"{(s_testes / total) * 100:.1f}%",
            ha="center",
            va="center",
            color="white",
        )
        plt.text(
            idx,
            s_testes + c_testes / 2,
            f"{(c_testes / total) * 100:.1f}%",
            ha="center",
            va="center",
            color="white",
        )

    # Adicionar labels e título
    plt.xlabel("Linguagem")
    plt.ylabel("Número de Projetos")
    plt.title("Projetos com Testes Automatizados por Linguagem")

    # Adicionar legenda
    plt.legend()

    # Exibir o gráfico
    plt.tight_layout()
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}test_corpus.png")


def plot_python_mock_tools():
    # Atualizar os dados da tabela Python
    data_python = {
        "Ferramenta": [
            "pytest",
            "unittest",
            "mongomock",
            "requests-mock",
            "douplex",
            "freezegun",
            "httmock",
            "HTTPretty",
            "mocket",
            "responses",
            "vcrpy",
        ],
        "Tipo": [
            "Completa",
            "Completa",
            "DB",
            "HTTP",
            "Mock",
            "Time",
            "HTTP",
            "HTTP",
            "HTTP",
            "HTTP",
            "HTTP",
        ],
        "Qtd de Estrelas": [
            11900,
            None,
            946,
            400,
            11,
            4100,
            466,
            2100,
            281,
            4100,
            2700,
        ],
    }

    # Criar DataFrame para Python
    df_python = pd.DataFrame(data_python)

    # Substituir valores None para unittest
    df_python["Qtd de Estrelas"] = df_python["Qtd de Estrelas"].fillna(0)

    # Adicionar cores ao gráfico
    color_list_python = df_python["Tipo"].map(colors_contrast)

    # Criar o novo campo de nome de ferramenta
    df_python["Ferramenta_Color"] = df_python.apply(
        lambda row: (
            f"{row['Ferramenta']}"
            if row["Ferramenta"] != "unittest"
            else "unittest (Completa)"
        ),
        axis=1,
    )

    # Plotar gráfico de barras horizontais para Python
    plt.figure(figsize=(10, 6))
    bars_python = plt.barh(
        df_python["Ferramenta_Color"],
        df_python["Qtd de Estrelas"],
        color=color_list_python,
    )

    # Adicionar rótulos aos valores das barras
    for bar in bars_python:
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}" if bar.get_width() > 0 else "Não Observado",
            va="center",
        )

    # Título e labels
    plt.xlabel("Quantidade de Estrelas")
    plt.ylabel("Ferramenta")
    plt.title("Ferramentas de Mock por Quantidade de Estrelas (Python)")

    # Legenda com cores contrastantes
    legend_labels_python = [
        plt.Rectangle((0, 0), 1, 1, color=colors_contrast[key])
        for key in colors_contrast
    ]
    plt.legend(legend_labels_python, colors_contrast.keys(), title="Tipo de Ferramenta")

    # Exibir o gráfico
    plt.tight_layout()
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}python_mock_tools.png")


def plot_javascript_mock_tools():
    # Dados da tabela JavaScript
    data_js = {
        "Ferramenta": [
            "jest",
            "jasmine",
            "mocha",
            "ava",
            "simon",
            "testdouble",
            "proxyquire",
            "nock",
            "tape",
        ],
        "Tipo": [
            "Completa",
            "Completa",
            "Completa",
            "Completa",
            "Mock",
            "Mock",
            "Mock",
            "HTTP",
            "Completa",
        ],
        "Qtd de Estrelas": [44100, 15700, 22600, 20700, 9600, 1400, 2700, 12700, 5800],
    }

    # Criando DataFrame para JavaScript
    df_js = pd.DataFrame(data_js)

    # Adicionar cores ao tipo de ferramenta JavaScript com o mesmo esquema de cores
    color_list_js = df_js["Tipo"].map(colors_contrast)

    # Criar um novo campo com o nome e tipo de ferramenta
    df_js["Ferramenta_Color"] = df_js.apply(
        lambda row: f"{row['Ferramenta']} ({row['Tipo']})", axis=1
    )

    # Plotar gráfico de barras horizontais para ferramentas de Mock em JavaScript
    plt.figure(figsize=(10, 6))
    bars_js = plt.barh(
        df_js["Ferramenta_Color"], df_js["Qtd de Estrelas"], color=color_list_js
    )

    # Adicionar rótulos aos valores das barras
    for bar in bars_js:
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}" if bar.get_width() > 0 else "Não Observado",
            va="center",
        )

    # Título e labels
    plt.xlabel("Quantidade de Estrelas")
    plt.ylabel("Ferramenta")
    plt.title("Ferramentas de Mock por Quantidade de Estrelas (JavaScript)")

    # Legenda com cores contrastantes
    legend_labels_js = [
        plt.Rectangle((0, 0), 1, 1, color=colors_contrast[key])
        for key in colors_contrast
    ]
    plt.legend(legend_labels_js, colors_contrast.keys(), title="Tipo de Ferramenta")

    # Exibir o gráfico
    plt.tight_layout()
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}javascript_mock_tools.png")


def plot_php_mock_tools():

    data_php = {
        "Ferramenta": [
            "phpunit",
            "codeception",
            "phpspec",
            "mockery",
            "prophecy",
            "php-mock",
            "vfsstream",
        ],
        "Tipo": ["Completa", "Completa", "Completa", "Mock", "Mock", "Mock", "File"],
        "Qtd de Estrelas": [19700, 4800, 1900, 10600, 8500, 359, 1400],
    }

    # Criando DataFrame para JavaScript
    df_js = pd.DataFrame(data_php)

    # Adicionar cores ao tipo de ferramenta JavaScript com o mesmo esquema de cores
    color_list_js = df_js["Tipo"].map(colors_contrast)

    # Criar um novo campo com o nome e tipo de ferramenta
    df_js["Ferramenta_Color"] = df_js.apply(
        lambda row: f"{row['Ferramenta']} ({row['Tipo']})", axis=1
    )

    # Plotar gráfico de barras horizontais para ferramentas de Mock em JavaScript
    plt.figure(figsize=(10, 6))
    bars_js = plt.barh(
        df_js["Ferramenta_Color"], df_js["Qtd de Estrelas"], color=color_list_js
    )

    # Adicionar rótulos aos valores das barras
    for bar in bars_js:
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}" if bar.get_width() > 0 else "Não Observado",
            va="center",
        )

    # Título e labels
    plt.xlabel("Quantidade de Estrelas")
    plt.ylabel("Ferramenta")
    plt.title("Ferramentas de Mock por Quantidade de Estrelas (PHP)")

    # Legenda com cores contrastantes
    legend_labels_js = [
        plt.Rectangle((0, 0), 1, 1, color=colors_contrast[key])
        for key in colors_contrast
    ]
    plt.legend(legend_labels_js, colors_contrast.keys(), title="Tipo de Ferramenta")

    # Exibir o gráfico
    plt.tight_layout()
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}php_mock_tools.png")


def plot_java_mock_tools():

    data_java = {
        "Ferramenta": [
            "powermock",
            "mockito",
            "easymock",
            "jmock",
            "hoverfly-java",
            "karate",
            "wiremock",
            "jmockit",
            "mock-server",
        ],
        "Tipo": [
            "Mock",
            "Mock",
            "Mock",
            "Mock",
            "HTTP",
            "Completa",
            "HTTP",
            "Mock",
            "HTTP",
        ],
        "Qtd de Estrelas": [4200, 14800, 820, 133, 168, 8100, 6300, 461, 4600],
    }

    # Criando DataFrame para JavaScript
    df_js = pd.DataFrame(data_java)

    # Adicionar cores ao tipo de ferramenta JavaScript com o mesmo esquema de cores
    color_list_js = df_js["Tipo"].map(colors_contrast)

    # Criar um novo campo com o nome e tipo de ferramenta
    df_js["Ferramenta_Color"] = df_js.apply(
        lambda row: f"{row['Ferramenta']} ({row['Tipo']})", axis=1
    )

    # Plotar gráfico de barras horizontais para ferramentas de Mock em JavaScript
    plt.figure(figsize=(10, 6))
    bars_js = plt.barh(
        df_js["Ferramenta_Color"], df_js["Qtd de Estrelas"], color=color_list_js
    )

    # Adicionar rótulos aos valores das barras
    for bar in bars_js:
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}" if bar.get_width() > 0 else "Não Observado",
            va="center",
        )

    # Título e labels
    plt.xlabel("Quantidade de Estrelas")
    plt.ylabel("Ferramenta")
    plt.title("Ferramentas de Mock por Quantidade de Estrelas (Java)")

    # Legenda com cores contrastantes
    legend_labels_js = [
        plt.Rectangle((0, 0), 1, 1, color=colors_contrast[key])
        for key in colors_contrast
    ]
    plt.legend(legend_labels_js, colors_contrast.keys(), title="Tipo de Ferramenta")

    # Exibir o gráfico
    plt.tight_layout()
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}java_mock_tools.png")


def plot_mocks_por_linguagem():
    colors_by_language = {
        "PHP": "#ff7f0e",  # Laranja
        "Java": "#1f77b4",  # Azul
        "JavaScript": "#2ca02c",  # Verde
        "Python": "#d62728",  # Vermelho
    }
    # Atualizar os dados com as porcentagens exatas da tabela fornecida
    data_mocking_updated = {
        "Linguagem": [
            "PHP",
            "PHP",
            "PHP",
            "PHP",
            "PHP",
            "PHP",
            "Java",
            "Java",
            "Java",
            "Java",
            "JavaScript",
            "JavaScript",
            "JavaScript",
            "JavaScript",
            "JavaScript",
            "Python",
            "Python",
            "Python",
            "Python",
        ],
        "Ferramenta": [
            "phpunit",
            "mockery",
            "vfsStream",
            "phpspec",
            "php-mock",
            "codeception",
            "mockito",
            "powermock",
            "easymock",
            "jmock",
            "Jest",
            "SinonJs",
            "Nock",
            "Proxyquire",
            "Testdouble.js",
            "Mock",
            "Freezegun",
            "requests_mock",
            "Httpretty",
        ],
        "Nº de Repositórios": [
            41,
            20,
            19,
            18,
            9,
            7,
            99,
            21,
            11,
            9,
            51,
            42,
            20,
            11,
            1,
            75,
            16,
            13,
            3,
        ],
        "% Uso": [
            100,
            49,
            46,
            44,
            21,
            17,
            63,
            13,
            7,
            6,
            42,
            35,
            16,
            9,
            0.8,
            60,
            13,
            10,
            2,
        ],
    }

    # Criar DataFrame atualizado
    df_mocking_updated = pd.DataFrame(data_mocking_updated)

    # Plotar gráfico de barras empilhadas com porcentagem de uso (eixo X)
    plt.figure(figsize=(12, 6))

    # Filtrar os dados por linguagem e aplicar a cor correta, adicionar os rótulos
    for linguagem in df_mocking_updated["Linguagem"].unique():
        dados_linguagem = df_mocking_updated[
            df_mocking_updated["Linguagem"] == linguagem
        ]
        bars = plt.barh(
            dados_linguagem["Ferramenta"],
            dados_linguagem["% Uso"],
            label=linguagem,
            color=colors_by_language[linguagem],
        )

        # Adicionar os rótulos fora das barras com o valor de repositórios e a porcentagem
        for bar, repos, pct in zip(
            bars, dados_linguagem["Nº de Repositórios"], dados_linguagem["% Uso"]
        ):
            plt.text(
                bar.get_width() + 1,
                bar.get_y() + bar.get_height() / 2,
                f"{int(repos)} ({pct:.1f}%)",
                va="center",
                ha="left",
                color="black",
                fontsize=10,
            )

    # Título e labels
    plt.xlabel("% de Uso")
    plt.ylabel("Ferramenta")
    plt.title("Uso das Ferramentas de Mocking Separado por Linguagem")

    # Adicionar legenda
    plt.legend(title="Linguagem")

    # Exibir o gráfico
    plt.tight_layout()
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}mocks_por_linguagem.png")


def plot_dep_type():
    data_dependencia = {
        "Linguagem": [
            "PHP",
            "PHP",
            "PHP",
            "Java",
            "Java",
            "Java",
            "JavaScript",
            "JavaScript",
            "JavaScript",
            "Python",
            "Python",
            "Python",
        ],
        "Tipo de Dependência": [
            "Interna",
            "Externa",
            "Indefinida",
            "Interna",
            "Externa",
            "Indefinida",
            "Interna",
            "Externa",
            "Indefinida",
            "Interna",
            "Externa",
            "Indefinida",
        ],
        "Nº de Mocks": [
            1927,
            4666,
            2,
            3874,
            7530,
            178,
            1128,
            4560,
            166,
            6545,
            8844,
            575,
        ],
        "Proporção": [
            29.22,
            70.75,
            0.03,
            33.79,
            65.68,
            0.53,
            19.23,
            77.77,
            3.00,
            41.00,
            55.40,
            3.60,
        ],
    }
    df_dependencia = pd.DataFrame(data_dependencia)

    # Definir cores para cada tipo de dependência
    colors_dependencia = {
        "Interna": "#1f77b4",  # Azul
        "Externa": "#ff7f0e",  # Laranja
        "Indefinida": "#2ca02c",  # Verde
    }

    df_dependencia_grouped = df_dependencia.pivot_table(
        values="Proporção", index="Linguagem", columns="Tipo de Dependência"
    ).fillna(0)

    plt.figure(figsize=(10, 6))

    # Barras empilhadas por tipo de dependência
    bars_interna = plt.bar(
        df_dependencia_grouped.index,
        df_dependencia_grouped["Interna"],
        label="Interna",
        color=colors_dependencia["Interna"],
    )
    bars_externa = plt.bar(
        df_dependencia_grouped.index,
        df_dependencia_grouped["Externa"],
        bottom=df_dependencia_grouped["Interna"],
        label="Externa",
        color=colors_dependencia["Externa"],
    )
    bars_indefinida = plt.bar(
        df_dependencia_grouped.index,
        df_dependencia_grouped["Indefinida"],
        bottom=df_dependencia_grouped["Interna"] + df_dependencia_grouped["Externa"],
        label="Indefinida",
        color=colors_dependencia["Indefinida"],
    )

    # Adicionar rótulos dentro das barras para o nº de Mocks e a porcentagem
    for bars, tipo in zip(
        [bars_interna, bars_externa, bars_indefinida],
        ["Interna", "Externa", "Indefinida"],
    ):
        for bar, linguagem in zip(bars, df_dependencia_grouped.index):
            valor_mock = df_dependencia[
                (df_dependencia["Linguagem"] == linguagem)
                & (df_dependencia["Tipo de Dependência"] == tipo)
            ]["Nº de Mocks"].values[0]
            valor_pct = df_dependencia[
                (df_dependencia["Linguagem"] == linguagem)
                & (df_dependencia["Tipo de Dependência"] == tipo)
            ]["Proporção"].values[0]
            if bar.get_height() > 0:
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(valor_mock)} ({valor_pct:.1f}%)",
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=10,
                )

    # Título e labels
    plt.xlabel("Linguagem")
    plt.ylabel("Proporção (%)")
    plt.title("Proporção de Tipos de Dependência por Linguagem")

    # Adicionar legenda fora do gráfico
    plt.legend(title="Tipo de Dependência", bbox_to_anchor=(1.05, 1), loc="upper left")

    # Exibir o gráfico
    plt.tight_layout()
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}dep_type.png")


def plot_mocktools_groups():
    import networkx as nx

    edge_color_fixed = "gray"

    # Criar grafo
    G = nx.Graph()

    # Adicionar arestas (tuplas) para cada linguagem
    # PHP
    G.add_edge("prophecy", "phpspec", weight=18)
    G.add_edge("phpspec", "mockery", weight=17)
    G.add_edge("prophecy", "mockery", weight=17)

    # Python
    G.add_edge("pytest", "unittest", weight=82)
    G.add_edge("responses", "unittest", weight=56)
    G.add_edge("responses", "pytest", weight=51)

    # Java
    G.add_edge("powermock", "mockito", weight=21)
    G.add_edge("wiremock", "mockito", weight=20)

    # JavaScript
    G.add_edge("jest", "ava", weight=31)
    G.add_edge("mocha", "ava", weight=31)
    G.add_edge("mocha", "jest", weight=25)

    # Definir cores por linguagem
    colors_by_language = {
        "PHP": "lightcoral",
        "Python": "lightblue",
        "Java": "lightgreen",
        "JavaScript": "lightgoldenrodyellow",
    }

    node_colors = {
        "prophecy": colors_by_language["PHP"],
        "phpspec": colors_by_language["PHP"],
        "mockery": colors_by_language["PHP"],
        "pytest": colors_by_language["Python"],
        "unittest": colors_by_language["Python"],
        "responses": colors_by_language["Python"],
        "powermock": colors_by_language["Java"],
        "mockito": colors_by_language["Java"],
        "wiremock": colors_by_language["Java"],
        "jest": colors_by_language["JavaScript"],
        "mocha": colors_by_language["JavaScript"],
        "ava": colors_by_language["JavaScript"],
    }

    # Criar lista de cores para as arestas com base nas linguagens
    edge_colors = [
        colors_by_language["PHP"],
        colors_by_language["PHP"],
        colors_by_language["PHP"],  # PHP
        colors_by_language["Python"],
        colors_by_language["Python"],
        colors_by_language["Python"],  # Python
        colors_by_language["Java"],
        colors_by_language["Java"],  # Java
        colors_by_language["JavaScript"],
        colors_by_language["JavaScript"],
        colors_by_language["JavaScript"],  # JavaScript
    ]

    # Ajustar as posições para reduzir o espaço horizontal entre os grupos
    pos_adjusted = {
        "prophecy": (-0.5, 1),
        "phpspec": (-0.25, 1),
        "mockery": (-0.375, 0.5),
        "pytest": (0.25, 1),
        "unittest": (0.5, 1),
        "responses": (0.375, 0.5),
        "powermock": (-0.5, -0.5),
        "mockito": (-0.375, -1),
        "wiremock": (-0.25, -0.5),
        "jest": (0.25, -0.5),
        "mocha": (0.375, -1),
        "ava": (0.5, -0.5),
    }

    # Plotar o grafo de rede com o ajuste nas posições
    plt.figure(figsize=(10, 6))

    # Desenhar o grafo com as cores dos nós representando as linguagens, arestas com cor fixa
    nx.draw(
        G,
        pos_adjusted,
        with_labels=True,
        node_color=[node_colors[node] for node in G.nodes()],
        edge_color=edge_color_fixed,
        node_size=3000,
        font_size=10,
        font_weight="bold",
        width=2,
    )
    edge_labels = nx.get_edge_attributes(G, "weight")
    # Adicionar rótulos com pesos nas arestas (número de projetos)
    nx.draw_networkx_edge_labels(
        G,
        pos_adjusted,
        edge_labels=edge_labels,
        font_size=10,
        bbox=dict(facecolor="white", edgecolor="none", pad=0.5),
    )

    # Título e legenda
    plt.title(
        "Ferramentas Adotadas em Conjunto por Linguagem (Distribuídas por Quadrantes)"
    )

    # Exibir o gráfico
    # plt.tight_layout()
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}mocktools_groups.png")


def plot_tools_languages():
    # Dados convertidos para formato de gráfico de barras empilhadas
    # data_converted = {
    #     "Linguagem": ["Java", "JavaScript", "PHP", "Python"],
    #     "pytest": [0, 0, 0, 95],
    #     "unittest": [0, 0, 0, 108],
    #     "mongomock": [0, 0, 0, 1],
    #     "requests_mock": [0, 0, 0, 12],
    #     "douplex": [0, 0, 0, 0],
    #     "freezegun": [0, 0, 0, 14],
    #     "httmock": [0, 0, 0, 0],
    #     "httpretty": [0, 0, 0, 2],
    #     "mocket": [0, 0, 0, 0],
    #     "responses": [0, 0, 0, 56],
    #     "vcrpy": [0, 0, 0, 2],
    #     "powermock": [20, 0, 0, 0],
    #     "mockito": [97, 0, 0, 0],
    #     "easymock": [9, 0, 0, 0],
    #     "jmock": [7, 0, 0, 0],
    #     "hoverfly-java": [0, 0, 0, 0],
    #     "karate": [0, 0, 0, 0],
    #     "wiremock": [21, 0, 0, 0],
    #     "jmockit": [4, 0, 0, 0],
    #     "mock-server": [5, 0, 0, 0],
    #     "jest": [0, 51, 0, 0],
    #     "jasmine": [0, 26, 0, 0],
    #     "mocha": [0, 59, 0, 0],
    #     "ava": [0, 57, 0, 0],
    #     "sinon": [0, 0, 0, 0],
    #     "testdouble": [0, 0, 0, 0],
    #     "proxyquire": [0, 0, 0, 0],
    #     "nock": [0, 0, 0, 0],
    #     "tape": [0, 11, 0, 0],
    #     "phpunit": [0, 0, 42, 0],
    #     "codeception": [0, 0, 8, 0],
    #     "phpspec": [0, 0, 17, 0],
    #     "mockery": [0, 0, 20, 0],
    #     "prophecy": [0, 0, 16, 0],
    #     "php-mock": [0, 0, 8, 0],
    #     "vfsstream": [0, 0, 15, 0],
    # }

    file_paths = glob.glob("../dataset/*_projects_tests_tools2.csv")
    # Converter os dados de todos os arquivos
    data_converted = convert_multiple_csvs_to_variable(file_paths)
    # Convertendo o dicionário para um DataFrame para visualização
    df_converted = pd.DataFrame(data_converted)

    # Definir a coluna 'Linguagem' como o índice
    df_converted.set_index("Linguagem", inplace=True)

    # Plotting the stacked bar chart
    plt.figure(figsize=(10, 8))  # Aumentando a altura do gráfico
    ax = df_converted.plot(
        kind="bar", stacked=True, figsize=(10, 8), legend=False
    )  # Removendo a legenda

    # Adicionando o rótulo com o nome da ferramenta e a quantidade no formato "Nome (XX)"
    for i, container in enumerate(ax.containers):
        for rect in container:
            height = rect.get_height()
            if height > 0:
                ax.text(
                    rect.get_x() + rect.get_width() / 2,  # Posição X
                    rect.get_y() + rect.get_height() / 2,  # Posição Y
                    f"{df_converted.columns[i]} ({int(height)})",  # Nome da ferramenta + quantidade
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="black",
                )

    # Ajustando os rótulos das linguagens para ficarem na horizontal
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha="center")

    plt.title("Gráfico de Barras Empilhadas - Ferramentas de Mock por Linguagem")
    plt.ylabel("Nº de Repositórios")
    plt.xlabel("Linguagem")

    plt.tight_layout()
    plt.savefig(f"{GRAPHCS_PATH}tools_languages.png")

    import csv


def convert_multiple_csvs_to_variable(file_paths):
    """
    Lê vários arquivos CSV no formato especificado e combina os dados no formato solicitado.
    Corrige conflitos entre nomes como "Java" e "JavaScript".

    Args:
        file_paths (list): Lista de caminhos para os arquivos CSV.

    Returns:
        dict: Dados combinados no formato solicitado.
    """
    # Inicializar estrutura de dados
    data = defaultdict(
        lambda: [0, 0, 0, 0]
    )  # Formato para Java, JavaScript, PHP, Python

    # Mapear linguagens para índices
    lang_to_index = {"JavaScript": 1, "Java": 0, "PHP": 2, "Python": 3}

    # Processar cada arquivo CSV
    for file_path in file_paths:
        # Inferir a linguagem a partir do nome do arquivo
        lang_index = None
        for lang in lang_to_index:
            if lang.lower() in file_path.lower():
                lang_index = lang_to_index[lang]
                break
        if lang_index is None:
            raise ValueError(f"Linguagem não reconhecida no arquivo: {file_path}")

        # Ler o arquivo CSV
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tools = eval(row["test_tools"])  # Converter string para lista
                for tool in tools:
                    data[tool][lang_index] += 1

    # Adicionar linguagens ao resultado
    result = {"Linguagem": ["Java", "JavaScript", "PHP", "Python"]}
    result.update(data)

    return result


if __name__ == "__main__":
    plot_test_corpus()
    plot_python_mock_tools()
    plot_javascript_mock_tools()
    plot_php_mock_tools()
    plot_java_mock_tools()
    plot_mocks_por_linguagem()
    plot_dep_type()
    plot_mocktools_groups()
    plot_tools_languages()
