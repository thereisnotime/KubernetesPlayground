#!/bin/bash

kubectl create namespace servernetes
kubectl create secret generic secret-url --from-literal=SECRET_URL=https://myreallysecretwebhooksomewhere.org/ -n servernetes

for dir in test-*; do
    echo "Deploying $dir"
    kubectl delete -f "$dir/manifest.yaml" -n servernetes; kubectl apply -f "$dir/manifest.yaml" -n servernetes
done
