# Docker_Flask - Development environment
A dockerised Flask/Apache instance complete with WSGI configuration, running Flask 2.0 on Python 3. This readme is aimed towards those who may never have used Docker before, and so spells out steps/procedures some might fight elementary or obvious.

## NOTE
This is the **development environment** version of this project; that means it's intended for running on a developer's machine, with the intent of replicating the server environment docker as close as possible for easy deployment. If you're looking for the server instance, please look at the branch **main** in this repository; **main** and **dev_build** maintain feature parity, but the intricacies of replicating a HTTPS/SSL environment on a local environment necessitate some extra setup in the dev_build branch.



## Getting started

### How it works
In essence, we are using Docker to spin up a container that runs a Flask backend behind an Apache server. This allows us to spin up an exact replica of our desired project on any machine, meaning that anything achieved on a developer's machine should immediately and effortlessly translate to our production server when we push our changes. 

Where the two environments differ is that our server instance, a UCD Virtual Machine, has a URL and (potentially/eventually), a HTTPS SSL cert. We can't simply copy-paste that setup to a local machine, as SSL certs are tied to domain names (mostly), and we're developing across multiple different developer machines; so the dev build employs some further setup to use self-issued SSL certs, that allow us to develop on a HTTPS environment much like our production server has (will have).

In both cases, we are utilise persistent docker volumes that allow for live changes of the site content without rebuilding the docker container.

### What we'll be doing
If on Windows, we'll need [Windows Subsystem for Linux 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10). This effectively runs a Linux distro under Windows; Docker utilises this for our virtualisation, and it also lets us install an Ubuntu distro so that we can develop in a Linux environment from within Windows.

First, we'll clone this repository on our local machine so that we have all the files docker needs. Then we'll need to modify our hosts file so that requests to localhost and 127.0.0.1 are redirected to our fake SSL site name, "dev.local". This is necessary because our self-signed SSL cert is for this fake domain. 

Then we'll build our docker container. This will create a folder on our machine that our docker container will store and read persistent files from; we then add our Flask and frontend files (html, js, css etc.) here, so that Docker can start our flask backend and server our frontend files. We can then modify the files in this folder at will, and our docker container will reflect these changes automatically.

### What you'll need
* Docker + Docker Compose (latest versions)
   
   N.B: For Windows specifically, use the [Docker for WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/)
* ~650MB of storage space
* Access to a system with a CPU capable of virtualisation
* Access to your `hosts` file
* VSCode, for Windows remote development.
* A WSL2 Linux distro; I reccomend Ubuntu from the Windows store.

## Setup and basic start/stop commands
Having installed Docker and Docker Compose, follow these steps:

