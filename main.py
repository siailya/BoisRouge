from math import ceil

import pymongo
from flask import Flask, request, render_template, redirect, session, g
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from forms import *
from bson.objectid import ObjectId
from processing import *
from flask_babel import Babel
from datetime import datetime

BLOCK_SIZE = 65536
UPLOAD_FOLDER = "news_photo"

app = Flask(__name__, static_folder="static")

client = MongoClient("mongodb+srv://Bois:Rouge@boisrouge.aephg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db_name = "DataBase"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "86F27F78E9AA221425B98B46F337A"
app.config["LANGUAGES"] = ['en', 'ru', "zh"]

babel = Babel(app)
db = MongoEngine(app)


@babel.localeselector
def get_locale():
    params_lang = request.args.get('lang')
    if params_lang and params_lang.lower() in app.config["LANGUAGES"]:
        session["lang"] = request.args.get('lang')
        return request.args.get('lang')
    elif session.get("lang"):
        return session["lang"]
    else:
        session["lang"] = request.accept_languages.best_match(app.config['LANGUAGES'])
        return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/admin', methods=["GET", "POST"])
def admin_index():
    # return render_template("admin/admin.html")
    return render_template("admin/shortcuts.html")


@app.route('/admin/add_new', methods=["GET", "POST"])
def add_new():
    news_form = NewsForm()
    if news_form.validate_on_submit():
        photo_name = ""
        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client, False, "")

        news = client[db_name]["news"]
        new_form = request.form
        num_id = 1
        if news.find().count() != 0:
            num_id = news.find().sort("num_id", -1)[0]["num_id"] + 1
        news.insert_one({"ru_header": new_form["ru_header"],
                         "ru_description": new_form["ru_description"],
                         "ru_text": new_form["ru_text"],

                         "en_header": new_form["en_header"],
                         "en_description": new_form["en_description"],
                         "en_text": new_form["en_text"],

                         "zh_header": new_form["zh_header"],
                         "zh_description": new_form["zh_description"],
                         "zh_text": new_form["zh_text"],

                         "de_header": new_form["de_header"],
                         "de_description": new_form["de_description"],
                         "de_text": new_form["de_text"],

                         "vt_header": new_form["vt_header"],
                         "vt_description": new_form["vt_description"],
                         "vt_text": new_form["vt_text"],

                         "fr_header": new_form["fr_header"],
                         "fr_description": new_form["fr_description"],
                         "fr_text": new_form["fr_text"],

                         "photo_path": photo_name,
                         "date": datetime.now(),
                         "num_id": num_id})
        return redirect("../admin/edit_new", 301)
    return render_template("admin/add_new.html", news_form=news_form)


@app.route('/admin/edit_new', methods=["GET", "POST"])
def edit_new():
    news = client[db_name]["news"].find().sort("num_id", -1)
    return render_template("admin/edit_new.html", news=news)


@app.route('/admin/edit_new/<id>', methods=["GET", "POST"])
def edit_one_new(id):
    news_form = NewsForm()
    news = client[db_name]["news"]
    new = news.find({"_id": ObjectId(id)})[0]
    if news_form.validate_on_submit():
        if "delete" in request.form:
            news.remove({"_id": ObjectId(id)})
            return redirect("/admin/edit_new", code=302)

        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client, False, "")
        else:
            photo_name = news.find_one({"_id": ObjectId(id)})["photo_path"]
        news = client[db_name]["news"]
        new_form = request.form
        news.update_one({"_id": ObjectId(id)},
                        {"$set": {"ru_header": new_form["ru_header"],
                                  "ru_description": new_form["ru_description"],
                                  "ru_text": new_form["ru_text"],

                                  "en_header": new_form["en_header"],
                                  "en_description": new_form["en_description"],
                                  "en_text": new_form["en_text"],

                                  "zh_header": new_form["zh_header"],
                                  "zh_description": new_form["zh_description"],
                                  "zh_text": new_form["zh_text"],

                                  "de_header": new_form["de_header"],
                                  "de_description": new_form["de_description"],
                                  "de_text": new_form["de_text"],

                                  "vt_header": new_form["vt_header"],
                                  "vt_description": new_form["vt_description"],
                                  "vt_text": new_form["vt_text"],

                                  "fr_header": new_form["fr_header"],
                                  "fr_description": new_form["fr_description"],
                                  "fr_text": new_form["fr_text"],

                                  "photo_path": photo_name}})

        return redirect("/admin/edit_new", code=302)

    news_form.ru_text.data = new["ru_text"]
    news_form.en_text.data = new["en_text"]
    news_form.zh_text.data = new["zh_text"]
    news_form.de_text.data = new["de_text"]
    news_form.fr_text.data = new["fr_text"]
    news_form.vt_text.data = new["vt_text"]

    return render_template("admin/edit_one_new.html", new=new, news_form=news_form)


