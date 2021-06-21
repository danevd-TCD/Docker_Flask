FROM debian:latest

RUN apt-get update && apt-get install -y apache2 \
	libapache2-mod-wsgi-py3 \
	build-essential \
	python3 \
	python3-dev \
	python3-pip \
	nano \
  && apt-get clean \
  && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

#certbot python-based install
RUN apt update
RUN apt install -y python3 python3-venv libaugeas0
RUN python3 -m venv /opt/certbot/
RUN /opt/certbot/bin/pip install --upgrade pip
RUN /opt/certbot/bin/pip install certbot certbot-apache
RUN ln -s /opt/certbot/bin/certbot /usr/bin/certbot

#copy app requirements to the /var folder docker will use to store files
COPY ./app/requirements.txt /var/www/apache-flask/app/requirements.txt
RUN pip3 install -r /var/www/apache-flask/app/requirements.txt

COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
#COPY ./apache-flask-ssl.conf /etc/apache2/sites-available/apache-flask-ssl.conf
#RUN a2ensite apache-flask
#RUN a2ensite apache-flask-ssl
RUN a2enmod headers
RUN a2enmod rewrite
RUN a2enmod ssl

#copy wsgi file
#COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi

#main flask file
#COPY ./flaskFile.py /var/www/apache-flask/flaskFile.py
COPY ./app /var/www/apache-flask/app/

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

#link apache configuration to docker logs
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
	ln -sf /proc/self/fd/1 /var/log/apache2/error.log

EXPOSE 80
EXPOSE 443
#working directory for docker
WORKDIR /var/www/apache-flask

#CMD /usr/sbin/apache2ctl -D FOREGROUND ; sleep 5 ;certbot --apache --agree-tos --staging -q -d csi6220-4-vm1.ucd.ie --no-autorenew -m daniel.danev@ucdconnect.ie

ADD start.sh /
RUN chmod +x /start.sh
CMD ["/start.sh"]

#certbot python-based run
#RUN sleep 10
#RUN certbot --apache --agree-tos --staging -q -d csi6220-4-vm1.ucd.ie --no-autorenew -m daniel.danev@ucdconnect.ie
