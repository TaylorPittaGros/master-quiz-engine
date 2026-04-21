import json
import random
import datetime
from pathlib import Path

# -------------------------
# 📁 BASE DIRECTORY
# -------------------------
BASE_DIR = Path(__file__).parent

# -------------------------
# 📦 LOAD QUESTIONS
# -------------------------
def load_questions(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON error: {e}")
        return []

# -------------------------
# 📁 GET TOPIC PATH
# -------------------------
def get_topic_path(topic):
    return BASE_DIR / topic / "questions.json"

# -------------------------
# 🎯 FILTER QUESTIONS
# -------------------------
def filter_questions(questions, difficulty):
    if difficulty == "all":
        return questions
    return [q for q in questions if q.get("difficulty", "").lower() == difficulty]

# -------------------------
# 🎲 SELECT QUESTIONS
# -------------------------
def select_questions(questions, amount):
    return random.sample(questions, min(amount, len(questions)))

# -------------------------
# 🎮 NORMAL QUIZ
# -------------------------
def run_quiz(questions):
    score = 0
    wrong = []
    weak_topics = {}

    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['question']}")
        user = input("Your answer: ").strip().lower()

        answers = [a.lower() for a in q.get("answer", [])]

        if user in answers:
            print("✅ Correct")
            score += 1
        else:
            print(f"❌ Wrong (Correct: {', '.join(q['answer'])})")
            wrong.append(q)

            topic = q.get("topic", "unknown")
            weak_topics[topic] = weak_topics.get(topic, 0) + 1

    return score, wrong, weak_topics

# -------------------------
# 🎯 MCQ QUIZ
# -------------------------
def run_mcq(questions):
    if len(questions) < 2:
        return run_quiz(questions)

    score = 0
    wrong = []
    weak_topics = {}

    for i, q in enumerate(questions, 1):
        correct = q["answer"][0]

        pool = set()
        for item in questions:
            if item != q:
                for ans in item.get("answer", []):
                    pool.add(ans.lower())

        pool.discard(correct.lower())
        distractors = random.sample(list(pool), min(3, len(pool)))

        options = [correct] + distractors
        random.shuffle(options)

        print(f"\nQ{i}: {q['question']}")
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")

        try:
            choice = int(input("Choose: "))
            user_answer = options[choice - 1]
        except:
            print("❌ Invalid input")
            wrong.append(q)
            continue

        if user_answer.lower() == correct.lower():
            print("✅ Correct")
            score += 1
        else:
            print(f"❌ Wrong (Correct: {correct})")
            wrong.append(q)

            topic = q.get("topic", "unknown")
            weak_topics[topic] = weak_topics.get(topic, 0) + 1

    return score, wrong, weak_topics

# -------------------------
# 📄 SAVE REPORT
# -------------------------
def save_report(score, total, topic):
    folder = BASE_DIR / "reports"
    folder.mkdir(exist_ok=True)

    file_name = folder / "results.txt"

    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {topic} | {score}/{total}\n")

# -------------------------
# 📊 SAVE PROGRESS
# -------------------------
def save_progress(topic, score, total):
    file = BASE_DIR / "progress.json"

    data = {"sessions": []}
    if file.exists():
        with open(file, "r") as f:
            data = json.load(f)

    data["sessions"].append({
        "date": str(datetime.datetime.now()),
        "topic": topic,
        "score": score,
        "total": total
    })

    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# 📊 SHOW PROGRESS
# -------------------------
def show_progress():
    file = BASE_DIR / "progress.json"

    if not file.exists():
        print("No progress yet")
        return

    with open(file, "r") as f:
        data = json.load(f)

    print("\n📊 Last sessions:")
    for s in data["sessions"][-5:]:
        print(s)

# -------------------------
# 🚀 MAIN
# -------------------------
def main():
    print("🎮 QUIZ ENGINE")

    topics = [d.name for d in BASE_DIR.iterdir() if d.is_dir()]
    print("Topics:", topics)

    while True:
        topic = input("Choose topic: ")
        if topic in topics:
            break
        print("Invalid topic")

    difficulty = input("Difficulty (easy/medium/hard/all): ").lower()

    while True:
        try:
            size = int(input("Size (10/25/50/100): "))
            if size in [10, 25, 50, 100]:
                break
        except:
            pass
        print("Invalid size")

    mode = input("Mode (1=normal,2=mcq): ")

    questions = load_questions(get_topic_path(topic))
    filtered = filter_questions(questions, difficulty)
    test = select_questions(filtered, size)

    if mode == "2":
        score, wrong, weak = run_mcq(test)
    else:
        score, wrong, weak = run_quiz(test)

    total = len(test)

    print(f"\nScore: {score}/{total}")

    save_report(score, total, topic)
    save_progress(topic, score, total)
    show_progress()

if __name__ == "__main__":
    main()