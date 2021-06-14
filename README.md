# Docker_Flask
A dockerised Flask/Apache instance complete with WSGI configuration, running Flask 2.0 on Python 3. This readme is aimed towards those who may never have used Docker before, and so spells out steps/procedures some might fight elementary or obvious.

Partially based on [carlostighe](https://github.com/carlostighe/apache-flask)'s repo, but updated for Python 3 and mod_WSGI use, this repository will get you up and running with a Flask instance running behind Apache, that serves files/folders/etc. from a persistent docker volume folder, allowing you to modify your sites' contents without having to rebuild your docker instance.

However, changes to the Flask file `flaskFile.py` *will* require a docker rebuild; in other words, backend changes will require a (brief, potentially automatable) server (aka docker instance) restart, but frontend work is seperate and the latest frontend files placed in the relevant directories will be served immediately on change.

## Default config/folder locations
Note that modifying the folder locations provided in this repository may prove somewhat complex, as the same locations appear over several files due to the nature of configuring both Flask and Apache + mod_WSGI to serve files from a specified folder. 

By default, the Flask file ( `flaskFile.py` ) will reside in `/var/www/apache-Flask`

The persistent docker volume accessible within the docker instance is located at `/var/Flask_Persistent/`, and by default Flask will look for a subfolder therein named `frontend` to serve static/template/etc. content.

If, for any reason, these folder locations do not suit, you are free to refactor all mentions of the errant folder structure present in the following files:

* `apache-flask.conf`
* `apache-flask.wsgi`
* `docker-compose.yml`
* `Dockerfile`
* `flaskFile.py`

By default, the `requirements.txt` file used by Docker to install all required pip packages is located in the `/app` folder. Installing/removing a python package means rebuilding your docker instance.

## Getting started

### What you'll need

* Docker + Docker Compose (latest versions)
   
   N.B: For Windows specifically, use the [Docker for WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/)
* ~650MB of storage space
* Access to a system with a CPU capable of virtualisation

## Setup and basic start/stop commands
Having installed Docker and Docker Compose, follow these steps:

1. Clone/download this repository into a folder of your choice.
2. In the root directory (Docker_Flask, unless you've renamed the folder), run the following command:
   
   `docker-compose up -d`
3. Docker compose will now build our instance, and upon completing, you should be able to access your server through either your device's (W)LAN IP (not your external one, unless you've allowed such connections through your firewall), or through "localhost". 
4. Check to see if your application is running by typing `docker ps`; if you need to kill the server, type `docker kill <CONTAINER ID>`, or use `docker stop <CONTAINER ID>` to issue a stop command that gives applications time to cease operations first. 
5. To restart your docker compose file, make sure you're in the root directory and enter `docker-compose up --build -d`. The --build parameter tells Docker Compose to rebuild our docker instance; Docker has good file change detection and file caching, and as such the --build command should almost never force a full redownload/rebuild of our project, instead only updating the relevant stage(s) of the build process.

You (probably) haven't placed anything for your application to actually *serve* in response to any requests yet, which is where the next section of this guide comes into play.

## Files and folders
By default, your docker instance will serve files and folders from `/var/Flask_Persistent/frontend`; meaning that within your docker instance, Flask will look for files and folders within that directory. You can access this same directory on your machine by finding out where Docker stores persistent volumes on your OS, and adding files/folders as necessary; any changes, either from within Docker or from your machine, are reflected immediately on either side.

Note that you will most likely need to update Flask to, for example, serve different files for different routes. A full explanation of the operation of Flask is outside the scope of this readme, but you must be aware that **any changes to the Flask python file will require a docker rebuild.**

If, for example, you updated flaskFile.py to serve a new route, you must save your changes, and then cd into the project root directory and run the following:

* `docker-compose down` (assuming docker_flask_web was already running)
* `docker-compose up --build -d` (rebuild to reflect changes)

## Stepping into Docker shell
You can step into your running Docker instance through a Docker-provided shell interface, allowing you to change or view files/folders as you so wish.
To do so:

1. Make sure your docker instance is running.
2. Run `docker ps` and copy your container's ID
3. Enter `docker exec -it <CONTAINER ID> sh`, which launches a shell in your docker instance
4. Do whatever you want to do in your shell; e.g `pwd` to see your current directory (by default, `/var/www/apache-flask`); or change directories into your docker volume and tinker with files to observe how changes are reflected on your dev machines' volume directory (by default, run `cd /var/Flask_Persistent`).
5. Exit the shell by inputting `CTRL+P` followed by `CTRL+Q`

Note that while you can edit any files you so desire within a running docker instance via the shell, these changes will not persist upon restarting your instance; only changes carried out in the shared docker volume will persist upon restarting/rebuilding the project.
