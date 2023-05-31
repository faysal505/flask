from flask import Flask, request, render_template, redirect, url_for, g, session, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
import datetime
from myFun import *
import fitz
import base64
import re


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
    balance = db.Column(db.Integer, default=0)
    rate = db.Column(db.Integer, default=5)
    apikey = db.Column(db.String(1000), nullable=True)
    count = db.Column(db.Integer, default=0)
    active = db.Column(db.Integer, nullable=False, default=0)


with app.app_context():
    db.create_all()


class Nid(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    nid = db.Column(db.String(50), nullable=False)
    birth = db.Column(db.String(50), nullable=False)



with app.app_context():
    db.create_all()









@app.route("/active/<email>/<num>", methods=["GET"])
def active(email, num):
    admin = User.query.filter_by(email=email).first()
    admin.active = num
    db.session.commit()
    return f'{admin.email} = {admin.active}'


@app.route("/balance/<email>/<num>", methods=["GET"])
def balance(email, num):
    admin = User.query.filter_by(email=email).first()
    admin.balance = num
    db.session.commit()
    return f'{admin.email} = {admin.balance}'

@app.route("/persion/<email>")
def persion(email):
    admin = User.query.filter_by(email=email).first()
    return f'{admin.name} | {admin.email} | {admin.password} | {admin.balance} | {admin.active} | {admin.count}'


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
                    return render_template("login.html", message='<p class="text-center text-success">Admin Not Active Your Account</p>')
            else:
                return render_template("login.html", message='<p class="text-center text-success">Password Not Match</p>')




@app.route("/home")
@app.route("/")
def home():
    if "user" in session:
        email = session['user']
        user = User.query.filter_by(email=email).first()
        return render_template("home.html", email=session['user'], balance=user.balance, rate=user.rate)
    else:
        return redirect(url_for("login"))










@app.route('/results', methods=["POST", "GET"])
def results():
    email = session['user']
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        nid = request.form["nid"]
        birth = request.form["birth"]
        f = request.files["file"]
        if f.filename:
            f.save('static/' + f.filename)
            persion = fileTOBase64('static/' + f.filename)
            if len(persion) == 3:
                print('here 3')
                nid = persion['nid']
                birth = persion['birth']
                source = f'data: image/jpg; base64, {persion["signature"]}'
            elif len(persion) == 1:
                print('here 1')
                source = f'data: image/jpg; base64, {persion["signature"]}'
        else:
            source = ''

        email = session["user"]
        admin = User.query.filter_by(email=email).first()
        admin.count += 1
        db.session.commit()





        print(nid, birth)
        person = nidInfo(nid, birth)
        print(person)

        if person:
            name1 = person['nameEn']
            nid1 = person["nationalId"]
            birth1 = person["nidDate"]
            nidAdd = Nid(name=name1, nid=nid1, birth=birth1)
            db.session.add(nidAdd)
            db.session.commit()
        else:
            return "False Information"


        if admin.rate <= admin.balance:
            admin.balance = admin.balance - admin.rate
            db.session.commit()
            print(source)
            render = render_template("nid.html", data=person, image=source)
            htmlToPdf(render, person['nameEn'])
            return send_from_directory('static', person['nameEn'] + '.pdf', as_attachment=True)
            # return render
        else:
            return render_template("home.html", balance=admin.balance, rate=admin.rate, alert='<script>alert("Not Enough Balance")</script>')

    if request.method == "GET":
        return redirect(url_for("home", balance=user.balance))




if __name__ == "__main__":
    app.run(debug=True)
