#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "Fail. This script must be run as root." 1>&2
   exit 1
fi

# depend
apt-get install libpcre3-dev

# clone the project
git clone http://github.com/wandenberg/nginx-push-stream-module.git
NGINX_PUSH_STREAM_MODULE_PATH=$PWD/nginx-push-stream-module
cd nginx-push-stream-module

# build with 1.1.x, 1.0.x, 0.9.x, 0.8.x series
./build.sh master 1.1.15
cd build/nginx-1.1.15

exit 1

# install and finish
#make install
checkinstall

# check
#sudo /usr/local/nginx/sbin/nginx -v

#        nginx version: nginx/1.1.15

# test configuration
# sudo /usr/local/nginx/sbin/nginx -c $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf -t
#        the configuration file $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf syntax is ok
#        configuration file $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf test is successful

# run
# sudo /usr/local/nginx/sbin/nginx -c $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf
