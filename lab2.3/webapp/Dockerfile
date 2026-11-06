FROM python:3.15-rc-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chown nobody:nogroup /app
RUN apt update
RUN apt -y install curl

COPY --chown=nobody:nogroup server.py ./

ENV PORT=${PORT}

CMD ["python","server.py"]
