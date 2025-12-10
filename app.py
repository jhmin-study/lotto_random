from flask import Flask, render_template
import random

app = Flask(__name__)

def generate_lotto():
    return sorted(random.sample(range(1, 46), 6))

@app.route("/")
def index():
    numbers = generate_lotto()
    return render_template("index.html", numbers=numbers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
