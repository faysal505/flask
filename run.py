from flask import Flask, request, render_template, redirect, url_for, g, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2



app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mydata_839h_user:J56VGKBunMhYrRrPjdJxTrcnYD55bdDl@dpg-cgts3nt269vbmevj9tfg-a.oregon-postgres.render.com/mydata_839h"
db.init_app(app)
app.secret_key = '44441234'


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Integer, default=10)
    apikey = db.Column(db.String(1000), nullable=True)
    count = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Integer, nullable=False, default=0)


with app.app_context():
    db.create_all()




@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            return render_template("signup.html", email='<p class="text-center text-warning">This Email Already Exist</p>')
        else:
            userInfo = User(name=name, phone=phone, email=email, password=password)
            db.session.add(userInfo)
            db.session.commit()
            return render_template("signup.html", email='<p class="text-center text-success">Signup Success</p>')

    if request.method == "GET":
        return render_template("signup.html")

# @app.before_request

@app.route("/login", methods=["GET", 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        searchEmail = User.query.filter_by(email=email).first()
        if searchEmail is None:
            return render_template("login.html", message='<p class="text-center text-success">Email Not Registration</p>')
        else:
            if searchEmail.password == password:
                if searchEmail.active == 1:
                    session['user'] = email
                    return redirect(url_for("home"))
                else:
                    return render_template("login.html", message='<p class="text-center text-success">Account Not Active</p>')
            else:
                return render_template("login.html", message='<p class="text-center text-success">Password Not Match</p>')




@app.route("/home")
@app.route("/")
def home():
    if "user" in session:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
