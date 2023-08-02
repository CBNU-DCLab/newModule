FROM ubuntu:latest


COPY .  /app
WORKDIR /app/newtest
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until
RUN ["apt-get", "-y", "update"]
RUN ["apt-get", "install", "-y", "python3","libpython3-dev", "default-libmysqlclient-dev", "gcc", "openssl","gnutls-bin","python3-pip","--fix-missing"]
RUN pip3 install gunicorn
RUN pip3 install django
