from flask import Flask, render_template
import os

app = Flask(__name__, static_url_path='/var/Team10_App/frontend')

#@app.route('/')
#def root():
#	return("Hello")

@app.route('/')
def root():
        return render_template('templates/index.html')


if __name__ == "__main__":
	app.run()
