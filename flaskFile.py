from flask import Flask, render_template, send_from_directory
import os

#Note: configure the below template_folder and static_folder locations to match your persistent docker volume
#so that Flask can find static/template objects. In this case, my persistent docker volume is 
#       /var/Flask_Persistent/
#and docker initiates a flask-apache instance in
#       /var/www/apache-flask
#so I describe the static and template folders *relative* to the flask file instance.
#the below persistent files are accessible on a windows-WSL2 docker setup using my docker-compose.yml file at:
#       \\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_flask_persistent-data\_data\frontend


app = Flask(__name__, static_url_path='', template_folder='../../Flask_Persistent/frontend/', static_folder='../../Flask_Persistent/frontend/')



#@app.route('/')
#def root():
#	return("Hello")

@app.route('/')
def root():
        return render_template('index.html')                                        #allows for jinja templating if necessary
        #return send_from_directory(app.static_folder, 'index.html')    #alternative to above

@app.route('/css/<path:CSS_filename>')
def css(CSS_filename):
        return send_from_directory(app.static_folder, ('css/' + CSS_filename))
        
@app.route('/fonts/<path:Font_filename>')
def fonts(Font_filename):
        return send_from_directory(app.static_folder, ('fonts/' + Font_filename))
        
@app.route('/js/<path:js_filename>')
def js(js_filename):
        return send_from_directory(app.static_folder , ('js/' + js_filename))
        
@app.route('/icons/<path:icon_filename>')
def icons(icon_filename):
        return send_from_directory(app.static_folder , ('icons/' + icon_filename))

if __name__ == "__main__":
	app.run(debug=True)
