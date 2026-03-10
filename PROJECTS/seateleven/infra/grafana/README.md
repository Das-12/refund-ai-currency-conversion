# Grafana & Prometheus Monitoring Setup

This directory contains configurations for extending the monitoring capabilities of the cluster.

## PostgreSQL Monitoring

### 1. ServiceMonitor
The `postgres-servicemonitor.yaml` file defines how Prometheus Operator should discover and scrape metrics from the PostgreSQL Exporter.

**Key Requirements:**
- The exporter service must be in the `infra` namespace.
- The exporter service must have labels that match the `ServiceMonitor` selector (e.g., `app.kubernetes.io/name: postgres-exporter`).
- The Prometheus Operator must have the correct `release` label (e.g., `release: monitoring-kube-prometheus`).

### 2. Verification Steps
After applying a new `ServiceMonitor`, verify it in the Prometheus UI:
1. Navigate to **Status -> Targets**.
2. Look for the `postgres-exporter-monitor` target.
3. Ensure the status is **UP** (Green).

### 3. Grafana Dashboard
To visualize the metrics:
1. In Grafana, go to **Dashboards -> Import**.
2. Use ID `9628` (PostgreSQL Database) or `14114`.
3. Select the appropriate Prometheus datasource (e.g., `prometheus-1`).

## Troubleshooting
If "No Data" appears in Grafana:
- Check if the metrics are present in Prometheus by running a test query like `pg_up`.
- Ensure the **Instance** or **Job** variables in the Grafana dashboard are correctly selected.
- Verify service labels: `kubectl get svc -n infra --show-labels`.
