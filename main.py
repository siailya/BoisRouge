from flask import Flask, request, render_template, redirect, session
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from news_form import NewsForm
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
    print(session)
    params_lang = request.args.get('lang')
    if params_lang and params_lang.lower() in app.config["LANGUAGES"]:
        session["lang"] = request.args.get('lang')
        return request.args.get('lang')
    elif session.get("lang"):
        return session["lang"]
    else:
        session["lang"] = request.accept_languages.best_match(app.config['LANGUAGES'])
        return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("admin.html")


@app.route('/add_new', methods=["GET", "POST"])
def add_new():
    news_form = NewsForm()
    if news_form.validate_on_submit():
        photo_name = ""
        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client)

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
                         "date": datetime.now().strftime('%d-%m-%Y'),
                         "num_id": num_id})
    return render_template("add_new.html", news_form=news_form)


@app.route('/edit_new', methods=["GET", "POST"])
def edit_new():
    news = client[db_name]["news"].find().sort("num_id", -1)
    return render_template("edit_new.html", news=news)


@app.route('/edit_new/<id>', methods=["GET", "POST"])
def edit_one_new(id):
    news_form = NewsForm()
    news = client[db_name]["news"]
    new = news.find({"_id": ObjectId(id)})[0]
    if news_form.validate_on_submit():
        if "delete" in request.form:
            news.remove({"_id": ObjectId(id)})
            return redirect("/edit_new", code=302)

        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client)
        else:
            photo_name = news.find_one({"_id": ObjectId(id)})["photo_path"]
        news = client[db_name]["news"]
        new_form = request.form
        news.update_one({"_id": ObjectId(id)},
                        {"$set": {"ru_header": new_form["ru_header"], "ru_description": new_form["ru_description"],
                                  "ru_text": new_form["ru_text"],
                                  "en_header": new_form["en_header"], "en_description": new_form["en_description"],
                                  "en_text": new_form["en_text"],
                                  "zh_header": new_form["zh_header"], "zh_description": new_form["zh_description"],
                                  "zh_text": new_form["zh_text"],
                                  "de_header": new_form["de_header"], "de_description": new_form["de_description"],
                                  "de_text": new_form["de_text"],
                                  "vt_header": new_form["vt_header"], "vt_description": new_form["vt_description"],
                                  "vt_text": new_form["vt_text"],
                                  "fr_header": new_form["fr_header"], "fr_description": new_form["fr_description"],
                                  "fr_text": new_form["fr_text"],
                                  "photo_path": photo_name}})
        return redirect("/edit_new", code=302)
    news_form.ru_text.data = new["ru_text"]
    news_form.en_text.data = new["en_text"]
    news_form.zh_text.data = new["zh_text"]
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


@app.route("/home", methods=["GET"])
def home():
    return render_template("index.html", title="Главная")


@app.route("/news", methods=["GET"])
def news():
    locale = get_locale().lower()
    news = list(client[db_name]["news"].find())
    locale_news = []

    for n in news:
        if not n.get("photo_path"):
            locale_news.append({
                "_id": str(n["_id"]),
                "picture": n.get("photo_hash"),
                "header": n[locale + "_header"],
                "description": n[locale + "_description"],
                "text": n[locale + "_text"]
            })
        else:
            locale_news.append({
                "_id": str(n["_id"]),
                "picture": n.get("photo_path"),
                "header": n[locale + "_header"],
                "description": n[locale + "_description"],
                "text": n[locale + "_text"]
            })

    print(locale_news)
    return render_template("news.html", title="Новости", news=locale_news)


@app.route("/news/<nid>", methods=["GET"])
def new_item(nid):
    locale = get_locale().lower()
    if locale == "zh":
        locale = "zh"

    news_item = list(client[db_name]["news"].find({"_id": ObjectId(nid)}))[0]
    locale_news_item = {
        "picture": news_item["photo_path"],
        "header": news_item[locale + "_header"],
        "description": news_item[locale + "_description"],
        "text": news_item[locale + "_text"]
    }

    return render_template("news_item.html", news_item=locale_news_item)


@app.route('/contacts', methods=["GET", "POST"])
def contacts():
    return render_template("contacts.html")


app.run(debug=True)
