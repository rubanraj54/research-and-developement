#!/bin/bash

#initialization
# dont forget to use exact version number
IMAGE_NAME="orient-robot:latest"
DEFAULT_PORT_ORIENTDB=2424
DEFAULT_PORT_ORIENTDB_STUDIO=2480
COORDINATION_INSTANCE_PORT=5001
DATA_PORT=6001
INITIAL_HOSTS=""
DOCKER_FILE_NAME="docker-compose-orientdb-robots.yml"
CONTAINER_NAME="orientdbrobot"


if [[ $# -eq 0  ]]; then
  #statements
  DEFAULT_NUMBER_OF_ROBOTS=2
elif [[ $1 -lt 11 ]]; then
  DEFAULT_NUMBER_OF_ROBOTS=$1
else
  echo "Please enter robot number less than or equal to 10"
  exit 0
fi

# clean the docker-compose file before writing new content
echo -n "" > $DOCKER_FILE_NAME
echo -e "version: '3'\n" >> $DOCKER_FILE_NAME
echo "services:" >> $DOCKER_FILE_NAME

for ((i=1;i<=$DEFAULT_NUMBER_OF_ROBOTS;i++));
do
  echo -e "  $CONTAINER_NAME$i:" >> $DOCKER_FILE_NAME
  echo -e "    image: $IMAGE_NAME" >> $DOCKER_FILE_NAME
  echo -e "    ports:" >> $DOCKER_FILE_NAME
  echo -e "      - $((DEFAULT_PORT_ORIENTDB+(i-1))):$DEFAULT_PORT_ORIENTDB" >> $DOCKER_FILE_NAME
  echo -e "      - $((DEFAULT_PORT_ORIENTDB_STUDIO+(i-1))):$DEFAULT_PORT_ORIENTDB_STUDIO" >> $DOCKER_FILE_NAME
  echo -e "    volumes:" >> $DOCKER_FILE_NAME
  echo -e "      - \$HOME/orientdb/databases$i:/orientdb/databases" >> $DOCKER_FILE_NAME
  # echo -e "      - \$HOME/orientdb/config$i/default-distributed-db-config.json:/orientdb/config/default-distributed-db-config.json" >> $DOCKER_FILE_NAME
  echo -e "      - \$HOME/orientdb/backup$i:/orientdb/backup" >> $DOCKER_FILE_NAME
  echo -e "      - \$PWD/src:/src" >> $DOCKER_FILE_NAME
  echo -e "    environment:" >> $DOCKER_FILE_NAME
  echo -e "      - ORIENTDB_NODE_NAME=node$i" >> $DOCKER_FILE_NAME
  echo -e "      - ORIENTDB_ROOT_PASSWORD=admin" >> $DOCKER_FILE_NAME
  echo -e "    command: /orientdb/bin/server.sh  -Ddistributed=true" >> $DOCKER_FILE_NAME
  # if (( $i > 1 )); then
  #   echo -e "    depends_on:" >> $DOCKER_FILE_NAME
  #   echo -e "      - $CONTAINER_NAME$((i-1))" >> $DOCKER_FILE_NAME
  # fi
done

docker-compose -f $DOCKER_FILE_NAME up
