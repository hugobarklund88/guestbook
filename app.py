from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "guestbook.json"


def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_entries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    entries = load_entries()
    entries.reverse()  # visa senaste inlägget överst
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    comment = request.form.get("comment")

    entry = {
        "name": name,
        "comment": comment,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    entries = load_entries()
    entries.append(entry)
    save_entries(entries)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)