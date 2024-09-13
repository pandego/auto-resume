import json
from fileinput import filename
from typing import Dict
import os
from rich import print as rprint
from datetime import datetime

# ------------------------ #
# --- Helper Functions --- #
# ------------------------ #


def load_data_from_json(file_path: str) -> Dict:
    with open(file_path, "r") as f:
        return json.load(f)


def load_file_from_txt(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def save_to_json(
    data: Dict,
    output_folder: str,
    file_type: str = "Tailored Resume",
) -> None:
    """
    Save data to a JSON file.

    Parameters
    ----------
    data : Dict
        The data to save to the JSON file.
    output_folder : str
        The path to the output directory.
    file_type : str, optional
        The type of file to save, by default "structured job description".

    Returns
    -------
    None
        This function doesn't return anything.

    """
    time_now = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename: str = ""
    if file_type == "Structured Resume":
        filename = f"{time_now}_{data['contact_info']['name'].replace(' ', '_')}.json"
    elif file_type == "Structured Job Description":
        filename = f"{time_now}_{data['Title'].replace(' ', '_')}_{data['Company'].replace(' ', '_')}.json"
    elif file_type == "Tailored Resume":
        filename = f"{time_now}_{data['contact_info']['name'].replace(' ', '_')}_{data['company_applying'].replace(' ', '_')}_tailored_resume.json"

    full_path = os.path.join(output_folder, filename)

    os.makedirs(output_folder, exist_ok=True)  # Ensure the output directory exists

    with open(full_path, "w") as f:
        json.dump(data, f)

    rprint(f"'{file_type} JSON' saved to:\n   -> [bold green]{full_path}[/bold green]")
