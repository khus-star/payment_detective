from flask import Flask, jsonify, render_template, request
from investigator import PaymentDetective

app = Flask(__name__)

# Create our detective engine
detective = PaymentDetective()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/cases")
def cases():
    return jsonify(detective.cases())


@app.post("/api/investigate")
def investigate():
    body = request.get_json(silent=True) or {}

    case_id = body.get("case_id", "revenue_drop")

    result = detective.investigate(case_id)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)