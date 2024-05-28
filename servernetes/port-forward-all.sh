#!/bin/bash

BASE_PORT=7777
PORT_INCREMENT=0
SERVICES=$(kubectl get services -n servernetes -l app=servernetes -o jsonpath='{.items[*].metadata.name}')
PROCESS_IDS=$(ps aux | grep "kubectl port-forward" | grep :7777 | awk '{print $2}')
for PROCESS_ID in $PROCESS_IDS; do
    kill "$PROCESS_ID"
done
for SERVICE in $SERVICES; do
    echo "Port forwarding $SERVICE to localhost:$PORT"
    PORT=$((BASE_PORT + PORT_INCREMENT))
    kubectl port-forward -n servernetes "service/$SERVICE" $PORT:7777 &
    PORT_INCREMENT=$((PORT_INCREMENT + 1))
done