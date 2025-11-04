from flask import Flask, render_template, request, redirect
from database import add_user, create_database, query, update_user_password, get_data

app = Flask(__name__)
create_database()

session = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if (first_name and last_name) and password == confirm_password:
            add_user(first_name, last_name, username, email, password)
            return redirect("/login")
        else:
            return render_template("error.html", error_message="Registration failed. Please check your details and try again.")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Here you would normally verify the username and password
        sql_query = "SELECT * FROM users WHERE username = ? AND password = ?"
        results = query(sql_query, (username, password))
        if results:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", message="Invalid credentials.")
    return render_template("login.html")

@app.route("/error")
def error():
    return render_template("error.html", error_message="An error occurred.")

@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/login")
    return render_template("dashboard.html")


@app.route("/update_password", methods=["GET", "POST"])
def update_password():
    if request.method == "POST":
        username = request.form.get("username")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        print("Received password update request for user:", username)

        if new_password == confirm_password:
            print("Updating password for user:", username)
            update_user_password(username, new_password)
            return redirect("/")
        else:
            return render_template("error.html", error_message="Passwords do not match.")
    return render_template("dashboard.html")

@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql_query = "DELETE FROM users WHERE username = ? and password = ?"
        query(sql_query, (username, password))
        return redirect("/")
    return render_template("dashboard.html")



@app.route("/view_users")
def view_users():
    data = get_data()
    return render_template('table.html', users=data)

@app.route("/logout")
def logout():
    if session.get("user"):
        session.pop("user")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)