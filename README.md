# Docker_Flask
A dockerised Flask/Apache instance complete with WSGI configuration
Partially based on https://github.com/carlostighe/apache-flask, but modified for Python 3 and mod_WSGI use

TODO:
Figure out support for Let's Encrypt
Create docker volume for static HTML files for frontend development, so that changes can be reflected instantly and not mandate a docker stop-start procedure
Organise/change file structure in "app"; see above

When in root folder, initialise container using docker compose with:

docker-compose up -d

Currently, to update any changes to files/folders within docker instance, you need to re-build the docker instance with 

docker-compose up --build -d

