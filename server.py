
from flask import Flask, request, jsonify, send_from_directory
from serpapi import GoogleSearch

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/ask")
def ask():
    query = request.args.get("q", "")
    if not query:
        return jsonify(error="No question provided"), 400

    search = GoogleSearch({
        "q": query,
        "api_key": "894807be90e816940e80a2259a46174f3dd1ff55ed27cab5bbc6665592fc0e82"
    })

    try:
        results = search.get_dict()
        answer = (
            results.get("answer_box", {}).get("answer")
            or results.get("answer_box", {}).get("snippet")
            or results.get("organic_results", [{}])[0].get("snippet", None)
        )
    except Exception as e:
        return jsonify(error=str(e)), 500

    if not answer:
        answer = "Hmm... I couldn’t find a solid answer, but I’m learning!"

    return jsonify(answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
