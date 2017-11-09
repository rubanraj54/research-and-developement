#!/bin/bash

#initialization

IMAGE_NAME="neo-robot:latest"
DEFAULT_PORT_NEO4J=7474
DEFAULT_PORT_NEO4J_BOLT=7687
COORDINATION_INSTANCE_PORT=5001
DATA_PORT=6001
INITIAL_HOSTS=""
DOCKER_FILE_NAME="docker-compose-neo-robots.yml"
CONTAINER_NAME="neorobot"


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


for (( i = 1; i <= $DEFAULT_NUMBER_OF_ROBOTS; i++ )); do
  INITIAL_HOSTS="$INITIAL_HOSTS $CONTAINER_NAME$i:$COORDINATION_INSTANCE_PORT,"
done

for ((i=1;i<=$DEFAULT_NUMBER_OF_ROBOTS;i++));
do
  echo -e "  $CONTAINER_NAME$i:" >> $DOCKER_FILE_NAME
  echo -e "    image: $IMAGE_NAME" >> $DOCKER_FILE_NAME
  echo -e "    ports:" >> $DOCKER_FILE_NAME
  echo -e "      - $((DEFAULT_PORT_NEO4J+i)):$DEFAULT_PORT_NEO4J" >> $DOCKER_FILE_NAME
  echo -e "      - $((DEFAULT_PORT_NEO4J_BOLT+i)):$DEFAULT_PORT_NEO4J_BOLT" >> $DOCKER_FILE_NAME
  echo -e "    volumes:" >> $DOCKER_FILE_NAME
  echo -e "      - \$HOME/neo4j-enterprise/logs$i:/logs" >> $DOCKER_FILE_NAME
  echo -e "      - \$HOME/neo4j-enterprise/data$i:/data" >> $DOCKER_FILE_NAME
  echo -e "      - \$HOME/neo4j-enterprise/tmp$i:/var/tmp/" >> $DOCKER_FILE_NAME
  echo -e "      - \$PWD/events:/events" >> $DOCKER_FILE_NAME
  echo -e "    hostname: $CONTAINER_NAME$i" >> $DOCKER_FILE_NAME
  echo -e "    networks:" >> $DOCKER_FILE_NAME
  echo -e "      - cluster" >> $DOCKER_FILE_NAME
  echo -e "    environment:" >> $DOCKER_FILE_NAME
  echo -e "      - NEO4J_dbms_mode=HA" >> $DOCKER_FILE_NAME
  echo -e "      - NEO4J_ha_serverId=$i" >> $DOCKER_FILE_NAME
  echo -e "      - NEO4J_ha_host_coordination=$CONTAINER_NAME$i:$COORDINATION_INSTANCE_PORT" >> $DOCKER_FILE_NAME
  echo -e "      - NEO4J_ha_host_data=$CONTAINER_NAME$i:$DATA_PORT" >> $DOCKER_FILE_NAME
  echo -e "      - NEO4J_ha_initialHosts=$INITIAL_HOSTS" >> $DOCKER_FILE_NAME
  echo -e "      - NEO4J_dbms_memory_heap_maxSize=2G" >> $DOCKER_FILE_NAME
  if (( $i > 1 )); then
    echo -e "    depends_on:" >> $DOCKER_FILE_NAME
    echo -e "      - $CONTAINER_NAME$((i-1))" >> $DOCKER_FILE_NAME
  fi
done
echo "networks:" >> $DOCKER_FILE_NAME
echo "  cluster:" >> $DOCKER_FILE_NAME
echo "    driver: bridge" >> $DOCKER_FILE_NAME

docker-compose -f $DOCKER_FILE_NAME up
