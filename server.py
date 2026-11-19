from functools import lru_cache

import requests
from flask import Flask, jsonify, render_template, request

from airtable_data import load_recycling_data
from ai_response import create_response

app = Flask(__name__)


@lru_cache(maxsize=1)
def get_records():
    """Load Airtable once per server process."""
    return load_recycling_data()


def find_matching_items(query, records):
    exact_matches = set()
    partial_matches = set()

    query = query.strip().casefold()
    search_words = query.replace("-", " ").split()

    for row in records:
        names = [row["item"]]

        for alias in row.get("aliases", "").split(";"):
            if alias.strip():
                names.append(alias.strip())

        for name in names:
            normalized_name = name.strip().casefold()

            if query == normalized_name:
                exact_matches.add(row["item"])

            name_words = normalized_name.replace("-", " ").split()

            if all(word in name_words for word in search_words):
                partial_matches.add(row["item"])

    return sorted(exact_matches or partial_matches)


def records_or_error():
    """Return records or a browser-safe error."""
    try:
        return get_records(), None
    except (
        requests.RequestException,
        RuntimeError,
        ValueError,
        KeyError
    ):
        return None, (
            jsonify({
                "error": "Recycling information is temporarily unavailable."
            }),
            503
        )


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Enter an item name."}), 400

    if len(query) > 150:
        return jsonify({"error": "Keep the item name under 150 characters."}), 400

    records, error = records_or_error()

    if error is not None:
        return error

    return jsonify({
        "matches": find_matching_items(query, records)
    })


@app.get("/api/conditions")
def conditions():
    item_name = request.args.get("item", "").strip()

    records, error = records_or_error()

    if error is not None:
        return error

    matches = []

    for record_number, row in enumerate(records):
        if row["item"] == item_name:
            matches.append({
                "id": record_number,
                "condition": row["condition"]
            })

    if not matches:
        return jsonify({"error": "That item was not found."}), 404

    return jsonify({"conditions": matches})


@app.post("/api/guidance")
def guidance():
    submitted = request.get_json(silent=True)

    if not isinstance(submitted, dict):
        return jsonify({"error": "Invalid request."}), 400

    record_number = submitted.get("id")

    records, error = records_or_error()

    if error is not None:
        return error

    if (
        type(record_number) is not int
        or not 0 <= record_number < len(records)
    ):
        return jsonify({"error": "Select a valid condition."}), 400

    # Retrieve the actual stored record, not instructions from the browser.
    selected = records[record_number]

    try:
        explanation = create_response(selected)
        ai_available = True
    except (requests.RequestException, RuntimeError, ValueError):
        explanation = (
            "The AI explanation is unavailable. "
            "Use the stored instructions shown above."
        )
        ai_available = False

    return jsonify({
        "item": selected["item"],
        "condition": selected["condition"],
        "category": selected["category"],
        "instruction": selected["instruction"],
        "source": selected["source"],
        "explanation": explanation,
        "ai_available": ai_available
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)