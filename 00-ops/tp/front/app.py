from flask import Flask, render_template
import requests

app = Flask(__name__)

API_URL = "tobefilled"


@app.context_processor
def utility_processor():
    def request_api():
        response = requests.get(API_URL).text
        return response

    return dict(request_api=request_api)


@app.route("/")
def hello():
    return render_template("./index.html")
