FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8 

RUN apk update &&\
    apk --no-cache add build-base gcc gfortran linux-headers pcre-dev

COPY ./app /app
COPY ./uwsgi_flask_nginx/uwsgi_timeout.conf /etc/nginx/conf.d/
COPY ./uwsgi_flask_nginx/nginx.conf /etc/nginx/
COPY ./uwsgi_flask_nginx/supervisord/supervisord.ini /etc/supervisor.d/

RUN cd /app &&\
    pip install -r requirements.txt &&\
    mkdir -p /var/log/supervisor &&\
    rm requirements.txt

WORKDIR /app
