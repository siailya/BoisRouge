from flask import Flask, request, redirect
from flask import render_template
from flask_mongoengine import MongoEngine
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
    return render_template("admin.html")


@app.route('/add_new', methods=["GET", "POST"])
def add_new():
    news_form = NewsForm()
    print(news_form.validate_on_submit())
    if request.method == "POST":
        form = request.data
        print(form)
        print(request.form)
        print(request.files)
    else:
        print("GET")
    return render_template("add_new.html", news_form=news_form)


@app.route('/add_photo', methods=["GET", "POST"])
def add_photo():
    print(request.args)
    return render_template("add_photo.html")


@app.route('/add_product', methods=["GET", "POST"])
def add_product():
    print(request.args)
    return render_template("add_product.html")


app.run(debug=True)
