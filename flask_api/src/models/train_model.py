import pandas as pd
from transformers import (
    AutoModelForQuestionAnswering,
    TrainingArguments,
    Trainer,
    AutoTokenizer,
)
from datasets import Dataset, load_metric
from sklearn.model_selection import train_test_split
import os


def train_model(
    df,
    output_dir="./models/train_output",
    model_name="Wikidepia/indobert-lite-squad",
    num_train_epochs=3,
):
    """
    Trains a question answering model using the given dataset.

    Args:
        df (pandas.DataFrame): The dataset to train the model on.
        output_dir (str, optional): The directory to save the trained model and logs. Defaults to './models/train_output'.
        model_name (str, optional): The name of the pre-trained model to use. Defaults to 'Wikidepia/indobert-lite-squad'.
        num_train_epochs (int, optional): The number of training epochs. Defaults to 3.

    Returns:
        None

    Raises:
        None

    Description:
        This function trains a question answering model using the given dataset. It defines the model architecture,
        sets the training arguments, splits the dataset into training and evaluation sets, creates Datasets from
        DataFrames, instantiates the Trainer, trains the model, evaluates the model, and saves the trained model
        and tokenizer.

        The function takes a pandas DataFrame `df` as input, which represents the dataset to train the model on.
        The `output_dir` parameter specifies the directory to save the trained model and logs. The `model_name`
        parameter specifies the name of the pre-trained model to use. The `num_train_epochs` parameter specifies
        the number of training epochs.

        The function does not return any value.

        Example usage:
        ```
        train_model(df, output_dir='./models/train_output', model_name='Wikidepia/indobert-lite-squad', num_train_epochs=3)
        ```
    """

    # Define the model
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    # Define the training arguments with early stopping
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=num_train_epochs,
        weight_decay=0.01,
        save_total_limit=1,
        logging_dir="./logs",
        logging_steps=10,
    )

    # Split the dataset into training and evaluation sets
    train_df, eval_df = train_test_split(df, test_size=0.2, random_state=42)

    # Create Datasets from DataFrames
    train_dataset = Dataset.from_pandas(train_df)
    eval_dataset = Dataset.from_pandas(eval_df)

    # Instantiate Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )

    # Train the model
    trainer.train()

    # Evaluate the model
    eval_results = trainer.evaluate()

    print("Evaluation results:", eval_results)

    # Save model and tokenizer
    model_path = "models"
    model.save_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(model_path)


if __name__ == "__main__":
    # Load your data from file
    df = pd.read_csv("data/processed_data/processed_data.csv")

    # Train the model
    train_model(df)
