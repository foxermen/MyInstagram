#!/bin/bash

NAME=MyInstagram
NEW_NAME=MyInstagram1
HOMEDIR=/home/foxermen/PythonProjects
DJANGODIR=${HOMEDIR}/${NAME}
SOCKFILE=/tmp/${NEW_NAME}.sock
# Три рабочих процесса на 1 ядро процессора
NUM_WORKERS=3
DJANGO_WSGI_MODULE=${NAME}.wsgi
GUNICORN=/home/foxermen/PythonProjects/venv/bin/gunicorn

cd $DJANGODIR
source ${HOMEDIR}/venv/bin/activate

# Если по какой-то причине директории с SOCKFILE не существует -- создаем её
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Запускаем наш Django-проект
exec ${GUNICORN} ${DJANGO_WSGI_MODULE}:application \
  --workers $NUM_WORKERS \
  --bind unix:${SOCKFILE} \
