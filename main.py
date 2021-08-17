from math import ceil

import flask_login
import pymongo
from flask import Flask, request, render_template, redirect, jsonify, session, flash, url_for
from flask_login import login_required, LoginManager, login_user, current_user, UserMixin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import MongoEngine
from forms import *
from bson.objectid import ObjectId
from processing import *
from flask_babel import Babel
from datetime import datetime, timedelta

BLOCK_SIZE = 65536
UPLOAD_FOLDER = "photos"

app = Flask(__name__, static_folder="static")

client = MongoClient("mongodb+srv://Bois:Rouge@boisrouge.aephg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db_name = "DataBase"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "86F27F78E9AA221425B98B46F337A"
app.config["LANGUAGES"] = ['en', 'ru', "zh"]
app.permanent_session_lifetime = timedelta(days=1)

babel = Babel(app)
db = MongoEngine(app)

login = LoginManager(app)
login.login_view = 'login'
login.init_app(app)


class User(UserMixin):
    def __init__(self, username, password, id):
        self.password_hash = generate_password_hash(password)
        self.username = username
        self.id = id

    def get_username(self):
        return self.username

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(username):
        return User("login", "piska", 1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("edit_new"))
    form = UserForm()
    if form.is_submitted():
        name = form.username.data
        password = form.password.data
        user_db_count = client[db_name]["users"].count_documents({"username": name})
        if user_db_count:
            user_db = client[db_name]["users"].find({"username": name})[0]
            user = User(user_db["username"], user_db["password"], 1)
            user.password_hash = user_db["password"]

            if user is not None and user.check_password(password):
                login_user(user)
                return redirect("admin/edit_new")
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('admin/login.html', title='Sign In', form=form)


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
@login_required
def admin_index():
    # return render_template("admin/admin.html")
    return render_template("admin/shortcuts.html")


@app.route('/admin/add_new', methods=["GET", "POST"])
@login_required
def add_new():
    news_form = NewsForm()
    print(flask_login.current_user)
    if news_form.validate_on_submit():
        photo_name = ""
        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client, False, "", "", "", "", "", "")

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
@login_required
def edit_new():
    news = client[db_name]["news"].find().sort("num_id", -1)
    return render_template("admin/edit_new.html", news=news)


@app.route('/admin/edit_new/<id>', methods=["GET", "POST"])
@login_required
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
            photo_name = save_photo(photo, client, False, "", "", "", "", "", "")
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
@login_required
def add_photo():
    photo_form = PhotosForm()
    if request.method == "POST":
        files = photo_form["files"].data
        descriptions_ru = request.form.getlist("description_ru")
        descriptions_en = request.form.getlist("description_en")
        descriptions_zh = request.form.getlist("description_zh")
        descriptions_de = request.form.getlist("description_de")
        descriptions_vt = request.form.getlist("description_vt")
        descriptions_fr = request.form.getlist("description_fr")
        for i in range(len(files)):
            print(files[i])
            photo_name = save_photo(files[i], client, True, descriptions_ru[i], descriptions_en[i],
                                    descriptions_zh[i], descriptions_de[i], descriptions_vt[i], descriptions_fr[i])
            print(photo_name)
        return redirect("../admin/edit_photo", 301)
    return render_template("admin/add_photo.html", photo_form=photo_form)


@app.route('/admin/edit_photo', methods=["GET", "POST"])
@login_required
def edit_photo():
    photos = client[db_name]["photos"].find({"isGallery": True}).sort("date", -1)
    return render_template("admin/edit_photo.html", photos=photos)


@app.route('/admin/edit_video', methods=["GET", "POST"])
@login_required
def edit_video():
    videos = client[db_name]["videos"].find().sort("date", pymongo.DESCENDING)
    video_form = VideoForm()

    if video_form.validate_on_submit():
        url = video_form.url.data

        check = False if client[db_name]["videos"].count_documents({"url": url}) > 0 else True
        if check:
            client[db_name]["videos"].insert_one({"url": url, "date": datetime.now()})

        return redirect("/admin/edit_video")

    return render_template("admin/edit_video.html", add_form=video_form, videos=videos)


@app.route("/admin/api/delete_video", methods=["GET", "POST"])
@login_required
def delete_video():
    vid = request.json.get("vid")
    print(vid)
    print(list(client[db_name]["videos"].find({"_id": ObjectId(vid)})))
    client[db_name]["videos"].delete_one({"_id": ObjectId(vid)})
    print(list(client[db_name]["videos"].find({"_id": ObjectId(vid)})))

    return jsonify({"status": "video deleted"})


