from flask import Flask, request, jsonify, render_template
from src.models.predict_model import predict_answer

app = Flask(__name__)

# Define the path to the trained model
MODEL_PATH = "models"
context = open("./data/processed/context.txt", "r").read()


# Home route
@app.route("/")
def home():
    return render_template("index.html")


# API endpoint for getting the chatbot response
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Predict the answer
    answer = predict_answer(MODEL_PATH, context, question)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
