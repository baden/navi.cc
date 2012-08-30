#!/bin/sh
if [[ $EUID -ne 0 ]]; then
   echo "Fail. This script must be run as root." 1>&2
   exit 1
fi

apt-get update
apt-get upgrade
apt-get install mc python-pip
nginx=stable # use nginx=development for latest development version
add-apt-repository ppa:nginx/$nginx
apt-get update
apt-get install nginx

echo "All done OK."
