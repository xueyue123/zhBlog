#!/bin/bash

cd /home/wang/blog1.1/
workon blog
uwsgi --ini project.ini &
