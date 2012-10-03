#!/bin/bash

node_modules/.bin/jade app/index.jade --pretty --out app/assets/
node_modules/.bin/jade app/partials/ --pretty --out app/assets/partials/

#rm -R app/index.html
#rm -R app/partials/*.html/
