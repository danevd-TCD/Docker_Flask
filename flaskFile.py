from flask import Flask, render_template
import os

#Note: configure the below template_folder and static_folder locations to match your persistent docker volume
#so that Flask can find static/template objects. In this case, my persistent docker volume is 
#       /var/Team10_App/
#and docker initiates a flask-apache instance in
#       /var/www/apache-flask
#so I describe the static and template folders *relative* to the flask file instance.
#the below persistent files are accessible on a windows-WSL2 docker setup using my docker-compose.yml file at:
#       \\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_flask_persistent-data\_data\frontend


app = Flask(__name__, static_url_path='', template_folder='../../Team10_App/frontend/templates', static_folder='../../Team10_App/frontend/static')



#templates = '/var/Team10_App/frontend/templates/'

#@app.route('/')
#def root():
#	return("Hello")

@app.route('/')
def root():
        return render_template('index.html')


if __name__ == "__main__":
	app.run(debug=True)
