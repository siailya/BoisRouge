from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from news_form import NewsForm
from bson.objectid import ObjectId
import datetime
import hashlib
import os

BLOCK_SIZE = 65536
UPLOAD_FOLDER = "news_photo"

app = Flask(__name__, static_folder="static")
client = MongoClient("mongodb+srv://Bois:Rouge@boisrouge.aephg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db_name = "DataBase"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "86F27F78E9AA221425B98B46F337A"
db = MongoEngine(app)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("admin.html")


@app.route('/add_new', methods=["GET", "POST"])
def add_new():
    news_form = NewsForm()
    if request.method == "POST":
        photo_hash = ""
        photo = request.files["pictures"]
        if photo:
            files = os.listdir("static/news_photo")
            photo_num = 1
            while True:
                if f"{photo_num}.png" not in files and f"{photo_num}.jpg" not in files:
                    photo_name = str(photo_num) + photo.filename[-4:]
                    outpath_file = os.path.join(os.path.join(os.getcwd(), "static/news_photo"), photo_name)
                    photo.save(outpath_file)

                    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
                    with open(outpath_file, "rb") as f:  # Open the file to read it's bytes
                        fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
                        while len(fb) > 0:  # While there is still data being read from the file
                            file_hash.update(fb)  # Update the hash
                            fb = f.read(BLOCK_SIZE)  # Read the next block from the file

                    photo_hash = file_hash.hexdigest()
                    photos = client[db_name]["photos"]
                    if photos.count_documents({"hash": photo_hash}) == 0:
                        now = datetime.datetime.now()
                        photos.insert_one({"hash": photo_hash, "path": photo_name,
                                           "date": now.strftime('%d-%m-%Y %H:%M:%S'), "isGallery": False,
                                           "galleryHidden": False})
                    else:
                        os.remove(f"static/news_photo/{photo_name}")
                    break
                photo_num += 1

        news = client[db_name]["news"]
        new_form = request.form
        news.insert_one({"ru_header": new_form["ru_header"], "ru_description": new_form["ru_description"],
                         "ru_text": new_form["ru_text"],
                         "en_header": new_form["en_header"], "en_description": new_form["en_description"],
                         "en_text": new_form["en_text"],
                         "cn_header": new_form["cn_header"], "cn_description": new_form["cn_description"],
                         "cn_text": new_form["cn_text"],
                         "de_header": new_form["de_header"], "de_description": new_form["de_description"],
                         "de_text": new_form["de_text"],
                         "vt_header": new_form["vt_header"], "vt_description": new_form["vt_description"],
                         "vt_text": new_form["vt_text"],
                         "fr_header": new_form["fr_header"], "fr_description": new_form["fr_description"],
                         "fr_text": new_form["fr_text"],
                         "photo_hash": photo_hash})

    else:
        print("GET")
    return redirect("/edit_new", code=302)


@app.route('/edit_new', methods=["GET", "POST"])
def edit_new():
    news = client[db_name]["news"]
    photos = client[db_name]["photos"]
    return render_template("edit_new.html", news=news, photos=photos)


@app.route('/edit_new/<id>', methods=["GET", "POST"])
def edit_one_new(id):
    news_form = NewsForm()
    news = client[db_name]["news"]
    new = news.find({"_id": ObjectId(id)})[0]
    photos = client[db_name]["photos"]
    if request.method == "POST":
        if "delete" in request.form:
            news.remove({"_id": ObjectId(id)})
            return redirect("/edit_new", code=302)
        photo_hash = ""
        photo = request.files["pictures"]
        if photo:
            files = os.listdir("static/news_photo")
            photo_num = 1
            while True:
                if f"{photo_num}.png" not in files and f"{photo_num}.jpg" not in files:
                    photo_name = str(photo_num) + photo.filename[-4:]
                    outpath_file = os.path.join(os.path.join(os.getcwd(), "static/news_photo"), photo_name)
                    photo.save(outpath_file)

                    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
                    with open(outpath_file, "rb") as f:  # Open the file to read it's bytes
                        fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
                        while len(fb) > 0:  # While there is still data being read from the file
                            file_hash.update(fb)  # Update the hash
                            fb = f.read(BLOCK_SIZE)  # Read the next block from the file

                    photo_hash = file_hash.hexdigest()
                    photos = client[db_name]["photos"]
                    if photos.count_documents({"hash": photo_hash}) == 0:
                        now = datetime.datetime.now()
                        photos.insert_one({"hash": photo_hash, "path": photo_name,
                                           "date": now.strftime('%d-%m-%Y %H:%M:%S'), "isGallery": False,
                                           "galleryHidden": False})
                    else:
                        os.remove(f"static/news_photo/{photo_name}")
                    break
                photo_num += 1
        if not photo_hash:
            photo_hash = news.find_one({"_id": ObjectId(id)})["photo_hash"]
        news = client[db_name]["news"]
        new_form = request.form
        news.update_one({"_id": ObjectId(id)},
                        {"$set": {"ru_header": new_form["ru_header"], "ru_description": new_form["ru_description"],
                                  "ru_text": new_form["ru_text"],
                                  "en_header": new_form["en_header"], "en_description": new_form["en_description"],
                                  "en_text": new_form["en_text"],
                                  "cn_header": new_form["cn_header"], "cn_description": new_form["cn_description"],
                                  "cn_text": new_form["cn_text"],
                                  "de_header": new_form["de_header"], "de_description": new_form["de_description"],
                                  "de_text": new_form["de_text"],
                                  "vt_header": new_form["vt_header"], "vt_description": new_form["vt_description"],
                                  "vt_text": new_form["vt_text"],
                                  "fr_header": new_form["fr_header"], "fr_description": new_form["fr_description"],
                                  "fr_text": new_form["fr_text"],
                                  "photo_hash": photo_hash}})
        return redirect("/edit_new", code=302)
    news_form.ru_text.data = new["ru_text"]
    news_form.en_text.data = new["en_text"]
    news_form.cn_text.data = new["cn_text"]
    news_form.de_text.data = new["de_text"]
    news_form.fr_text.data = new["fr_text"]
    news_form.vt_text.data = new["vt_text"]
    return render_template("edit_one_new.html", new=new, news_form=news_form)


@app.route('/add_photo', methods=["GET", "POST"])
def add_photo():
    print(request.args)
    return render_template("add_photo.html")


@app.route('/add_product', methods=["GET", "POST"])
def add_product():
    print(request.args)
    return render_template("add_product.html")


app.run(debug=True)
