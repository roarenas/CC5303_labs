FROM python:3.15-rc-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chown nobody:nogroup /app
RUN apt update
RUN apt -y install curl socat


ENV HAPROXY_API_HOST = {HAPROXY_API_HOST}
ENV HAPROXY_API_PORT = {HAPROXY_API_PORT}
ENV BACKEND=${BACKEND}
ENV SERVER_PORT = {SERVER_PORT}

COPY --chown=nobody:nogroup server.py ./

#CMD ["/bin/sh", "-c", "esperamos..."]
#CMD ["/bin/sh", "-c", "sleep 5 && echo listo"]
#CMD ["/bin/sh", "-c", "export IP=\`hostname -I\`;echo \"experimental-mode on; add server $BACKEND/$HOSTNAME $IP:$PORT check port $PORT from mydefaults\" | socat stdio tcp:frontend:9999 && echo 'agregamos $HOSTNAME a backend $BACKEND"]
#CMD ["/bin/sh", "-c", "echo \"enable server $BACKEND/$HOSTNAME\" | socat stdio tcp:frontend:9999 && echo 'Activamos $HOSTNAME en backend $BACKEND"]


CMD ["python","server.py"]
