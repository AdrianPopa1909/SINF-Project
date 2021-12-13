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
    docker stack deploy --compose-file stack.yml $STACK_NAME
}

function stop_docker() {
    docker stack rm $STACK_NAME
    docker image rm --force http_server:latest
    docker volume rm ${STACK_NAME}_db_data
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



