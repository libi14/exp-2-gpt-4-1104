from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)


# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Generate Blog
# -------------------------------
@app.route("/generate", methods=["POST"])
def generate_blog():

    data = request.get_json()

    # Get user inputs
    topic = data.get("topic", "")
    style = data.get("style", "Professional")
    tone = data.get("tone", "Friendly")
    word_count = data.get("word_count", 300)
    audience = data.get("audience", "Engineering Students")

    # -------------------------------
    # Validate Topic
    # -------------------------------
    if not topic.strip():
        return jsonify({
            "success": False,
            "error": "Please enter a blog topic."
        })


    # -------------------------------
    # Prompt Engineering
    # -------------------------------
    prompt = f"""
Write a blog about "{topic}".

Requirements:

- Writing Style: {style}
- Tone: {tone}
- Word Count: approximately {word_count} words
- Target Audience: {audience}

Structure the blog with:

1. Title
2. Introduction
3. Main Content
4. Conclusion

Use simple and clear English.
Make the blog informative, well structured and easy to understand.
"""


    try:

        # -------------------------------
        # Send Prompt to Ollama
        # -------------------------------
        response = ollama.chat(
            model="llama3.2:1b",

            # Reduce memory usage
            options={
                "num_ctx": 2048
            },

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        # -------------------------------
        # Get Generated Blog
        # -------------------------------
        blog = response["message"]["content"]


        # -------------------------------
        # Send Result to Website
        # -------------------------------
        return jsonify({
            "success": True,
            "blog": blog
        })


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


# -------------------------------
# Start Flask Application
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)