#!/bin/sh

if [ ! -f ./bootstrap.py ]
then
 curl http://python-distribute.org/bootstrap.py -o ./bootstrap.py
fi

# Возникли проблемы с установкой (или патчингом, я не понял). Пришлось запускать скрипт от рута и потом делать chown baden:baden -R *

python ./bootstrap.py --distribute
# python bootstrap.py --distribute
#buildout init
