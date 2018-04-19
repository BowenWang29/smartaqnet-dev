#! /bin/bash
# Set up SensorThingsServerDocker
git clone https://github.com/image357/docker-SensorThingsServer.git Frost-Server
docker-compose -f ./Frost-Server/docker-compose.yml up --build -d
sleep 4m
docker-compose -f ./Frost-Server/docker-compose.yml exec database psql -U sensorthings -d sensorthings -c 'CREATE EXTENSION IF NOT EXISTS "postgis"' && \
docker-compose -f ./Frost-Server/docker-compose.yml exec database psql -U sensorthings -d sensorthings -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"' && \
curl -X POST http://localhost:8080/FROST-Server/DatabaseStatus
# Set up landoop and sftp
sleep 3m
docker-compose -f ./docker-compose.yml up --build -d
# Set up ST2SFTP
# Set up FrostFranz
sleep 3m
docker-compose -f ./FrostyFranz/docker-compose.yml up --build -d
