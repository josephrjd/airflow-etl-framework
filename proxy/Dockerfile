FROM haproxy:1.8-alpine

ENV TIMEZONE="Asia/Dubai"

RUN apk add tzdata

RUN cp /usr/share/zoneinfo/${TIMEZONE} /etc/localtime && \
    echo ${TIMEZONE} >  /etc/timezone

RUN apk del tzdata

RUN set -x && \
 apk upgrade --update &&  \
 apk add bash ca-certificates rsyslog &&  \
 mkdir -p /etc/rsyslog.d/ && \
 touch /var/log/haproxy.log && \
 ln -sf /dev/stdout /var/log/haproxy.log

# Include our configurations (`./etc` contains the files that we'd
# need to have in the `/etc` of the container).
ADD ./etc/ /etc/

# Include our custom entrypoint that will the the job of lifting
# rsyslog alongside haproxy.
ADD ./entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint

# Set our custom entrypoint as the image's default entrypoint
ENTRYPOINT [ "entrypoint" ]

# Make haproxy use the default configuration file
CMD [ "-f", "/etc/haproxy.cfg" ]