@app.route('/admin/edit_photo/<photo_id>', methods=["GET", "POST"])
@login_required
def edit_one_photo(photo_id):
    photo_form = PhotosForm()
    photos = client[db_name]["photos"]
    if request.method == "GET":
        photo = photos.find({"_id": ObjectId(photo_id)})[0]
        return render_template("admin/edit_one_photo.html", photo=photo, photo_form=photo_form,
                               description_ru=photo["description_ru"], description_en=photo["description_en"],
                               description_de=photo["description_de"], description_zh=photo["description_zh"],
                               description_fr=photo["description_fr"], description_vt=photo["description_vt"])
    elif request.method == "POST":
        p_form = request.form
        galleryHidden = False
        if "galleryHidden" in p_form:
            galleryHidden = True

        photos.update_one({"_id": ObjectId(photo_id)},
                          {"$set": {"description_ru": p_form["description_ru"],
                                    "description_en": p_form["description_en"],
                                    "description_zh": p_form["description_zh"],
                                    "description_vt": p_form["description_vt"],
                                    "description_de": p_form["description_de"],
                                    "description_fr": p_form["description_fr"],
                                    "galleryHidden": galleryHidden}})
        return redirect("/admin/edit_photo", code=302)


@app.route('/admin/add_log', methods=["GET", "POST"])
@login_required
def add_log():
    logs_form = LogsForm()
    wood_types = client[db_name]["wood_types"].find()
    if logs_form.is_submitted():
        photo_name = ""
        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client, False, "", "", "", "", "", "")

        logs = client[db_name]["logs"]
        log_form = request.form
        print(log_form)
        logs.insert_one(
            {"log_title": log_form["log_title"],
             "type": log_form["type"],
             "log_diameter": log_form["log_diameter"],
             "log_length": log_form["log_length"],
             "ru_text": log_form["ru_text"],
             "en_text": log_form["en_text"],
             "zh_text": log_form["zh_text"],
             "de_text": log_form["de_text"],
             "vt_text": log_form["vt_text"],
             "fr_text": log_form["fr_text"],

             "photo_path": photo_name})
        return redirect("../admin/edit_logs", 301)
    return render_template("admin/add_log.html", logs_form=logs_form, wood_types=wood_types)


@app.route('/admin/edit_logs', methods=["GET", "POST"])
@login_required
def edit_logs():
    logs = client[db_name]["logs"].find()
    return render_template("admin/edit_logs.html", logs=logs)


@app.route('/admin/edit_logs/<id>', methods=["GET", "POST"])
@login_required
def edit_one_log(id):
    logs_form = LogsForm()
    logs = client[db_name]["logs"]
    wood_types = client[db_name]["wood_types"].find()
    log = logs.find({"_id": ObjectId(id)})[0]
    if logs_form.is_submitted():
        if "delete" in request.form:
            logs.remove({"_id": ObjectId(id)})
            return redirect("/admin/edit_logs", code=302)

        photo_name = log["photo_path"]
        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client, False, "", "", "", "", "", "")

        log_form = request.form
        print(log_form)
        logs.update_one({"_id": ObjectId(id)},
                        {"$set": {"log_title": log_form["log_title"],
                                  "type": log_form["type"],
                                  "log_diameter": log_form["log_diameter"],
                                  "log_length": log_form["log_length"],
                                  "ru_text": log_form["ru_text"],
                                  "en_text": log_form["en_text"],
                                  "zh_text": log_form["zh_text"],
                                  "de_text": log_form["de_text"],
                                  "vt_text": log_form["vt_text"],
                                  "fr_text": log_form["fr_text"],

                                  "photo_path": photo_name}})

        return redirect("/admin/edit_logs", code=302)

    logs_form.ru_text.data = log["ru_text"]
    logs_form.en_text.data = log["en_text"]
    logs_form.zh_text.data = log["zh_text"]
    logs_form.de_text.data = log["de_text"]
    logs_form.fr_text.data = log["fr_text"]
    logs_form.vt_text.data = log["vt_text"]

    return render_template("admin/edit_one_log.html", logs_form=logs_form, log=log, wood_types=wood_types)


@app.route('/admin/add_wood_board', methods=["GET", "POST"])
@login_required
def add_wood_board():
    wood_board_form = WoodBoardForm()
    wood_types = client[db_name]["wood_types"].find()
    if wood_board_form.is_submitted():
        photo_name = ""
        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client, False, "", "", "", "", "", "")

        wood_boards = client[db_name]["wood_boards"]
        wood_board_form_requested = request.form
        print(wood_board_form_requested)
        wood_boards.insert_one(
            {"wood_board_title": wood_board_form_requested["wood_board_title"],

             "wood_board_subcategory": wood_board_form_requested["wood_board_subcategory"],
             "type": wood_board_form_requested["type"],
             "wood_board_section": wood_board_form_requested["wood_board_section"],
             "wood_board_length": wood_board_form_requested["wood_board_length"],
             "wood_board_humidity": wood_board_form_requested["wood_board_humidity"],

             "ru_text": wood_board_form_requested["ru_text"],
             "en_text": wood_board_form_requested["en_text"],
             "zh_text": wood_board_form_requested["zh_text"],
             "de_text": wood_board_form_requested["de_text"],
             "vt_text": wood_board_form_requested["vt_text"],
             "fr_text": wood_board_form_requested["fr_text"],

             "photo_path": photo_name})
        return redirect("../admin/edit_wood_board", 301)
    return render_template("admin/add_wood_board.html", wood_board_form=wood_board_form, wood_types=wood_types)


