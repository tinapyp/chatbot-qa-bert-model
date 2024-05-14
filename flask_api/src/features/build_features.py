import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer
import json
import os


def preprocess_and_save_dataset(
    input_file,
    output_dir,
    tokenizer_name="Wikidepia/indobert-lite-squad",
    max_length=384,
):
    """
    Preprocesses the input data, adjusts answer positions, tokenizes questions and context,
    finds start and end token positions, creates a DataFrame, and saves the processed dataset.

    Parameters:
    - input_file (str): Path to the input JSON file.
    - output_dir (str): Directory to save the processed data.
    - tokenizer_name (str, optional): Name of the tokenizer to use
      (default is "Wikidepia/indobert-lite-squad").
    - max_length (int, optional): Maximum length of the tokenized sequences
      (default is 384).

    Returns:
    - Dataset: Processed dataset in the form of a Dataset object.

    Example:
    ```
    from preprocess_data import preprocess_and_save_dataset

    # Define paths and parameters
    input_file_path = "/path/to/input/data.json"
    output_directory = "/path/to/output_directory"
    tokenizer_name = "wikidepia/indobert-lite-squad"
    max_length = 384

    # Preprocess and save the dataset
    train_dataset = preprocess_and_save_dataset(input_file_path, output_directory,
                                                tokenizer_name, max_length)
    ```
    """

    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    # Read the input JSON file
    df = pd.read_json(input_file)

    # Preprocess the data
    df["question"] = df["question"].str.lower()
    df["context"] = df["context"].str.lower()
    df["answer"] = df["answer"].str.lower()
    df["answer_start"] = df.apply(
        lambda row: row["context"].find(row["answer"]), axis=1
    )

    # Manually adjust answer_start for specific rows if needed
    df.at[2, "answer_start"] = 0
    df.at[3, "answer_start"] = 10
    df.at[12, "answer_start"] = 0
    df.at[19, "answer_start"] = 0
    df.at[29, "answer_start"] = 0
    df.at[31, "answer_start"] = 4

    df["answer"] = df["answer"].apply(
        lambda x: json.dumps({"text": [x], "answer_start": int(df["answer_start"][0])})
    )

    questions = [q.strip() for q in df["question"]]
    context = [q.strip() for q in df["context"]]
    inputs = tokenizer(
        questions,
        context,
        max_length=max_length,
        truncation="only_second",
        return_offsets_mapping=True,
        padding="max_length",
    )

    offset_mapping = inputs.pop("offset_mapping")

    start_positions = []
    end_positions = []
    answers = df["answer"].apply(lambda x: json.loads(x))
    for i, offset in enumerate(offset_mapping):
        answer = answers[i]
        start_char = int(answer["answer_start"])
        end_char = start_char + len(answer["text"][0])
        sequence_ids = inputs.sequence_ids(i)

        # Find the start and end of the context
        idx = 0
        while sequence_ids[idx] != 1:
            idx += 1
        context_start = idx
        while sequence_ids[idx] == 1:
            idx += 1
        context_end = idx - 1

        # If the answer is not fully inside the context, label it (0, 0)
        if offset[context_start][0] > end_char or offset[context_end][1] < start_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
            # Otherwise it's the start and end token positions
            idx = context_start
            while idx <= context_end and offset[idx][0] <= start_char:
                idx += 1
            start_positions.append(idx - 1)

            idx = context_end
            while idx >= context_start and offset[idx][1] >= end_char:
                idx -= 1
            end_positions.append(idx + 1)

    df["start_positions"] = start_positions
    df["end_positions"] = end_positions

    # Create DataFrame
    data = {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "start_positions": start_positions,
        "end_positions": end_positions,
        "answer": answers,
    }
    processed_df = pd.DataFrame(data)

    # Save the processed dataset
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "processed_data.csv")
    processed_df.to_csv(output_file, index=False)

    return Dataset.from_pandas(processed_df)
