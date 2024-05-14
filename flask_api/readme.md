# Simple Chatbot using Transformer-based QA Model
This is a simple Flask web application that serves as a chatbot using a Transformer-based Question Answering (QA) model. Users can input a context and a question, and the chatbot will provide the answer based on the provided context.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repository
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app:

    ```bash
    python app.py
    ```

5. Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to interact with the chatbot.

## Usage

- On the homepage, input the context and question in the provided form.
- Click the "Ask" button.
- The chatbot will predict the answer based on the provided context and display it below the form.

## Files and Directories

- `app.py`: Flask application file containing the routes and API endpoints.
- `predict_model.py`: Python script containing the `predict_answer` function to predict answers using the Transformer-based QA model.
- `index.html`: HTML template for the homepage with the chatbot interface.
- `models/`: Directory containing the trained model files.

## Dependencies

- Flask
- Transformers
- Torch

## Acknowledgements

The model used in this project is based on the Hugging Face Transformers library. Special thanks to Hugging Face for providing pre-trained models and tools for natural language processing tasks.