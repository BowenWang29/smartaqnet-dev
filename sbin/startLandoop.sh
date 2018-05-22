#! /bin/bash
if test -z "$smartaqnethome"
then echo "export smartaqnethome=localhost" > /etc/environment
fi
# Start landoop with heap size set to 3G
docker run --rm --net=host --name="frosty_landoop" \
-d -e CONNECT_HEAP=3G -e ADV_HOST=$smartaqnethome -e RUNTESTS=0 landoop/fast-data-dev
