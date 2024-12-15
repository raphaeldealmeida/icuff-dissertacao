from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.preprocessing import MultiLabelBinarizer

GRAPHCS_PATH = "../graphics/"


def clean_transactions(data):
    """
    This function takes a list of lists (transactions) and removes any empty lists.

    Parameters:
    data (list): List of transactions, where each transaction is a list of tools.

    Returns:
    cleaned_data (list): List of transactions without empty lists.
    """
    return [transaction for transaction in data if transaction]


def extract_combinations(data):
    # Extract only the combinations of two tools from the list of projects
    combinations_of_two = [
        list(combinations(project, 2)) for project in data if len(project) > 1
    ]

    # Flatten the list of lists
    combinations_of_two_flat = [
        combo for sublist in combinations_of_two for combo in sublist
    ]
    return combinations_of_two_flat


# Function to process the data and calculate co-occurrence matrix
def process_cooccurrence_data(data):
    # Extract only the combinations of two tools from the list of projects
    combinations_of_two = [
        list(combinations(project, 2)) for project in data if len(project) > 1
    ]

    # Flatten the list of lists
    combinations_of_two_flat = [
        combo for sublist in combinations_of_two for combo in sublist
    ]

    # Create a DataFrame from the combinations
    combination_df = pd.DataFrame(
        combinations_of_two_flat, columns=["Tool 1", "Tool 2"]
    )
    # Create a crosstab (co-occurrence matrix) based on the number of times each pair appears
    cooccurrence_matrix_pairs = pd.crosstab(
        combination_df["Tool 1"], combination_df["Tool 2"]
    )

    # Adding symmetrical entries to ensure a complete matrix for the heatmap
    cooccurrence_matrix_full = cooccurrence_matrix_pairs.add(
        cooccurrence_matrix_pairs.T, fill_value=0
    )

    return cooccurrence_matrix_full


# Function to plot the heatmap with custom colormap and ordered by usage
def plot_cooccurrence_heatmap(cooccurrence_matrix_full, lang):
    # Create a mask for the upper triangle
    mask = np.triu(np.ones_like(cooccurrence_matrix_full, dtype=bool))

    # Use the 'viridis' colormap
    cmap = sns.color_palette("viridis", as_cmap=True)

    # Reorder the co-occurrence matrix based on the total appearance of the tools
    tool_sums = cooccurrence_matrix_full.sum(axis=1).sort_values(ascending=False)
    cooccurrence_df_sorted_top = cooccurrence_matrix_full.loc[
        tool_sums.index, tool_sums.index
    ]

    # Generate the heatmap with the reordered tools based on usage, using the 'viridis' colormap
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        cooccurrence_df_sorted_top, cmap=cmap, annot=True, cbar=True, fmt="g", mask=mask
    )
    # plt.title("Heatmap of Pairwise Tool Co-occurrence (Viridis - Most Used Tools at Top)")
    plt.xlabel("Ferramentas")
    plt.ylabel("Ferramentas")
    # plt.show()  # show on jupter notebook
    plt.savefig(f"{GRAPHCS_PATH}apriori.{lang}.png")


def plot_heatmap(data, lang):
    data = clean_transactions(data)
    # Process the data
    cooccurrence_matrix = process_cooccurrence_data(data)
    # Plot the heatmap
    plot_cooccurrence_heatmap(cooccurrence_matrix, lang)


def extract_frequences_and_display(data, lang, min_support=0.1):
    data = clean_transactions(data)
    # Convert data to a one-hot encoded format for the apriori algorithm
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Apply the Apriori algorithm
    frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)

    # Generate association rules with minimum confidence of 0.6
    rules_java = association_rules(
        frequent_itemsets, metric="confidence", min_threshold=0.4, num_itemsets=len(df)
    )

    # Show the first few association rules
    # rules_java.head()

    rules_java = rules_java[
        [
            "antecedents",
            "consequents",
            "antecedent support",
            "consequent support",
            "support",
            "confidence",
            "lift",
        ]
    ]
    rules_java["antecedents"] = rules_java["antecedents"].apply(lambda x: list(x))
    rules_java["consequents"] = rules_java["consequents"].apply(lambda x: list(x))
    rules_java = rules_java.round(
        {
            "antecedent support": 3,
            "consequent support": 3,
            "support": 3,
            "confidence": 3,
            "lift": 3,
        }
    )

    rules_java = rules_java[rules_java["support"] > min_support]
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        # print(rules_java)
        _save_csv(rules_java, lang)


def _get_data(lang):
    DATASET_PATH_TEST_PROJECTS = f"../dataset/{lang}_projects_tests_tools2.csv"

    # Variável para armazenar os dados
    data = []

    # Leitura do arquivo CSV
    try:
        with open(DATASET_PATH_TEST_PROJECTS, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Converte a string da coluna 'test_tools' para uma lista real
                test_tools = eval(row["test_tools"])
                data.append(test_tools)
    except FileNotFoundError:
        data = "Arquivo não encontrado."

    return data


def _save_csv(rules, lang):
    association_rules_path = f"../dataset/associate_rules_{lang}.csv"
    # import pprint

    # pprint.pp(rules)

    with open(
        association_rules_path, mode="a", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)
        if csv_file.tell() == 0:
            writer.writerow(
                [
                    "antecedents",
                    "consequents",
                    "antecedent suppor",
                    "consequent support",
                    "support",
                    "confidence",
                    "lift",
                ]
            )
        for _, rule in rules.iterrows():
            writer.writerow(
                [
                    rule["antecedents"],
                    rule["consequents"],
                    rule["antecedent support"],
                    rule["consequent support"],
                    rule["support"],
                    rule["confidence"],
                    rule["lift"],
                ]
            )


def run(lang):
    data = _get_data(lang)
    extract_frequences_and_display(data, lang, 0.1)
    plot_heatmap(data, lang)


if __name__ == "__main__":
    # run("Python")
    # run("PHP")
    run("Java")
    # run("JavaScript")
