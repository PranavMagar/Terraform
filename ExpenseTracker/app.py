from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import pandas as pd
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'

USERS_FILE = "users.csv"
BASE_EXPENSE_DIR = "user_expenses"

# Ensure folders/files exist
os.makedirs(BASE_EXPENSE_DIR, exist_ok=True)
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

# -------------------- Helper Functions --------------------
def read_users():
    return pd.read_csv(USERS_FILE)

def write_users(df):
    df.to_csv(USERS_FILE, index=False)

def user_csv(username):
    return os.path.join(BASE_EXPENSE_DIR, f"{username}_expenses.csv")

def read_df(username):
    path = user_csv(username)
    if not os.path.exists(path):
        pd.DataFrame(columns=["Date", "Category", "Amount", "Description"]).to_csv(path, index=False)
    return pd.read_csv(path)

def write_df(username, df):
    df.to_csv(user_csv(username), index=False)

# -------------------- Authentication --------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("signup"))

        df = read_users()

        # Check if user exists
        if username in df["username"].values:
            flash("User already exists. Please log in.", "error")
            return redirect(url_for("login"))

        hashed_pw = generate_password_hash(password)
        new_user = pd.DataFrame([[username, hashed_pw]], columns=["username", "password"])
        df = pd.concat([df, new_user], ignore_index=True)
        write_users(df)

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        df = read_users()
        user = df[df["username"] == username]

        if user.empty:
            return render_template("login.html", error="❌ User not found")

        hashed = user.iloc[0]["password"]
        if not check_password_hash(hashed, password):
            return render_template("login.html", error="❌ Incorrect password")

        session["username"] = username
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------- Dashboard + Expense Logic --------------------
@app.route("/")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    df = read_df(username)

    total = df["Amount"].sum() if not df.empty else 0.0
    now = datetime.now()
    month_total = df[pd.to_datetime(df["Date"]).dt.month == now.month]["Amount"].sum() if not df.empty else 0.0
    avg_total = df["Amount"].mean() if not df.empty else 0.0
    categories = ["Food", "Transport", "Bills", "Shopping", "Other"]

    return render_template(
        "dashboard.html",
        total=round(total, 2),
        month_total=round(month_total, 2),
        avg_total=round(avg_total, 2),
        categories=categories,
        user_expenses=df.to_dict(orient="records"),
    )

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    categories = ["Food", "Transport", "Bills", "Shopping", "Other"]

    if request.method == "POST":
        date = request.form.get("date")
        category = request.form.get("category")
        amount = request.form.get("amount")
        description = request.form.get("description", "")

        if not date or not category or not amount:
            return "Date, Category and Amount are required", 400
        try:
            amount = float(amount)
        except:
            return "Amount must be numeric", 400

        df = read_df(username)
        new_row = pd.DataFrame([[date, category, amount, description]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        write_df(username, df)

        return redirect(url_for("dashboard"))

    return render_template("add.html", categories=categories)


@app.route("/reports")
def reports():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    df = read_df(username)
    if df.empty:
        summary, monthly = {}, {}
    else:
        summary = df.groupby("Category")["Amount"].sum().round(2).to_dict()
        monthly = df.groupby("Date")["Amount"].sum().sort_index().round(2).to_dict()

    return render_template("reports.html", summary=summary, monthly=monthly)

@app.route("/api/chart-data")
def chart_data():
    if "username" not in session:
        return jsonify({"pie": {}, "line": {}})

    username = session["username"]
    df = read_df(username)
    if df.empty:
        pie, line = {}, {}
    else:
        pie = df.groupby("Category")["Amount"].sum().round(2).to_dict()
        line = df.groupby("Date")["Amount"].sum().sort_index().round(2).to_dict()

    return jsonify({"pie": pie, "line": line})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

