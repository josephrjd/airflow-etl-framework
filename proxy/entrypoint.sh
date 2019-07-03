#!/bin/bash

set -o errexit
set -o nounset

readonly RSYSLOG_PID="/var/run/rsyslogd.pid"

main() {
  start_rsyslogd
  start_lb "$@"
}

# make sure we have rsyslogd's pid file not
# created before
start_rsyslogd() {
  rm -f $RSYSLOG_PID
  echo "Running rsyslog"
  rsyslogd -n &
  echo "Rsyslog running..."
}

# Starts the load-balancer (haproxy) with
# whatever arguments we pass to it ("$@")
start_lb() {
  echo "Launching haproxy with args $@"
  exec haproxy "$@"
}

main "$@"
