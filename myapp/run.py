from flask import Flask, render_template, request
import requests
import datetime
from bs4 import BeautifulSoup



app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/results', methods=["POST"])
def results():
    nid = request.form["nid"]
    birth = request.form["birth"]
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
    h = {"X-XSRF-TOKEN": X_Token}
    js = {
        "dob": birth,
        "nid": nid
    }

    nidVerifyUrl = "https://idp-v2.live.mygov.bd/preview-nid"
    r_verify = s.post(nidVerifyUrl, json=js, headers=h)
    if r_verify.json()['data'] == None:
        return "NID INFORMATION NOT CURRECT"
    return r_verify.json()


if __name__ == '__main__':
    app.run(debug=True)