@app.route('/admin/edit_wood_board', methods=["GET", "POST"])
@login_required
def edit_wood_board():
    wood_boards = client[db_name]["wood_boards"].find()
    return render_template("admin/edit_wood_board.html", wood_boards=wood_boards)


@app.route('/admin/edit_wood_board/<id>', methods=["GET", "POST"])
@login_required
def edit_one_wood_board(id):
    wood_board_form = WoodBoardForm()
    wood_boards = client[db_name]["wood_boards"]
    wood_types = client[db_name]["wood_types"].find()
    wood_board = wood_boards.find({"_id": ObjectId(id)})[0]
    if wood_board_form.is_submitted():
        if "delete" in request.form:
            wood_boards.remove({"_id": ObjectId(id)})
            return redirect("/admin/edit_logs", code=302)

        photo_name = wood_board["photo_path"]
        photo = request.files["pictures"]
        if photo:
            photo_name = save_photo(photo, client, False, "", "", "", "", "", "")

        wood_board_form_requested = request.form
        wood_boards.update_one({"_id": ObjectId(id)},
                               {"$set": {"wood_board_title": wood_board_form_requested["wood_board_title"],

                                         "wood_board_subcategory": wood_board_form_requested["wood_board_subcategory"],
                                         "type": wood_board_form_requested["type"],
                                         "wood_board_section": wood_board_form_requested["wood_board_section"],
                                         "wood_board_length": wood_board_form_requested["wood_board_length"],
                                         "wood_board_humidity": wood_board_form_requested["wood_board_humidity"],

                                         "ru_text": wood_board_form_requested["ru_text"],
                                         "en_text": wood_board_form_requested["en_text"],
                                         "zh_text": wood_board_form_requested["zh_text"],
                                         "de_text": wood_board_form_requested["de_text"],
                                         "vt_text": wood_board_form_requested["vt_text"],
                                         "fr_text": wood_board_form_requested["fr_text"],

                                         "photo_path": photo_name}})

        return redirect("/admin/edit_wood_board", code=302)

    wood_board_form.ru_text.data = wood_board["ru_text"]
    wood_board_form.en_text.data = wood_board["en_text"]
    wood_board_form.zh_text.data = wood_board["zh_text"]
    wood_board_form.de_text.data = wood_board["de_text"]
    wood_board_form.fr_text.data = wood_board["fr_text"]
    wood_board_form.vt_text.data = wood_board["vt_text"]

    return render_template("admin/edit_one_wood_board.html", wood_board_form=wood_board_form, wood_board=wood_board,
                           wood_types=wood_types)


@app.route('/admin/add_wood_type', methods=["GET", "POST"])
@login_required
def add_wood_type():
    wood_type_form = WoodTypeForm()
    if wood_type_form.validate_on_submit():
        title = request.form.get("title")
        descriptions = request.form.get("description")
        files = wood_type_form["files"].data
        wood_types = client[db_name]["wood_types"]
        wood_types.insert_one({"title": title,
                               "description": descriptions,
                               "path": save_photo(files, client, False, "", "", "", "", "", "")})
        return redirect("../admin/edit_wood_type", 301)
    return render_template("admin/add_wood_type.html", wood_type_form=wood_type_form)


@app.route('/admin/edit_wood_type', methods=["GET", "POST"])
@login_required
def edit_wood_type():
    wood_types = client[db_name]["wood_types"].find()
    return render_template("admin/edit_wood_type.html", wood_types=wood_types)


@app.route('/admin/edit_wood_type/<photo_id>', methods=["GET", "POST"])
@login_required
def edit_one_wood_type(photo_id):
    wood_type_form = WoodTypeForm()
    wood_types = client[db_name]["wood_types"]
    wood_type = wood_types.find({"_id": ObjectId(photo_id)})[0]
    if request.method == "GET":
        return render_template("admin/edit_one_wood_type.html", wood_type=wood_type, wood_type_form=wood_type_form)
    elif request.method == "POST":
        t_form = request.form
        if "delete" in t_form:
            wood_types.remove({"_id": ObjectId(photo_id)})
            return redirect("/admin/edit_wood_type", code=302)

        photo_name = wood_type["path"]
        photo = request.files["files"]
        if photo:
            photo_name = save_photo(photo, client, False, "", "", "", "", "", "")
        wood_types.update_one({"_id": ObjectId(photo_id)},
                              {"$set": {"title": t_form["title"],
                                        "description": t_form["description"],
                                        "path": photo_name}})
        return redirect("/admin/edit_wood_type", code=302)


