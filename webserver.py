from flask import Flask
from flask import request, render_template
app = Flask(__name__)

status = 0

@app.route('/', methods=['GET','POST'])
def check_pressed():
    global status
    if request.method == 'POST':
        status = 1
    #elif request.method == 'GET':
    return render_template('test.html')

def kill():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def run():
    app.run(host='0.0.0.0')

def getstatus():
    global status
    s = status
    status = 0
    return s

if __name__ == '__main__':
    app.run(debug=True)
