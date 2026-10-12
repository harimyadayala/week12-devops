
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("registration.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    student_id = request.form.get("student_id", "").strip()
    email = request.form.get("email", "").strip()
    year = request.form.get("year", "").strip()

    if not all([name, student_id, email, year]):
        return "All fields are required.", 400

    return render_template(
        "Successful.html",
        name=name,
        student_id=student_id,
        email=email,
        year=year
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
