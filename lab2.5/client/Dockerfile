FROM alpine:3.24.2
WORKDIR /tmp
ENV URL=${URL}
RUN apk update
RUN apk add curl bind-tools
RUN cat > test.sh <<EOF
#!/bin/sh -x
MY_NAME=\`hostname\`
MY_LOG_PATH=/tmp/log
MY_LOG_FILE=\$MY_LOG_PATH/log.txt

if [ ! -d \$MY_LOG_PATH ]; then
  mkdir -p \$MY_LOG_PATH
fi

while true; do
  echo " -- \$MY_NAME " >>\$MY_LOG_FILE
  echo -n " -- \$MY_NAME " >>\$MY_LOG_FILE
  SLEEP=\`curl -s \$URL 2>&1| sed -n "s/.*random_number\":\([0-9]*\).*/\1/p"\`
  echo " \$SLEEP" >> \$MY_LOG_FILE
  sleep 0.\$SLEEP
done

EOF
RUN sed "s/\r$//" test.sh
RUN chmod 755 test.sh

CMD ["./test.sh"]