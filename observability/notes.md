# Notes

- Observability means the ability of observing the infrastructure to be sure everything is ok. Three pillars:
1. What happened? (metrics)
2. Where did it happened? (traces)
3. Why? (Logs)

- There are the data that we need to detect and solve a problem in our infrastructure.

## LGTM Stack (Loki, Grafana, Tempo, Mimir)

- LGTM stack (Loki, Grafana, Tempo, Mimir) is the industry-standart open-source tech stack. It uses cost-effective object storage (s3 or MinIO) to handle massive scale


### Loki

- Instead of indexing every word of logs (like how Elasticsearch works), it only indexes metadata (labels) attached to the log. like app=payment-service, environment=production. Cost-effective

### Grafana

- Visualize everything. The dashboard. Not just LGTM stack, also Azure, SQL database in the same panel.

### Tempo

- Designed to make tracing affordable, by help of object storage. store %100 of traces, no sampling.

### Mimir

- long term storage backend for prometheus metrics.

## flow

1. Application (.NET eShop for example) generates data using OTel SDK.
2. OTel collector recieves all mixed data.
3. LTM part: Collector sees a log -> send to Loki
             Collector sees a trace => send to Tempo
             Collector sees a metric => send to Mimir
4. View all from grafana.

## What to do to Implement Observability?

- You already dockerized the app and have docker-compose.
- Add these to docker-compose: OpenTelemetry Collector, Loki, Tempo, Prometheus (Mimir actually), Grafana.
- Create config for OTel collector and mount it to OTel container.
- in the otel-collector-config.yaml, congi these: "Send Traces to tempo:4317", "Send Metrics to prometheus:9090", "Send Logs to loki:3100"
- launch grafana from the browser: localhost:3000. Add the data sources: http://loki:3100, http://tempo:3200, http://prometheus:9090 you can automate this by creating a datasources.yaml and mount it to   /etc/grafana/provisioning/datasources/ container path.