@app.route('/admin/add_photo', methods=["GET", "POST"])
def add_photo():
    photo_form = PhotosForm()
    if request.method == "POST":
        files = photo_form["files"].data
        descriptions = request.form.getlist("description")
        for i in range(len(files)):
            print(files[i])
            photo_name = save_photo(files[i], client, True, descriptions[i])
            print(photo_name)
        return redirect("../admin/edit_photo", 301)
    return render_template("admin/add_photo.html", photo_form=photo_form)


@app.route('/admin/edit_photo', methods=["GET", "POST"])
def edit_photo():
    photos = client[db_name]["photos"].find({"isGallery": True}).sort("date", -1)
    return render_template("admin/edit_photo.html", photos=photos)


@app.route('/admin/edit_photo/<photo_id>', methods=["GET", "POST"])
def edit_one_photo(photo_id):
    photo_form = PhotosForm()
    photos = client[db_name]["photos"]
    if request.method == "GET":
        photo = photos.find({"_id": ObjectId(photo_id)})[0]
        return render_template("admin/edit_one_photo.html", photo=photo, photo_form=photo_form,
                               description=photo["description"])
    elif request.method == "POST":
        p_form = request.form
        galleryHidden = False
        if "galleryHidden" in p_form:
            galleryHidden = True
            print(request.form, photo_id)

        photos.update_one({"_id": ObjectId(photo_id)},
                          {"$set": {"description": p_form["description"],
                                    "galleryHidden": galleryHidden}})
        return redirect("/admin/edit_photo", code=302)


@app.route('/admin/add_product', methods=["GET", "POST"])
def add_product():
    print(request.args)
    return render_template("admin/add_product.html")


@app.route('/admin/add_wood_type', methods=["GET", "POST"])
def add_wood_type():
    wood_type_form = WoodTypeForm()
    if request.method == "POST":
        title = request.form.get("title")
        descriptions = request.form.get("description")
        files = wood_type_form["files"].data[0]
        wood_types = client[db_name]["wood_types"]
        wood_types.insert_one({"title": title,
                               "description": descriptions,
                               "path": save_photo(files, client, False, "")})
        return redirect("../admin/edit_wood_type", 301)
    return render_template("admin/add_wood_type.html", wood_type_form=wood_type_form)


@app.route('/admin/edit_wood_type', methods=["GET", "POST"])
def edit_wood_type():
    wood_types = client[db_name]["wood_types"].find()
    return render_template("admin/edit_wood_type.html", wood_types=wood_types)


@app.route('/admin/edit_wood_type/<photo_id>', methods=["GET", "POST"])
def edit_one_wood_type(photo_id):
    wood_type_form = WoodTypeForm()
    wood_types = client[db_name]["wood_types"]
    if request.method == "GET":
        wood_type = wood_types.find({"_id": ObjectId(photo_id)})[0]
        return render_template("admin/edit_one_wood_type.html", wood_type=wood_type, wood_type_form=wood_type_form)
    elif request.method == "POST":
        t_form = request.form
        if "delete" in t_form:
            wood_types.remove({"_id": ObjectId(photo_id)})
            return redirect("/admin/edit_wood_type", code=302)
        wood_types.update_one({"_id": ObjectId(photo_id)},
                              {"$set": {"title": t_form["title"],
                                        "description": t_form["description"]}})
        return redirect("/admin/edit_wood_type", code=302)


