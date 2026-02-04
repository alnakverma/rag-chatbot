# IMPORTS

from flask import Flask, request, jsonify

# import our modules
from intent import classify_intent
from rag import generate_answer


# CREATE FLASK APP

app = Flask(__name__)


# HOME ROUTE (for testing server)
# open: http://127.0.0.1:5000

@app.route("/")
def home():
    return "✅ RAG Chatbot backend running!"


# MAIN CHAT API

@app.route("/chat", methods=["POST"])
def chat():

    # 1. Read JSON from frontend
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Missing query"}), 400

    query = data["query"]

    print("\n==============================")
    print("User Query:", query)


    # 2. Intent Classification
    intent = classify_intent(query)

    print("User Query:", query)
    print("Predicted Intent:", intent)


    # 3. Intent Routing Logic

    if intent == "HR_POLICY":

        # call RAG only for HR questions
        answer = generate_answer(query)

    elif intent == "GREETING":

        answer = "Hello 👋 How can I help you with HR policies today?"

    elif intent == "GENERAL_CHAT":

        answer = "I only answer HR policy related questions."

    else:

        answer = "Sorry, I cannot answer that."


    print("Final Answer:", answer)
    print("==============================\n")


    # 4. Return response to frontend
    return jsonify({
        "query": query,
        "intent": intent,
        "answer": answer
    })


# RUN SERVER

if __name__ == "__main__":

    # debug=True → auto reload + error logs
    # port=5000 → default API port

    app.run(debug=True, port=5000)




# To run backend
# source venv/bin/activate
# cd backend
# python3 app.py

# To run frontend
# source venv/bin/activate
# cd frontend
# streamlit run ui.py