import subprocess
import json
import os

def analyze_contract_with_slither(file_path):
    """
    Analyze a Solidity contract using Slither.
    Args:
        file_path (str): Path to the Solidity (.sol) file.
    Returns:
        dict: Vulnerabilities detected by Slither, or None if an error occurs.
    """
    try:
        # Run Slither analysis
        result = subprocess.run(
            ["slither", file_path, "--json", "output.json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Check if output.json exists and is non-empty
        if os.path.exists("output.json") and os.path.getsize("output.json") > 0:
            with open("output.json", "r") as json_file:
                analysis_result = json.load(json_file)
                return analysis_result
        else:
            print("Error: Slither did not generate a valid output.json file.")
            return None

    # except subprocess.CalledProcessError as e:
    #     print(f"Error running Slither:{e.stderr}")
    #     return None
    # except json.JSONDecodeError as e:
    #     print("Error decoding JSON output:", e)
    #     return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# # Example usage
# analysis = analyze_contract_with_slither("../Contracts-Folder/VulnerableContract.sol")
# if analysis:
#     print("Detected Vulnerabilities:")
#     for vulnerability in analysis.get("results", {}).get("detectors", []):
#         print(vulnerability)
# else:
#     print("Analysis failed.")
