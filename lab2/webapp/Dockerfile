FROM python:3.15-rc-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chown nobody:nogroup /app

COPY --chown=nobody:nogroup server.py ./

ENV PORT=8000
EXPOSE 8000

CMD ["python","server.py"]
