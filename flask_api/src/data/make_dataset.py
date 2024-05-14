import pandas as pd
import json


def transform_to_json(file_path: str, save_file_path: str) -> list[dict]:
    df = pd.read_csv(file_path)

    data_json = []
    for _, row in df.iterrows():
        data = {
            "context": row["context"],
            "question": row["question"],
            "answer": row["answer"],
        }
        data_json.append(data)

    with open(save_file_path, "w") as f:
        json.dump(data_json, f)

    return data_json
