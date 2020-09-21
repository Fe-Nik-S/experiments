
from flask import Flask


APP_VERSION = "0.0.1"


app = Flask(__name__)


@app.route("/")
def home():
    return ""


@app.route("/ping")
def ping():
    return {
        "version": APP_VERSION
    }


if __name__ == "__main__":
    app.run()
