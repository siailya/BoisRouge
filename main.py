from flask import Flask, request, redirect
from flask import render_template
from flask_mongoengine import MongoEngine
import models


UPLOAD_FOLDER = "news_photo"

app = Flask(__name__, static_folder="static")
app.config['MONGODB_SETTINGS'] = {
    'host': "mongodb+srv://Bois:Rouge@boisrouge.aephg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db = MongoEngine(app)


@app.get('/')
def index():
    return render_template("admin.html")


@app.route('/add_specifies', methods=["GET", "POST"])
def add_specifies():
    print(request.args)
    return render_template("admin.html")


@app.route('/add_new', methods=["GET", "POST"])
def add_new():
    if request.method == "POST":
        text_ru = models.NewText(header="Русский заголовок",
                                 brief_description="Русское краткое",
                                 description="Русское описание")
        form = request.form
        new = models.New(text_ru=text_ru, **form).save()
        print("new", new)
        print(request.files.getlist("new_photos"))
        print("photo")

    else:
        print("GET")
    return redirect("/", code=302)


app.run()
