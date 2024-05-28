# servernetes

What if you run your code as "serverless" functions, but on your own Kubernetes cluster?

Even compiled languages like Rust and Typescript, without having to worry about the pipelines (not very useful though).

## Usage

First `cd` into the folder of the language you want to use, then:

Create a namespace, an example secret for our function:

```bash
kubectl create namespace servernetes
kubectl create secret generic secret-url --from-literal=SECRET_URL=https://myreallysecretwebhooksomewhere.org/ -n servernetes
```

Apply with kubectl:

```bash
kubectl apply -f manifest.yaml -n servernetes
```

Develop:

```bash
kubectl delete -f manifest.yaml -n servernetes; kubectl apply -f manifest.yaml -n servernetes
```

Start Port Forward:

```bash
kubectl port-forward "svc/servernetes-$(pwd | awk -F'-' '{print $NF}')" 7777:7777 -n servernetes &
```

Stop Port Forward:

```bash
kill $(lsof -t -i:7777)
```

Port Forward All:

```bash
BASE_PORT=7777
PORT_INCREMENT=0
SERVICES=$(kubectl get services -n servernetes -l app=servernetes -o jsonpath='{.items[*].metadata.name}')
for SERVICE in $SERVICES; do
    echo "Port forwarding $SERVICE to localhost:$PORT"
    PORT=$((BASE_PORT + PORT_INCREMENT))
    kill $(lsof -t -i:$PORT)
    kubectl port-forward -n servernetes service/$SERVICE $PORT:7777 &
    PORT_INCREMENT=$((PORT_INCREMENT + 1))
done
```

Send a test request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "Random Name",
  "age": 30,
  "email": "random@example.com",
  "address": {
    "street": "123 Random St",
    "city": "Random City",
    "zip": "12345"
  },
  "preferences": {
    "likes": ["reading", "coding", "movies"],
    "dislikes": ["noise", "crowds"]
  }
}' http://localhost:7777
```

Run Benchmark:

```bash
python3 benchmark.py 100
```

Cleanup:

```bash
kubectl delete namespace servernetes
kill $(lsof -t -i:7777)
```

## Benchmarks

Some interesting results (keep in mind bad implementation for an API):

```bash
python3 benchmark.py 1000

+------+--------------------+-----------------------+-----------------------+-----------------------+---------------------+-----------------------+
| Port |      Language      | Max Response Time (s) | Min Response Time (s) | Avg Response Time (s) | Total Requests Sent | Total Failed Requests |
+------+--------------------+-----------------------+-----------------------+-----------------------+---------------------+-----------------------+
| 7777 |       Python       |         0.1351        |         0.0052        |         0.0554        |         1000        |           0           |
| 7778 |        Rust        |         0.1356        |         0.0073        |         0.0640        |         1000        |           0           |
| 7779 |     TypeScript     |         0.1406        |         0.0056        |         0.0469        |         1000        |           0           |
+------+--------------------+-----------------------+-----------------------+-----------------------+---------------------+-----------------------+
```
