## Prerequisites
* [Docker Compose](https://docs.docker.com/compose/)


## Quickstart
### Jaeger testing
1. run the `docker-compose build && docker-compose up -d` command
1. send several requests to the `hello` endpoint, i.e. via curl `curl -X POST http://127.0.0.1:9990/hello/`
1. go to the jaeger UI on `http://localhost:16686/` and discover some traces

### Manual span testing
run the `python opentelemetry_pycon/span_cli.py` and follow CLI instructions, you will see opentelemetry data after each "request"


## K8s example
See `k8s/collector-example.yaml` for k8s deployment example. You can just apply it via kubectl or other methods.
