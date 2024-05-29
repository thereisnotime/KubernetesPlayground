# servernetes

What if you run your code as "serverless" functions, but on your own Kubernetes cluster?

Even compiled languages like Rust and Typescript, without having to worry about the pipelines (not very useful though).

What is the use case? I don't know yet, but it's fun to play with.

Interesting things to note:

- You can use configMaps as libraries to share between pods

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
bash ../port-forward-all.sh
```

Deploy All:

```bash
bash ../deploy-all.sh
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
}' http://localhost:7777/
```

Run Benchmark (make sure that you did `pip3 install -r requirements.txt`):

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
$ python3 benchmark.py 500
+------+------------+-----------------------+-----------------------+-----------------------+-----------------+---------------------+-----------------------+
| Port |  Language  | Max Response Time (s) | Min Response Time (s) | Avg Response Time (s) | Total Time (ms) | Total Requests Sent | Total Failed Requests |
+------+------------+-----------------------+-----------------------+-----------------------+-----------------+---------------------+-----------------------+
| 7778 |   Golang   |         0.0427        |         0.0051        |         0.0174        |     8710.47     |         500         |           0           |
| 7779 |   Python   |         0.0495        |         0.0055        |         0.0180        |     8991.95     |         500         |           0           |
| 7780 |    Rust    |         0.0657        |         0.0052        |         0.0177        |     8830.51     |         500         |           0           |
| 7781 | TypeScript |         0.0441        |         0.0058        |         0.0179        |     8964.82     |         500         |           0           |
+------+------------+-----------------------+-----------------------+-----------------------+-----------------+---------------------+-----------------------+
```

## Todo

- [ ] Fix Zig.
- [ ] Add Ruby.
- [ ] Fix Java.
- [ ] Fix Elixir.
- [ ] Add benchmark for buildtime.
- [ ] Add PHP.