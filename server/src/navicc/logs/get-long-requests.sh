#/bin/bash

# Поиск долгих запросов
grep '200 GET' ./server.log |  sed 's/ms/ ms/g' | awk '{ if ($9 > 100 ) print $p0'}
