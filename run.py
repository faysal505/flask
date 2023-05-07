from flask import Flask, request, render_template, redirect, url_for, g, session
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
import datetime


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
    rate = db.Column(db.Integer, default=10)
    apikey = db.Column(db.String(1000), nullable=True)
    count = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Integer, nullable=False, default=1)


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
        return render_template("home.html", email=session['user'])
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
        if len(f.filename) >= 1:
            f.save("static/" + f.filename)
        else:
            f.filename = "blank.png"
        getLoginToken = "https://idp-v2.live.mygov.bd/"
        s = requests.session()
        r_for_token = s.get(getLoginToken)
        html = BeautifulSoup(r_for_token.text, "html.parser")
        token = html.input["value"]

        form_data = {
            "_token": token,
            "mobile": "01303188962",
            "password": "Faysal=1234"
        }

        loginUrl = "https://idp-v2.live.mygov.bd/login"
        login = s.post(loginUrl, data=form_data)
        cookieStr = login.cookies.get("XSRF-TOKEN")
        X_Token = cookieStr.replace("%3D", "=")
        h = {
            "X-XSRF-TOKEN": X_Token,
            'Content-Type': 'application/json; charset=utf-8',
            "accept": "application/json, text/plain, */*",
            'content-type': "application/json"
        }

        js = {
            "dob": birth,
            "nid": nid
        }


        nidVerifyUrl = "https://idp-v2.live.mygov.bd/preview-nid"
        r_verify = s.post(nidVerifyUrl, json=js, headers=h)
        if r_verify.json()['data'] == None:
            return "NID INFORMATION NOT CURRECT"

        diccct = r_verify.json()
        photo = diccct['data']['photo']
        name = diccct['data']['name']
        nameEn = diccct['data']['nameEn']
        bloodGroup = diccct['data']['bloodGroup']
        dateOfBirth = diccct['data']['dateOfBirth']
        nationalId = diccct['data']['nationalId']
        pin = diccct['data']['pin']
        father = diccct['data']['father']
        mother = diccct['data']['mother']
        homeOrHoldingNo2 = diccct['data']['presentAddress']['homeOrHoldingNo']
        if "additionalVillageOrRoad" in diccct['data']['presentAddress']:
            village = diccct['data']['presentAddress']['additionalVillageOrRoad']

        if "villageOrRoad" in diccct['data']['presentAddress']:
            village = diccct['data']['presentAddress']['villageOrRoad']
        unionOrWard2 = diccct['data']['presentAddress']['unionOrWard']
        # upozila2 = diccct['data']['presentAddress']['upozila']
        postOffice2 = diccct['data']['presentAddress']['postOffice']
        postalCode2 = diccct['data']['presentAddress']['postalCode']
        if "cityCorporationOrMunicipality" in diccct['data']['presentAddress']:
            cityCorporationOrMunicipality2 = diccct['data']['presentAddress']['cityCorporationOrMunicipality']
            cityCorporationOrMunicipality2 += ", "
        else:
            cityCorporationOrMunicipality2 = ''
        upozila2 = diccct['data']['presentAddress']['upozila']
        district2 = diccct['data']['presentAddress']['district']

        def nidBirth(v):
            nidBirth = ""
            nidBirth += v[8:]
            if v[5:7] == "01":
                nidBirth += " Jan "
            if v[5:7] == "02":
                nidBirth += " Feb "
            if v[5:7] == "03":
                nidBirth += " Mar "
            if v[5:7] == "04":
                nidBirth += " Apr "
            if v[5:7] == "05":
                nidBirth += " May "
            if v[5:7] == "06":
                nidBirth += " Jun "
            if v[5:7] == "07":
                nidBirth += " Jul "
            if v[5:7] == "08":
                nidBirth += " Aug "
            if v[5:7] == "09":
                nidBirth += " Sept "
            if v[5:7] == "10":
                nidBirth += " Oct "
            if v[5:7] == "11":
                nidBirth += " Nov "
            if v[5:7] == "12":
                nidBirth += " Dec "
            nidBirth += v[0:4]
            return nidBirth

        nidDate = nidBirth(str(dateOfBirth))

        tody = datetime.datetime.now()
        date = str(tody.date())

        def EnNumToBn(s):
            bangla = ""
            for i in s:
                if i == "0":
                    bangla += "০"
                if i == "1":
                    bangla += "১"
                if i == "2":
                    bangla += "২"
                if i == "3":
                    bangla += "৩"
                if i == "4":
                    bangla += "৪"
                if i == "5":
                    bangla += "৫"
                if i == "6":
                    bangla += "৬"
                if i == "7":
                    bangla += "৭"
                if i == "8":
                    bangla += "৮"
                if i == "9":
                    bangla += "৯"
            return bangla

        ban_dd = EnNumToBn(date)[6:]
        ban_mmm = EnNumToBn(date)[4:6]
        ban_yyyy = EnNumToBn(date)[0:4]
        fullDate = f"{ban_dd}/{ban_mmm}/{ban_yyyy}"
        con = EnNumToBn(str(postalCode2))
        if con == "":
            postal_c = postalCode2
        else:
            postal_c = con

        perAdd = f"বাসা/হোল্ডিং: {homeOrHoldingNo2}, গ্রাম/রাস্তা: {village}, {unionOrWard2}, ডাকঘর: {postOffice2} - {postal_c}, {cityCorporationOrMunicipality2}{upozila2}, {district2}"

        form_data = {
            "data": f"<pin>{pin}</pin><name>{nameEn}</name><DOB>{nidDate}</DOB><FP></FP><F>Right+Index</F><TYPE>A</TYPE><V>2.0</V><ds>302c0214617d0b9f4d7527f6ed877d2ad65f45df2a67fdc1021437986f77b6316140f466f7784fceb6bb900381ef</ds>",
            "code": "PDF417",
            "multiplebarcodes": "true",
            "eclevel": "L",
            "dmsize": "Default",
            "base64": "true"
        }

        barcodeUrl = "https://barcode.tec-it.com/barcode.ashx"
        requestp = requests.post(barcodeUrl, data=form_data)
        pdf417 = requestp.text


        person = {
            "photo": photo,
            "name": name,
            "nameEn": nameEn,
            "bloodGroup": bloodGroup,
            "nidDate": nidDate,
            "nationalId": nationalId,
            "pin": pin,
            "father": father,
            "mother": mother,
            "homeOrHoldingNo2": homeOrHoldingNo2,
            "village": village,
            "unionOrWard2": unionOrWard2,
            "upozila2": upozila2,
            "postOffice2": postOffice2,
            "postalCode2": postalCode2,
            "cityCorporationOrMunicipality2": cityCorporationOrMunicipality2,
            "district2": district2,
            "perAdd": perAdd,
            "pdf417": pdf417,
            "fullDate": fullDate,
            "sign": f.filename

        }

        return render_template("nid.html", data=person, image=f)

    if request.method == "GET":
        return redirect(url_for("home"))




if __name__ == "__main__":
    app.run(debug=True)