1. Clone/download this repository into a folder of your choice.
2. Modify your hosts file with the following: `127.0.0.1 dev.local`. This redirects all requests to 127.0.0.1 to "dev.local", our fake self-signed SSL cert site.
4. In the root directory (Docker_Flask, unless you've renamed the folder), run the following command:
   
   `docker-compose up --build -d`
3. Docker compose will now build our instance, and upon completing, you should be able to access our server through "localhost", and be automatically redirect to a HTTPS version of the site.
4. Check to see if our application is running by typing `docker ps`; if you need to kill the server, type `docker kill <CONTAINER ID>`, or use `docker stop <CONTAINER ID>` to issue a stop command that gives applications time to cease operations first. 
5. To restart your docker compose file, make sure you're in the root directory and enter `docker-compose up --build -d`. The --build parameter tells Docker Compose to rebuild our docker instance; Docker has good file change detection and file caching, and as such the --build command should almost never force a full redownload/rebuild of our project, instead only updating the relevant stage(s) of the build process.

You (probably) haven't placed anything for your application to actually *serve* in response to any requests yet, which is where the next section of this guide comes into play.

## Files and folders
By default, your docker instance will serve files and folders from its internal docker-container location, `/var/Flask_Persistent/frontend`; meaning that within your docker instance, Flask will look for files and folders within that directory. You can access this directory by stepping into Docker shell; or by accessing the underlying persistent volume folder location on the host machine.

On Windows using WSL2, the default folder location for the persistent volume created by our docker compose file is 

`\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_flask_persistent-data\_data`

Note that you will most likely need to update Flask to, for example, serve different files for different routes, depending on your site structure/layout.

As of a recent update, Flask and it's WSGI partner app are now stored in the persistent volume. We're now ready to actually add our Flask backend and served frontend files. We clone our frontend repository into the persistent folder (`......\docker\volumes\docker_flask_persistent-data\_data`), so that any changes we make to our frontend can both be read by Docker and pushed to Github.

Enter the following git command in your git terminal to clone our frontend section to this folder, without creating a parent folder:

`git clone git@github.com:Team10UCD/Frontend.git .` 

Your persistent volume folder should now look like this:

![image](https://user-images.githubusercontent.com/59771183/122412121-38753880-cf7d-11eb-92c7-3cf3ca8f42e4.png)

You'll probably have to restart your docker container now that we have files in the right location.
With this setup, we can now change Flask/Python backend elements, as well as frontend files, on the fly. After changing or adding any files (Python or otherwise), you **must touch or otherwise change the .wsgi file**; e.g `touch flaskFile.py`, in the `flask` folder.

This is because Apache will reload all served content when it detects a change to our .wsgi interface file; the touch command achieves this by updating the last-edited timestamp on the file, allowing our server to reflect changes without restarting the Flask server or rebuilding the docker instance. Please refrain from actually adding/removing content from the .wsgi file unless you're absolutely certain you know what you're doing.

There are situations where rebuilding the docker container may be necessary. If, for example, you modify an underlying Docker file (one of the core docker configs), you must save your changes, and then cd into the project root directory and run the following:

* `docker-compose down` (assuming docker_flask_web was already running)
* `docker-compose up --build -d` (rebuild to reflect changes)

## Developing under Windows
To make sure we don't introduce any Windows-specific issues when we're developing on a Windows-based machine, we'll be using VS Code with the remote development plugin, and a WSL2 distro like Ubuntu. In short, VS Code will actually host a server in our WSL2 Ubuntu distro, and we'll be remote-developing in a Linux environment from Windows, using VS Code as our editor.

This means that all of our e.g Python modules, or node packages, or file structures etc. will be developed and linted in a Linux environment. In short, developing our frontend files using VSCode through WSL2 means that we're developing our frontend in a Linux environment, without needing a VM.

Please see [this guide](https://code.visualstudio.com/blogs/2019/09/03/wsl2) for setting up the remote development plugin in VS Code. Next time you start up VS Code, the bottom left of the program should have a green icon; you should then be able to click on it and select which WSL2 Distro you'd like to remote-develop with; select Ubuntu, and then start/edit our files in a folder location within that WSL2 distro. This means that when we build our output, or use a built-in dev preview server ala vue, everything will be running under Linux. 

## Why all this setup?
To start a project in VSCode, we would select our Ubuntu distro in VS Code to initate a remote development session. We then navigate to our folder of choosing to start a project; `/home` is a good starting point. We make a new directory with `mkdir Vue` if, for example, starting a Vue.js project; then we proceed to develop the project under WSL2 through VSCode. This means that when Vue.js starts a dev server to show our work, it'll still open our desktop browser and reflect our changes as usual; but all of our changes and work will be done under Linux, for a Linux output.

The big reason we go through all this effort, VSCode or not, is that by using this Linux-based setup, and with our docker dev server running in the background, **we'll be able to access localhost-based server backends just like our production environment has**.

In other words, this lets us develop a Vue.js application with Vue's native development preview server, while still accessing Flask data and functionality from localhost/127.0.0.1. This means we can develop our frontend with full testing against a backend, and all of our frontend references to localhost will work as expected when pushed to our public server, as our pushed files will be looking at "localhost" on our production server.

**Note**: Due to the pecularities of how Windows manages WSL distro install mounting, it is currently necessary to copy over any finalised files from our Ubuntu WSL2 location to our persistent docker volume location.
For example:
Starting a WSL2 Ubuntu Vue.js project in `\\wsl$\Ubuntu\home\Vue` , and building the project to `\\wsl$\Ubuntu\home\Vue\dist`, would necessitate copying the output from the dist folder to `\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_flask_persistent-data\_data`


## Stepping into Docker shell
You can step into your running Docker instance through a Docker-provided shell interface, allowing you to change or view files/folders as you so wish.
To do so:

1. Make sure your docker instance is running.
2. Run `docker ps` and copy your container's ID
3. Enter `docker exec -it <CONTAINER ID> sh`, which launches a shell in your docker instance
4. Do whatever you want to do in your shell; e.g `pwd` to see your current directory (by default, `/var/www/apache-flask`); or change directories into your docker volume and tinker with files to observe how changes are reflected on your dev machines' volume directory (by default, run `cd /var/Flask_Persistent`).
5. Exit the shell by inputting `CTRL+P` followed by `CTRL+Q`

Note that while you can edit any files you so desire within a running docker instance via the shell, these changes will not persist upon restarting your instance; only changes carried out in the shared docker volume will persist upon restarting/rebuilding the project.

## Default config/folder locations
**N.B**: this section is more of a reference on file locations than a suggestion to go changing anything. Please don't change folder structures without consulting with the rest of the team; it *will* break something, somewhere.

----

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