@app.route('/admin/add_product', methods=["GET", "POST"])
@login_required
def add_product():
    product_form = ProductForm()
    if product_form.validate_on_submit():
        title = request.form.get("title")
        files = product_form["files"].data
        products = client[db_name]["products"]
        product_form_requested = request.form
        products.insert_one({"title": title,
                             "ru_text": product_form_requested["ru_text"],
                             "en_text": product_form_requested["en_text"],
                             "zh_text": product_form_requested["zh_text"],
                             "de_text": product_form_requested["de_text"],
                             "vt_text": product_form_requested["vt_text"],
                             "fr_text": product_form_requested["fr_text"],
                             "wood_type": product_form_requested.get("wood_type"),
                             "visible": True,
                             "path": save_photo(files, client, False, "", "", "", "", "", "")})
        return redirect("../admin/edit_product", 301)
    wood_types = client[db_name]["wood_types"].find()
    return render_template("admin/add_product.html", product_form=product_form, wood_types=wood_types)


@app.route('/admin/edit_product', methods=["GET", "POST"])
@login_required
def edit_product():
    products = client[db_name]["products"].find()
    return render_template("admin/edit_product.html", products=products)


@app.route('/admin/edit_product/<id>', methods=["GET", "POST"])
@login_required
def edit_one_product(id):
    product_form = ProductForm()
    products = client[db_name]["products"]
    product = products.find({"_id": ObjectId(id)})[0]
    if request.method == "GET":
        wood_types = client[db_name]["wood_types"].find()

        product_form.ru_text.data = product["ru_text"]
        product_form.en_text.data = product["en_text"]
        product_form.zh_text.data = product["zh_text"]
        product_form.de_text.data = product["de_text"]
        product_form.fr_text.data = product["fr_text"]
        product_form.vt_text.data = product["vt_text"]

        return render_template("admin/edit_one_product.html", product=product, product_form=product_form,
                               wood_types=wood_types)
    elif product_form.validate_on_submit():
        p_form = request.form
        if "delete" in p_form:
            products.remove({"_id": ObjectId(id)})

        else:
            photo_name = ""
            if product["path"] and (".jpg" in product["path"] or ".png" in product["path"]):
                photo_name = product["path"]
            photo = request.files["files"]
            if photo:
                photo_name = save_photo(photo, client, False, "", "", "", "", "", "")
            visible = False
            if "visible" in p_form:
                visible = True
            products.update_one({"_id": ObjectId(id)},
                                {"$set": {"title": p_form["title"],
                                          "ru_text": p_form["ru_text"],
                                          "en_text": p_form["en_text"],
                                          "zh_text": p_form["zh_text"],
                                          "de_text": p_form["de_text"],
                                          "vt_text": p_form["vt_text"],
                                          "fr_text": p_form["fr_text"],
                                          "visible": visible,
                                          "path": photo_name,
                                          "wood_type": p_form["type"]}})
        return redirect("/admin/edit_product", code=302)


@app.route('/admin/contacts', methods=["GET", "POST"])
@login_required
def admin_contacts():
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
    photos, videos = [], []

    if active == "video":
        videos = list(client[db_name]["videos"].find().sort("date", pymongo.DESCENDING))
    else:
        photos = list(client[db_name]["photos"].find({"isGallery": True, "galleryHidden": False},
                                                     {"path": 1, "date": 1, "description": 1}))

    return render_template("client/gallery.html", photos=photos, photo_page=photo_page, video_page=video_page,
                           videos=videos, active=active)


@app.route("/contacts", methods=["GET"])
def contacts():
    contacts_list = list(client[db_name]["contacts"].find())

    return render_template("client/contacts.html", contacts=contacts_list)


@app.route("/services", methods=["GET"])
def services():
    return render_template("client/services.html")


@app.route("/species", methods=["GET"])
def species():
    species_list = list(client[db_name]["wood_types"].find())
    return render_template("client/species.html", species=species_list)


@app.route("/products", methods=["GET"])
def products():
    return render_template("client/products.html")


@app.route("/logs", methods=["GET"])
def logs():
    return render_template("client/logs.html")


@app.post("/api/footer_form")
def footer_form():
    name, email = request.json.values()
    print(name, email)
    return "123"


app.run(debug=True)
