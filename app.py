from flask import Flask, render_template, request
import yaml
import requests
import json

configinfo = yaml.load(open('./config.yaml'))
serverport = configinfo['serverport']
bridgeip = configinfo['bridgeip']
authuser = configinfo['authuser']
lampadinatest = configinfo['lampadinatest']

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        data = {}
        data['on'] = True
        req = requests.put("http://"+str(bridgeip)+"/api/"+authuser+"/lights/"+str(lampadinatest)+"/state", data=json.dumps(data))
        print(str(req))
        print(req.status_code)
    return render_template('index.html') #"Hello World!"

if __name__ == '__main__':
    app.run(debug=True, port=serverport)