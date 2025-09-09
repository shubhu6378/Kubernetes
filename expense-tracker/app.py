from flask import Flask, request, render_template, redirect, jsonify
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "expense_db")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    total = sum(exp["amount"] for exp in expenses)
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        description = request.form["description"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (category, amount, description) VALUES (%s, %s, %s)",
                       (category, amount, description))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/")
    return render_template("add.html")

@app.route("/api/expenses", methods=["GET"])
def api_get_expenses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(expenses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

