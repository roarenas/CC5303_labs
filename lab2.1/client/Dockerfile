FROM alpine:3.24.0
WORKDIR /tmp
RUN apk update
RUN apk add curl bind-tools
RUN cat > test.sh <<EOF
RUN mkdir -p /tmp/log
#!/bin/sh
MY_NAME=\`hostname\`
MY_LOG_FILE=/tmp/log/salida.log

echo -n "\$MY_NAME ">>\$MY_LOG_FILE;
curl -s http://webapp:8000/random 2>&1 >> \$MY_LOG_FILE;

EOF
RUN sed "s/\r$//" test.sh
RUN chmod 755 test.sh

CMD ["./test.sh"]