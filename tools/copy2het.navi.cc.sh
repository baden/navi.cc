#!/bin/bash

echo Копирование проекта на сервер.

# nice -n +17 rsync -avz /backup/arch/ user2@Server2_IP:/hdd2/get/

#SRC=/backup/arch/
SRC=..
DST=baden@het.navi.cc:~/new.navi.cc

rsync -avz $SRC/src/www/_public/ $DST/www/
rsync -avz $SRC/etc/gsmcontrol.org/ $DST/etc/
rsync -avz $SRC/src/api/ $DST/api/ --exclude 'misc'
rsync -avz $SRC/src/channel/ $DST/channel/ --exclude 'misc'

exit

rsync -avz $SRC/bin $DST
rsync -avz $SRC/contrib $DST
rsync -avz $SRC/logs $DST
# ls $SRC/clients/android/magnum/bin/MagnuM.apk
# rsync -avz $SRC/clients/android/magnum/bin/MagnuM.apk $DST/www/apk/
