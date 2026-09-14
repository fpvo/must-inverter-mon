#!/bin/sh
set -e

SER2NET_HOST="${SER2NET_HOST:-192.168.30.211}"
SER2NET_PORT="${SER2NET_PORT:-8003}"

rm -f /dev/ttyUSB0
socat -d -d pty,link=/dev/ttyUSB0,raw,mode=666 "tcp:${SER2NET_HOST}:${SER2NET_PORT}" &
SOCAT_PID=$!

for i in $(seq 1 20); do
  [ -e /dev/ttyUSB0 ] && break
  sleep 0.5
done

node server.js &
NODE_PID=$!

trap 'kill "$NODE_PID" "$SOCAT_PID" 2>/dev/null' TERM INT
wait "$NODE_PID"
EXIT_CODE=$?
kill "$SOCAT_PID" 2>/dev/null
exit "$EXIT_CODE"
