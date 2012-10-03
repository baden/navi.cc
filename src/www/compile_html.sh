#!/bin/sh

echo Compile htmls

node_modules/.bin/jade app/index.jade -w --pretty --out app/assets/
#node_modules/.bin/jade app/index.jade --pretty --out app/assets/

#./scripts/compile-html.sh

