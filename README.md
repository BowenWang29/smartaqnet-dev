# smartaqnet-dev
Docker based smartaqnet-dev environment.
## FROST-Server-GUI
An implementation of the SensorthingsAPI implemented by [FraunhoferIOSB/FROST-Server](https://github.com/FraunhoferIOSB/FROST-Server).
## FROST-Server-Database
Postgresql database + postgis + [wale](https://github.com/wal-e/wal-e) installed. The container uses postgresql database with postgis plugin to store data for FROST-Server. It features three different types of data backup, more information is found in the wiki page of the project.
## Fast data dev
Kafka image implemented by [Landoop](https://github.com/Landoop/fast-data-dev). It's an all-in-one Apache Docker image including Zookeeper, Kafka Distribution from Confluent,a convenient open source GUI for Kafka, Kafka Connect, Schema Registry and some other tools.
## Scripts
Quick reset and quick start of FROST-Server, Fast-data-dev and so on.
