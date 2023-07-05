import fitz
import base64
import re
import requests
from datetime import date


current_date = date.today().strftime("%d-%m-%Y")



class manually:

    @staticmethod
    def mess():
        print('hello')
        return "fuuu"

    @staticmethod
    def sign_text(pdf_path):
        doc = fitz.open(pdf_path)
        page = doc[0]
        text = page.get_text()
        nid = re.findall(r'\b\d{10}\b', text)[0]
        pin = re.findall(r'\b\d{17}\b', text)[0]
        birth = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', text)[0]
        birth_like_nid = manually.birth_like_nid(birth)
        today_date = manually.date_convert(current_date)
        print(birth_like_nid)
        sign_text = {"nid": nid, "pin": pin, "birth": birth, "birth_like_nid": birth_like_nid, 'today_date': today_date}
        return sign_text




    @staticmethod
    def sign_image(pdf_path):
        doc = fitz.open(pdf_path)
        first_page = doc[0]
        images_list = first_page.get_images()
        if len(images_list) == 2:
            images_dict = {}

            #get user image
            user_image = images_list[0]
            xref = user_image[0]
            image_info = doc.extract_image(xref)
            image_data = image_info["image"]
            base64_code = base64.b64encode(image_data).decode("utf-8")
            images_dict["user_image"] = "data:image/jpeg;base64, " + base64_code

            #get user signature if jpeg
            user_signature = images_list[1]
            xref1 = user_signature[0]
            image_info1 = doc.extract_image(xref1)
            if image_info1["ext"] == "jpeg":
                image_data1 = image_info1["image"]
                base64_code1 = base64.b64encode(image_data1).decode("utf-8")
                images_dict["user_signature"] = "data:image/jpeg;base64, " + base64_code1

            #get user signatur if png
            if image_info1["ext"] == "png":
                page = doc.load_page(0)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip= (612, 268, 729, 294))
                buffer = pix.tobytes("jpg")
                base64_image = base64.b64encode(buffer).decode('utf-8')
                images_dict["user_signature"] = "data:image/jpeg;base64, " + base64_image
        return images_dict


    @staticmethod
    def birth_like_nid(v):
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

    @staticmethod
    def date_convert(d):
        bangla = ''
        for i in d:
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
            if i == "-":
                bangla += "/"
        return bangla

    @staticmethod
    def scanner(pin, nameEn, birth):
        form_data = {
            "data": f"<pin>{pin}</pin><name>{nameEn}</name><DOB>{birth}</DOB><FP></FP><F>Right+Index</F><TYPE>A</TYPE><V>2.0</V><ds>302c0214617d0b9f4d7527f6ed877d2ad65f45df2a67fdc1021437986f77b6316140f466f7784fceb6bb900381ef</ds>",
            "code": "PDF417",
            "multiplebarcodes": "true",
            "eclevel": "L",
            "dmsize": "Default",
            "base64": "true"
        }

        barcodeUrl = "https://barcode.tec-it.com/barcode.ashx"
        requestp = requests.post(barcodeUrl, data=form_data)
        return requestp.text




# print(manually.mess())
# c = manually.sign_text('kh3.pdf')
# print(c)


