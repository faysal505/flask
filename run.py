from flask import Flask, render_template, request
import myCode

app = Flask(__name__)

@app.route('/')
def manually():
    return render_template('home.html')


@app.route("/upload", methods=["POST", "GET"])
def sign():
    if request.method == "POST":
        file = request.files["sign"]
        if file.filename:
            file.save('static/' + file.filename)
        images = myCode.manually.sign_image('static/' + file.filename)
        text = myCode.manually.sign_text("static/" + file.filename)
        res = {**images, **text}
    return res



@app.route("/nid", methods=["POST", "GET"])
def nid():
    if request.method == "POST":
        photo = request.form['user']
        sign = request.form['sign']
        name = request.form['name']
        nameEn = request.form['nameEn']
        father = request.form['father']
        mother = request.form['mother']
        birth_like_nid = request.form['birth_like_nid']
        birth = request.form['birth']
        nid = request.form['nid']
        pin = request.form['pin']
        bloodGroup = request.form['bloodGroup']
        presentAddress = request.form['presentAddress']
        birthOfPlace = request.form['birthOfPlace']
        today_date = request.form['today_date']
        scanner = myCode.manually.scanner(pin, nameEn, birth)

        person = {
            "photo": photo,
            "sign": sign,
            "name": name,
            "nameEn": nameEn,
            "birth_like_nid": birth_like_nid,
            "nationalId": nid,
            "pin": scanner,
            "father": father,
            "mother": mother,
            "bloodGroup": bloodGroup,
            "pdf417": scanner,
            "fullDate": today_date,
            "presentAddress": presentAddress,
            "birthOfPlace": birthOfPlace
        }
        return render_template("nid.html", data=person)





if __name__ == "__main__":
    app.run(debug=True)


