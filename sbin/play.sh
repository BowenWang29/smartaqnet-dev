#! /bin/bash
echo $smartaqnethome
if test -z "$smartaqnethome"
then echo "export smartaqnethome=smartaqnet-dev01.teco.edu" >/etc/environment
fi
echo $smartaqnethome
