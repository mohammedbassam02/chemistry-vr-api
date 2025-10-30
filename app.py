from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

# إنشاء تطبيق Flask
app = Flask(__name__)
CORS(app)

# مفتاح OpenAI (من متغيرات البيئة في Render)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Chemistry VR API"}), 200

# المسار الرئيسي لاستقبال الأسئلة
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "Please provide a question"}), 400

        # استدعاء نموذج OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful chemistry assistant."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
