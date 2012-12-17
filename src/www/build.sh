#!/bin/sh

yeoman build

sed -i 's/^http:\/\/localhost:3501\///' ./_public/manifest.appcache
sed -i '/manifest.appcache/d' ./_public/manifest.appcache

