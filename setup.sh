#!/bin/bash

function usage () {
    echo "usage: $0 [ -a|--action deploy|clean ]"
    exit 1
}

action=""
STACK_NAME=sinf

while [[ $# -ne 0 ]];
do
    case $1 in
    -a|--action)
        action=$2
        shift
        shift
        ;;
    *)
    echo "unknown option $1"
    usage
    ;;
    esac
done


function deploy_docker() {
    docker build -t http_server server
    docker build -t sinf_grafana grafana
    docker stack deploy --compose-file stack.yml $STACK_NAME
}

function stop_docker() {
    docker stack rm $STACK_NAME
    docker image rm --force http_server:latest
    docker image rm --force sinf_grafana:latest

    docker volume rm --force ${STACK_NAME}_elastic_search_data
    docker volume rm --force ${STACK_NAME}_grafana_data
    docker volume rm --force ${STACK_NAME}_grafana_etc
}


if [[ "$action" == "deploy" ]];
then
    deploy_docker
elif [[ "$action" == "clean" ]];
then
    stop_docker
else
    echo "action $action is not valid"
fi



