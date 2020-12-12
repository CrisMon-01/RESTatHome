from flask import Flask, render_template, request
import yaml

configinfo = yaml.load(open('./config.yaml'))
serverport = configinfo['serverport']

app = Flask(__name__)

@app.route('/', methods=['GET','PUT'])
def index():
    # if request.methods == 'PUT':
    #     request
    return render_template('index.html') #"Hello World!"

if __name__ == '__main__':
    app.run(debug=True, port=serverport)