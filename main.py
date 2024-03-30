from flask import render_template, Flask

app = Flask(__name__)


#
@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('index.html', title=title)


if __name__ == "__main__":
    app.run(port=8200, host="127.0.0.1")
