from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/admin')
def index():
    return render_template("admin.html")


app.run()
