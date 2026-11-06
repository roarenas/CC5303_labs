FROM alpine:3.24.2
WORKDIR /tmp
ENV URL=${URL}
RUN apk update
RUN apk add curl bind-tools jq
RUN cat > test.sh <<EOF
#!/bin/sh
MY_NAME=\`hostname\`
MY_LOG_PATH=/tmp/log
MY_LOG_FILE=\$MY_LOG_PATH/log.txt

if [ ! -d \$MY_LOG_PATH ]; then
  mkdir -p \$MY_LOG_PATH
fi

while true; do
  echo " -- \$MY_NAME " >>\$MY_LOG_FILE
  echo -n " -- \$MY_NAME " >>\$MY_LOG_FILE
  echo "URL \$URL"
  DATA=\`curl -s \$URL 2>&1\`
  STATUS=\`echo \$DATA|jq -r ".status"\`
  echo "-\$STATUS-"
  if [ "a\$STATUS" = "aok" ];then
    SLEEP=\`echo \$DATA|jq -r ".message"\`
  else
    SLEEP=99
  fi
  echo " \$SLEEP" >> \$MY_LOG_FILE
  sleep 0.\$SLEEP
done

EOF
RUN sed "s/\r$//" test.sh
RUN chmod 755 test.sh

CMD ["./test.sh"]