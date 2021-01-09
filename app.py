from flask import Flask, render_template, request
import yaml
import requests
import json

configinfo = yaml.load(open('./config.yaml'), Loader=yaml.FullLoader)
serverport = configinfo['serverport']
bridgeip = configinfo['bridgeip']
authuser = configinfo['authuser']
lampadinatest = configinfo['lampadinatest']

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
    app.run(host='0.0.0.0', debug=True, port=serverport)