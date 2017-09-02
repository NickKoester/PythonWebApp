from flask import Flask, render_template, request
from sheetAppend import sheetAppend

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/confirm', methods=['POST', 'GET'])
def confirm():
    if request.method == 'POST':
        result = request.form
        sheetAppend(list(result.values()))
        return render_template('confirm.html', result=result)


if __name__ == '__main__':
    app.run()
