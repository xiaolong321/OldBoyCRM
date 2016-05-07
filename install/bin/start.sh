#!/bin/bash
cd `dirname $0`
cd ..
cd ..
BIN_DIR=`pwd`
PYTHON=`which python`

PIDS=`ps aux |grep $BIN_DIR/manage.py |grep -v grep |awk '{print $2}'`
if [ -n "$PIDS" ]; then
    echo "ERROR: The manage.py already started!"
    echo "PID: $PIDS"
    exit 1
fi

nohup $PYTHON $BIN_DIR/manage.py runserver 0.0.0.0:8080 &