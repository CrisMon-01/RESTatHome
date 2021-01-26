from flask import Flask, render_template, request
import yaml
import requests
import json
import socket

configinfo = yaml.load(open('./config.yaml'), Loader=yaml.FullLoader)
try:
    serverport = configinfo['serverport']
except:
    serverport = 8888
    print("You will expose on 8888")
bridgeip = configinfo['bridgeip']
authuser = configinfo['authuser']

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    req = requests.get("http://"+str(bridgeip)+"/api/"+authuser+"/groups")
    lights = json.loads(req.content)
    groups = []
    for (k,v) in lights.items():
        if not 'Group for' in str(v['name']):
            groups.append((v['name'],v['state']['all_on']))
    if request.method == 'POST':
        data = {}
        print("Nome Gruppo: "+str(request.form.get('light')))
        for (k,v) in lights.items():
            if str(request.form.get('light')) in str(v['name']):
                status = v['state']['all_on']
                nextstatus = not(bool(status))
                data['on'] = nextstatus
                req = requests.put("http://"+str(bridgeip)+"/api/"+authuser+"/groups/"+k+"/action", data=json.dumps(data))
        return render_template('index.html', groups=groups)
    else:
        return render_template('index.html', groups=groups)

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', serverport)) != 0 :
            app.run(host='0.0.0.0', debug=True, port=serverport)
        else:
            app.run(host='0.0.0.0', debug=True, port=8081)
