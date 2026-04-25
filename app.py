from flask import Flask, render_template, request, session, redirect, url_for
import json
import random
from pathlib import Path

app = Flask(__name__)
app.secret_key = "dev"

BASE_DIR = Path(__file__).parent


# -------------------------
# 📦 LOAD BY TOPIC
# -------------------------
def load_questions(topic):
    file_path = BASE_DIR / topic / "questions.json"

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------
# 🚀 START
# -------------------------
@app.route("/")
def start():
    return """
    <h2>Choose Topic</h2>
    <a href="/quiz/Python">Python</a><br>
    <a href="/quiz/HTML">HTML</a><br>
    <a href="/quiz/JavaScript">JavaScript</a><br>
    """


# -------------------------
# 🎮 QUIZ
# -------------------------
@app.route("/quiz/<topic>", methods=["GET", "POST"])
def quiz(topic):

    if "questions" not in session or session.get("topic") != topic:
        session["questions"] = random.sample(load_questions(topic), len(load_questions(topic)))
        session["index"] = 0
        session["score"] = 0
        session["topic"] = topic

    questions = session["questions"]
    i = session["index"]

    if i >= len(questions):
        return redirect(url_for("result"))

    q = questions[i]

    if request.method == "POST":
        user = request.form["answer"].lower()
        correct = [a.lower() for a in q["answer"]]

        if user in correct:
            session["score"] += 1

        session["index"] += 1
        return redirect(url_for("quiz", topic=topic))

    return render_template(
        "quiz.html",
        question=q["question"],
        number=i + 1,
        topic=topic
    )


# -------------------------
# 🏁 RESULT
# -------------------------
@app.route("/result")
def result():
    return render_template(
        "result.html",
        score=session["score"],
        total=len(session["questions"])
    )


if __name__ == "__main__":
    app.run(debug=True)