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

@app.route('/creategroup', methods=['GET','POST'])
def creategroup():
    if request.method == 'GET':
        req = requests.get("http://"+str(bridgeip)+"/api/"+authuser+"/lights")
        lights_json = json.loads(req.content)
        lights = []
        for (k,v) in lights_json.items():
            lights.append((k,v['name']))
        return render_template('creategroup.html', lights=lights)
    if request.method == 'POST':
        print(str(request.form.get('gname'))+str(request.form.getlist('lights')))
        json_group = {}
        lights_new_group = []
        for light in request.form.getlist('lights'):
            lights_new_group.append(str(light))
        json_group['lights'] = lights_new_group
        json_group['name'] = str(request.form.get('gname'))
        json_group['type']= 'Zone'
        print(str(json.dumps(json_group)))
        req = requests.post("http://"+str(bridgeip)+"/api/"+authuser+"/groups/", data=json.dumps(json_group))
        return index()
        
if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', serverport)) != 0 :
            app.run(host='0.0.0.0', debug=True, port=serverport)
        else:
            app.run(host='0.0.0.0', debug=True, port=8081)
