import re
from pyvis.network import Network
import networkx as nx


def parse_contract_to_graph(file_path):
    """
    Parses a Solidity smart contract into a graph representation.
    Args:
        file_path (str): Path to the Solidity file.
    Returns:
        nx.DiGraph: A graph representation of the smart contract.
    """
    with open(file_path, "r") as file:
        code = file.readlines()

    # Initialize graph
    graph = nx.DiGraph()

    # Regular expressions for detection
    function_pattern = re.compile(r"function\s+(\w+)\s*\(")  # Function names
    variable_pattern = re.compile(
        r"\b(?:uint|int|address|bool|string|bytes\d*|mapping|struct|enum)\b.*?\s+(\w+)\s*[;=]"
    )  # Variables
    mapping_pattern = re.compile(r"mapping\s*\(([^)]+)\)\s+(\w+);")  # Mappings
    modifier_pattern = re.compile(r"modifier\s+(\w+)\s*")  # Modifiers
    structure_pattern = re.compile(r"struct\s+(\w+)\s*{")  # Structures

    # Parse lines to find functions, variables, mappings, modifiers, and structures
    for line_number, line in enumerate(code, start=1):
        stripped_line = line.strip()

        # Detect function definitions
        func_match = function_pattern.search(stripped_line)
        if func_match:
            func_name = func_match.group(1)
            graph.add_node(func_name, type="function", line=line_number)
            continue

        # Detect mappings
        map_match = mapping_pattern.search(stripped_line)
        if map_match:
            map_name = map_match.group(2)
            graph.add_node(map_name, type="mapping", line=line_number)
            continue

        # Detect variable declarations
        var_match = variable_pattern.search(stripped_line)
        if var_match:
            var_name = var_match.group(1)
            graph.add_node(var_name, type="variable", line=line_number)
            continue

        # Detect modifiers
        mod_match = modifier_pattern.search(stripped_line)
        if mod_match:
            mod_name = mod_match.group(1)
            graph.add_node(mod_name, type="modifier", line=line_number)
            continue

        # Detect structures
        struct_match = structure_pattern.search(stripped_line)
        if struct_match:
            struct_name = struct_match.group(1)
            graph.add_node(struct_name, type="structure", line=line_number)

    # Add edges based on dependencies
    for node in graph.nodes(data=True):
        if node[1]["type"] == "function":
            for line_number, line in enumerate(code, start=1):
                stripped_line = line.strip()
                for target_node in graph.nodes(data=True):
                    if (
                        target_node[1]["type"] in ["variable", "mapping", "modifier"]
                        and target_node[0] in stripped_line
                    ):
                        graph.add_edge(node[0], target_node[0])

    return graph


def visualize_contract_graph(graph, output_file="contract_graph.html"):
    """
    Visualizes a smart contract graph using PyVis with separated node types.
    Args:
        graph (nx.DiGraph): Graph representation of the contract.
        output_file (str): Name of the HTML file for visualization.
    """
    net = Network(notebook=True, directed=True)

    # Define styles for each node type
    type_styles = {
        "function": {"color": "lightblue", "shape": "ellipse"},
        "variable": {"color": "lightgreen", "shape": "circle"},
        "mapping": {"color": "orange", "shape": "box"},
        "modifier": {"color": "red", "shape": "diamond"},
        "structure": {"color": "purple", "shape": "hexagon"},
    }

    # Add nodes with styles
    for node, data in graph.nodes(data=True):
        node_type = data.get("type", "unknown")
        style = type_styles.get(node_type, {"color": "gray", "shape": "ellipse"})
        net.add_node(
            node,
            label=f"{node_type.capitalize()}: {node}",
            color=style["color"],
            shape=style["shape"],
        )

    # Add edges
    for source, target in graph.edges:
        net.add_edge(source, target)

    # Show and save the graph
    net.show(output_file)


# Example Usage
contract_file_path = "../Contracts-Folder/Token.sol"
contract_graph = parse_contract_to_graph(contract_file_path)

# Print nodes with details
print("Graph Nodes:")
for node, data in contract_graph.nodes(data=True):
    print(f"{data['type'].capitalize()}: {node}, Line: {data['line']}")

# Print edges
print("\nGraph Edges:")
for source, target in contract_graph.edges:
    print(f"{source} -> {target}")

# Visualize the graph
visualize_contract_graph(contract_graph, "contract_graph.html")
