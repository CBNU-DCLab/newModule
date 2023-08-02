FROM python:3.8.17


COPY .  /app
WORKDIR /app/newtest

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
RUN ["apt-get", "-y", "update"]
RUN ["apt-get", "install", "-y", "libpython3-dev", "default-libmysqlclient-dev", "gcc", "openssl","gnutls-bin"]
RUN pip install gunicorn
RUN pip install django
