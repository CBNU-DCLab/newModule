FROM ubuntu:latest


COPY .  /app
WORKDIR /app/newtest
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until
RUN ["apt-get", "-y", "update"]
RUN ["apt-get", "install", "-y", "python3","libpython3-dev", "default-libmysqlclient-dev", "gcc", "openssl","gnutls-bin","--fix-missing"]
RUN pip install gunicorn
RUN pip install django
