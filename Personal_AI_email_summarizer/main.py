import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400
    try:
        completion = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[{"role": "user", "content": question}],
        )
        answer = completion.choices[0].message.content
        return jsonify({"response": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/summarise", methods=["POST"])
def summarise():
    email_text = request.form.get("email")
    if not email_text:
        return jsonify({"error": "No email provided"}), 400
    prompt = f"summarise the following email in 2-3 lines : {email_text}"

    try:
        completion = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        summary = completion.choices[0].message.content
        return jsonify({"summary": summary}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)


    