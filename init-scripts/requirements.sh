#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "Fail. This script must be run as root." 1>&2
   exit 1
fi

pip install -r requirements.txt