@app.route('/admin/contacts', methods=["GET", "POST"])
def contacts():
    contact_form = ContactsForm()
    contacts = client[db_name]["contacts"]
    if request.method == "POST":
        ids = request.form.getlist("id")
        types = request.form.getlist("type")
        values = request.form.getlist("value")
        for i in range(len(ids)):
            if ids[i]:
                contacts.update_one({"_id": ObjectId(ids[i])},
                                    {"$set": {"type": types[i], "value": values[i]}})
            else:
                last_id = contacts.insert_one({"type": types[i], "value": values[i]})
                ids.append(last_id.inserted_id)
        contacts.delete_many({"_id": {"$nin": list(map(ObjectId, [id for id in ids if id]))}})
    contacts = contacts.find()
    return render_template("admin/contacts.html", contact_form=contact_form, contacts=contacts)


@app.route("/", methods=["GET"])
def index():
    return render_template("client/index.html")


@app.route("/news")
@app.route("/news/<page>", methods=["GET"])
def news(page=None):
    NEWS_ON_PAGE = 6

    if (page is None) or (page == 1):
        page = 1

    news = list(
        client[db_name]["news"].find({}, limit=NEWS_ON_PAGE, skip=int(page) * NEWS_ON_PAGE - NEWS_ON_PAGE).sort(
            [("num_id", pymongo.DESCENDING)]))

    news_count = client[db_name]["news"].count()
    news_pages = ceil(news_count / NEWS_ON_PAGE)

    print(news_count)
    print(news_count // NEWS_ON_PAGE)
    print(news_count % NEWS_ON_PAGE)

    locale = get_locale().lower()
    locale_news = []

    for n in news:
        if not n.get("photo_path"):
            locale_news.append({
                "nid": str(n["num_id"]),
                "date": n["date"],
                "picture": n.get("photo_hash"),
                "header": n[locale + "_header"],
                "description": n[locale + "_description"],
                "text": n[locale + "_text"]
            })
        else:
            locale_news.append({
                "nid": str(n["num_id"]),
                "date": n["date"],
                "picture": n.get("photo_path"),
                "header": n[locale + "_header"],
                "description": n[locale + "_description"],
                "text": n[locale + "_text"]
            })

    return render_template("client/news.html", title="Новости", news=locale_news, count=news_count, pages=news_pages,
                           current_page=page)


@app.route("/read_news/<nid>", methods=["GET"])
def new_item(nid):
    locale = get_locale().lower()

    news_item = list(client[db_name]["news"].find({"num_id": int(nid)}))[0]
    print(news_item)
    locale_news_item = {
        "nid": int(news_item["num_id"]),
        "picture": news_item["photo_path"],
        "header": news_item[locale + "_header"],
        "date": news_item["date"],
        "description": news_item[locale + "_description"],
        "text": news_item[locale + "_text"]
    }

    news_count = client[db_name]["news"].count()
    print(news_count)

    return render_template("client/news_item.html", news_item=locale_news_item, news_count=news_count)


@app.route("/gallery", methods=["GET"])
def photos_gallery(page=None):
    photo_page = request.args.get("photoPage")
    video_page = request.args.get("videoPage")
    active = request.args.get("active")

    photos = list(client[db_name]["photos"].find({"isGallery": True, "galleryHidden": False},
                                                 {"path": 1, "date": 1, "description": 1}))
    return render_template("client/gallery.html", photos=photos, photo_page=photo_page, video_page=video_page,
                           active=active)


@app.post("/api/footer_form")
def footer_form():
    name, email = request.json.values()
    print(name, email)
    return "123"


app.run(debug=True)
