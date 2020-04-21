from flask import Flask, render_template, redirect, request
import Predict_Calories as pc
app = Flask(__name__)

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/home', methods = ['POST'])
def calories():
    if request.method == 'POST':
        f = request.files['userfile']
        path = "./static/{}".format(f.filename)
        f.save(path)
        item_class = pc.predict_class(path, False)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)