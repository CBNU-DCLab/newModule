FROM python:3.8.10


COPY .  /app
WORKDIR /app/newtest

RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until
RUN ["apt-get", "-y", "update"]
RUN ["apt-get", "install", "-y", "libpython3-dev", "default-libmysqlclient-dev", "gcc", "openssl","gnutls-bin"]
RUN pip install gunicorn
RUN pip install django
