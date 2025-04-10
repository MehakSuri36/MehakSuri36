from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

API_KEY = "AIzaSyBsxBA5X8jwB49wfNj7nmUiEh2vi7NPDBg"
MODEL = "gemini-1.5-pro-002"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    input_text = data.get("text", "")
    from_lang = data.get("from", "English")
    to_lang = data.get("to", "French")

    if not input_text:
        return jsonify({"error": "Missing text"}), 400

    prompt = f"Translate this text from {from_lang} to {to_lang}. Respond with only the translated sentence, no explanation:\n\n{input_text}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))

    print("Gemini status:", response.status_code)
    print("Gemini raw response:", response.text)

    if response.status_code != 200:
        return jsonify({"error": "Gemini API Error", "details": response.text}), 500

    try:
        data = response.json()
        reply = data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"translation": reply.strip()})
    except Exception as e:
        return jsonify({"error": "Unexpected response format", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
