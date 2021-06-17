# Docker_Flask - Production environment
A dockerised Flask/Apache instance complete with WSGI configuration, running Flask 2.0 on Python 3. This readme is aimed towards those who may never have used Docker before, and so spells out steps/procedures some might fight elementary or obvious.


## NOTE
This is the **production environment** version of this project; that means it's intended for deployment on a server that can/has been issued an SSL certificate by e.g LetsEncrypt. To facilitate local development, a parallel branch named **"dev_build"** is present in this repository; it maintains feature parity with this branch, but differs in setup to allow local development of HTTPS/SSL-based sites.

## Default config/folder locations
Note that modifying the folder locations provided in this repository may prove somewhat complex, as the same locations appear over several files due to the nature of configuring both Flask and Apache + mod_WSGI to serve files from a specified folder. 

By default, the Flask file ( `flaskFile.py` ) will reside in `/var/Flask_Persistent/`

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
2. Customise apache-flask.conf to reflect your server's domain name.
3. In the root directory (Docker_Flask, unless you've renamed the folder), run the following command:
   
   `docker-compose up -d`
3. Docker compose will now build our instance, and upon completing, you should be able to access your server through it's IP. 
4. Check to see if your application is running by typing `docker ps`; if you need to kill the server, type `docker kill <CONTAINER ID>`, or use `docker stop <CONTAINER ID>` to issue a stop command that gives applications time to cease operations first. 
5. To restart your docker compose file, make sure you're in the root directory and enter `docker-compose up --build -d`. The --build parameter tells Docker Compose to rebuild our docker instance; Docker has good file change detection and file caching, and as such the --build command should almost never force a full redownload/rebuild of our project, instead only updating the relevant stage(s) of the build process.

You (probably) haven't placed anything for your application to actually *serve* in response to any requests yet, which is where the next section of this guide comes into play.

## Files and folders
By default, your docker instance will serve files and folders from its internal docker-container location, `/var/Flask_Persistent/frontend`; meaning that within your docker instance, Flask will look for files and folders within that directory. You can access this directory by stepping into Docker shell; or by accessing the underlying persistent volume folder location on the host machine.

Note that you will most likely need to update Flask to, for example, serve different files for different routes, depending on your site structure/layout.

As of a recent update, Flask and it's WSGI partner app are now stored in the persistent volume. This allows for changing Flask/Python backend elements on the fly. After changing or adding any files (Python or otherwise), you **must touch or otherwise change the .wsgi file**; e.g `touch flaskFile.py`. This is because Apache will reload all served content when it detects a change to our .wsgi interface file; the touch command achieves this by updating the last-edited timestamp on the file, allowing our server to reflect changes without restarting the Flask server or rebuilding the docker instance.

If, for example, you modify an underlying Docker file (one of the core docker configs), you must save your changes, and then cd into the project root directory and run the following:

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
