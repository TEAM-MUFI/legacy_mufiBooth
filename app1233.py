from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("new-2.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)