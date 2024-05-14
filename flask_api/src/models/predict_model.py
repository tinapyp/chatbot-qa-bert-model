import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer


def predict_answer(model_path, context, question):
    """
    Predicts the answer to a given question based on a pre-trained model.

    Args:
        model_path (str): The path to the saved model.
        context (str): The context in which the question is asked.
        question (str): The question to be answered.

    Returns:
        str: The predicted answer to the question.

    Raises:
        None

    Description:
        This function loads a pre-trained model and tokenizer from the given model path.
        It then tokenizes the input question and context using the tokenizer.
        The tokenized inputs are passed to the loaded model for inference.
        The predicted start and end indices of the answer are obtained from the model's output.
        The token indices corresponding to the answer are extracted from the tokenized inputs.
        Finally, the token indices are converted to a text span, which represents the predicted answer.
    """

    # Load the saved model and tokenizer
    model = AutoModelForQuestionAnswering.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Tokenize the input
    inputs = tokenizer(
        question,
        context,
        padding="max_length",
        truncation="only_second",
        max_length=384,
        return_tensors="pt",
    )

    # Perform inference using the loaded model
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted start and end indices
    start_index = torch.argmax(outputs.start_logits, dim=-1).item()
    end_index = torch.argmax(outputs.end_logits, dim=-1).item()

    # Convert token indices to text span
    all_tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    answer_tokens = all_tokens[start_index : end_index + 1]
    answer = tokenizer.convert_tokens_to_string(answer_tokens)

    return answer


if __name__ == "__main__":
    # Example usage
    model_path = "models"
    context = "Pelaksanaan Ujian Mandiri dilaksanakan secara offline melalui Computer Based Test (CBT)."
    question = "Bagaimana pelaksanaan Ujian Mandiri dilakukan ?"

    # Predict answer
    predicted_answer = predict_answer(model_path, context, question)

    print("Predicted Answer:", predicted_answer)
