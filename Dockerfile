FROM debian:buster
RUN apt-get update && apt-get install -y python3 python3-paho-mqtt python3-serial

COPY docker-entrypoint.sh /ultraheat/docker-entrypoint.sh
COPY t550.py /ultraheat/t550.py
CMD ["sh", "/ultraheat/docker-entrypoint.sh"]