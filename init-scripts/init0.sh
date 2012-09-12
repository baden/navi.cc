#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "Fail. This script must be run as root." 1>&2
   exit 1
fi

command_exists () {
    type "$1" &> /dev/null ;
}

init_update()
{
  echo "Update system..."
  apt-get update &> /dev/null
  apt-get upgrade -y &> /dev/null
}

init_base()
{
  echo "Base install..."
  # apt-get install mc python-pip -y
  apt-get install mc gcc python-setuptools python-software-properties libxml2-dev python-dev -y &> /dev/null
}


init_nginx()
{
  echo "Install nginx..."
  nginx=stable # use nginx=development for latest development version
  add-apt-repository ppa:nginx/$nginx
  apt-get update &> /dev/null
  apt-get install nginx -y &> /dev/null
  service nginx start
  update-rc.d nginx defaults
}

init_mongodb()
{
  echo "Install mongoDB..."
  # Предполагаем что используется Upstart, а не SysV.
  apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10 &> /dev/null
  echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen">/etc/apt/sources.list.d/10gen.list
  # deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen
  apt-get update &> /dev/null
  apt-get install mongodb-10gen -y &> /dev/null
}

init_rabbitmq()
{
  echo "Install rabbitmq-server"
  echo "deb http://www.rabbitmq.com/debian/ testing main">/etc/apt/sources.list.d/rabbitmq.list
  wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
  sudo apt-key add rabbitmq-signing-key-public.asc
  apt-get update &> /dev/null
  sudo apt-get install rabbitmq-server
}

init_update
init_base

# if ! command_exists nginx; then
if ! builtin type -p nginx &>/dev/null; then
  init_nginx
else
  echo "Skip nginx install."
fi

#if ! command_exists mongo; then
if ! builtin type -p mongo &>/dev/null; then
  init_mongodb
else
  echo "Skip mongoDB install."
fi

#rabbitmq-server
if ! builtin type -p rabbitmq-server &>/dev/null; then
  init_rabbitmq
else
  echo "Skip rabbitmq-server install."
fi

echo "All done OK."
echo "Edit /etc/mongodb.conf and uncomment and fix line: replSet = navicc"
echo "Add for debugging: rest = true"