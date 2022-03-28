#!/bin/bash

a=`curl -F 'file=@./browser/main.html' 127.0.0.1:3000`

wget localhost:3000/files/$a -O /dev/shm/$a

firefox /dev/shm/$a