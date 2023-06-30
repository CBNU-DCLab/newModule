FROM python:3.8.10


COPY .  /app
WORKDIR /app/newtest

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.13.5/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

RUN ["apt-get", "-y", "update"]
RUN ["apt-get", "install", "-y", "libpython3-dev", "default-libmysqlclient-dev", "gcc", "openssl","gnutls-bin"]
RUN pip install gunicorn
RUN pip install django
