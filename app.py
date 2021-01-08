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
    if request.method == 'POST':
        data = {}
        data['on'] = True
        print("Nome Gruppo: "+str(request.form['name']))
        req = requests.put("http://"+str(bridgeip)+"/api/"+authuser+"/groups/"+str(request.form.get('name'))+"/state", data=json.dumps(data))
        print(str(req))
        print(req.status_code)
        return render_template('index.html')
        # TO-DO GESTIRE PAGINA 
    else:
        req = requests.get("http://"+str(bridgeip)+"/api/"+authuser+"/groups")
        lights = json.loads(req.content)
        groups = []
        for (k,v) in lights.items():
            if not 'Group for' in str(v['name']):
                groups.append((v['name'],v['state']['all_on']))
        return render_template('index.html', groups=groups)

if __name__ == '__main__':
    app.run(debug=True, port=serverport)