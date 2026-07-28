import json
import pandas as pd

from config.settings import OUTPUT_FOLDER


def save_json(data):

    path = f"{OUTPUT_FOLDER}/books.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("JSON file saved.")


def save_csv(data):

    path = f"{OUTPUT_FOLDER}/books.csv"

    df = pd.DataFrame(data)

    df.to_csv(path, index=False)

    print("CSV file saved.")
