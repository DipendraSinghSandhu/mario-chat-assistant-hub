from flask import Flask, render_template, request, jsonify
from ai_utils import get_best_response

app = Flask(__name__, static_folder="static", template_folder="templates")
ROADMAP_PROMPT = """
You are an expert coach.
When creating study roadmaps:
- Keep output short, deep, and scannable.
- Use stages (Beginner → Intermediate → Advanced).
- For each stage: 3–6 bullet points, 1 resource, 1 mini-project.
- Use emojis + Markdown headings.
- dont use gemini emojis
- Avoid paragraphs, explanations, or long text.
"""

SUGGESTION_PROMPT = """
You are a friendly, practical suggestion assistant. When given a user's situation or question, provide clear, actionable suggestions:
- Summarize the user's need
- Offer 3-6 concrete suggestions or options
- Give a recommended next step and short reasoning
- If relevant, provide resources or short examples
Format the reply as numbered suggestions and keep it concise but helpful.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/roadmap', methods=['GET'])
def roadmap_page():
    return render_template('roadmap.html')

@app.route('/suggestion', methods=['GET'])
def suggestion_page():
    return render_template('suggestion.html')
    

# Roadmap API
@app.route('/api/roadmap', methods=['POST'])
def roadmap_api():
    data = request.get_json(force=True)
    user_input = data.get('message', '')
    history = [{"role": "user", "parts": [{"text": ROADMAP_PROMPT}]}]
    reply = get_best_response(history, user_input)
    return jsonify({"reply": reply})

# Suggestion API

@app.route('/api/suggestion', methods=['POST'])
def suggestion_api():
    data = request.get_json(force=True)
    user_input = data.get('message', '')
    history = [{"role": "user", "parts": [{"text": SUGGESTION_PROMPT}]}]
    reply = get_best_response(history, user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
