import os
import sys

from transformers import RobertaTokenizer

# Initialize CodeBERT tokenizer
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")

def tokenize_smart_contract(file_path):
    """
    Tokenizes a Solidity smart contract for CodeBERT.
    Args:
        file_path (str): Path to the Solidity (.sol) file.
    Returns:
        dict: Tokenized code with tokens and attention mask.
    """
    with open(file_path, 'r') as file:
        code = file.read()

    # Tokenize the smart contract code
    tokens = tokenizer(code, return_tensors=None, padding="max_length", truncation=True, max_length=512)

    #Either return token or return token_dict for json formate.
    token_dict = tokens.data

    return token_dict

# # Example Usage
# contract_path = "../Contracts-Folder/VulnerableContract.sol"  # Replace with your Solidity file path
# tokens = tokenize_smart_contract(contract_path)
#
# print("Tokens:", tokens)
# print("Attention Mask:", tokens['attention_mask'])

