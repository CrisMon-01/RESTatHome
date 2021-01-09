# REST@~

This webapp use the Philips HUE REST API. 
You can manage your lights with the browser only (for guests or without the mobile app). <br>

## Configure
You need to write a config file before start using it.
The file is used in the `app.py` in read only, so write a `config.yaml` in the main folder of the project.<br>
In the config.yaml you need
* IP of the Philips hue gateway 
* Access Token 
* Server Port to expose the page (I will remote it...)
example of config.yaml:
```
bridgeip: x.y.z.
authuser: xxxx-yyyy-zzzzzz
serverport: n
```
The information about the bridge IP and the token is in the official [Philips HUE SDK page](https://developers.meethue.com/develop/get-started-2/): 

## Run
`python3 app.py`

I made this only for fun. <br>
