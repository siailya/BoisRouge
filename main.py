from flask import Flask, request, redirect
from flask import render_template
from flask_mongoengine import MongoEngine
import models
from news_form import NewsForm

UPLOAD_FOLDER = "news_photo"

app = Flask(__name__, static_folder="static")
app.config['MONGODB_SETTINGS'] = {
    'host': "mongodb+srv://Bois:Rouge@boisrouge.aephg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "86F27F78E9AA221425B98B46F337A"
db = MongoEngine(app)


@app.route('/', methods=["GET", "POST"])
def index():
    news_form = NewsForm()

    print(news_form.validate_on_submit())
    print(news_form.data)

    print(news_form.ru_description.errors)
    print(news_form.ru_header.errors)
    print(news_form.ru_text.errors)

    return render_template("admin.html", news_form=news_form)


@app.route('/add_specifies', methods=["GET", "POST"])
def add_specifies():
    print(request.args)
    return render_template("admin.html")


@app.route('/add_new', methods=["GET", "POST"])
def add_new():
    print(request.form)

    if request.method == "POST":
        pass
    #     text_ru = models.NewText(header="Русский заголовок",
    #                              brief_description="Русское краткое",
    #                              description="Русское описание")
    #     form = request.form
    #     new = models.New(text_ru=text_ru, **form).save()
    #     print("new", new)
    #     print(request.files.getlist("new_photos"))
    #     print("photo")

    else:
        print("GET")
    return redirect("/", code=302)


app.run(debug=True)
