from flask import Flask
import os

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
	return("Hello")

if __name__ == "__main__":
	app.run()
