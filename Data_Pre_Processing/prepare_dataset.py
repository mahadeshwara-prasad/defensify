import os
import json

from tokenization import tokenize_smart_contract
from graph_creation import parse_contract_to_graph
from label_smart_contract import analyze_contract_with_slither

def prepare_dataset(folder_path):
    """
    Prepares a dataset from Solidity smart contracts.
    Args:
        folder_path (str): Path to the folder containing Solidity files.
    Returns:
        list: Dataset with tokenized code, vulnerability annotations, and graph representations.
    """
    dataset = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".sol"):
            file_path = os.path.join(folder_path, file_name)

            # Tokenize code
            tokens = tokenize_smart_contract(file_path)

            # Analyze for vulnerabilities
            analysis = analyze_contract_with_slither(file_path)

            # Parse to graph
            contract_graph = parse_contract_to_graph(file_path)

            # Add to dataset
            dataset.append({
                "file_name": file_name,
                "tokens": tokens,
                "analysis": analysis,
                "graph": contract_graph
            })

    # Save dataset to JSON
    with open("dataset.json", "w") as json_file:
        json.dump(dataset, json_file)

    return dataset


# Example Usage
dataset = prepare_dataset("../Contracts-Folder")
print("Dataset prepared:", len(dataset), "contracts processed.")
