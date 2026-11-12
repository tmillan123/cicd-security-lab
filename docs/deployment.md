
# Deployment – Cloud-Native Workload Security Lab

## 1. Deployment Overview

This document describes the deployment and configuration
approach for the Cloud-Native Workload Security Engineering Lab.

The laboratory is hosted on an Ubuntu Linux virtual machine
running on VMware Workstation.

The deployment architecture uses Docker, Kubernetes (kind),
Helm, and security monitoring components to provide a
controlled environment for workload security engineering.

The deployment objectives are to:

- Establish a reproducible Kubernetes environment.
- Deploy representative containerized workloads.
- Install runtime security monitoring capabilities.
- Configure centralized logging and observability.
- Support automated security validation through CI/CD.
- Provide repeatable verification and troubleshooting procedures.

Detailed architectural design decisions are documented in
[Architecture](architecture.md).

## 2. Deployment Environment

| Component | Technology | Purpose |
|-----------|------------|---------|
| Virtualization | VMware Workstation | Hosts the Ubuntu VM |
| Operating System | Ubuntu Linux | Laboratory execution environment |
| Container Runtime | Docker | Container execution and kind infrastructure |
| Kubernetes | kind | Local Kubernetes cluster |
| Cluster Administration | kubectl | Kubernetes resource management |
| Package Management | Helm | Kubernetes application deployment |
| Runtime Security | Falco | Runtime security detection |
| Log Aggregation | Grafana Loki | Centralized logging |
| Visualization | Grafana | Security monitoring and investigation |
| CI/CD | GitHub Actions | Automated validation |
| GitOps | Argo CD (planned) | Declarative deployment management |

## 3. Environment Prerequisites

The following components must be available before deploying
the security monitoring stack:

- Ubuntu Linux VM with sufficient CPU, memory, and storage.
- Docker Engine installed and operational.
- kind installed and accessible.
- kubectl configured to access the Kubernetes cluster.
- Helm installed.
- Git installed for repository management.
- Network connectivity for downloading required images
  and Helm charts.

### Verify Docker

```bash
docker version
docker ps
```

### Verify Kubernetes

```bash
kind get clusters
kubectl cluster-info
kubectl get nodes
```

### Verify Helm

```bash
helm version
helm list -A
```

These commands verify that the underlying deployment
dependencies are available.

## 4. Kubernetes Cluster Deployment

The laboratory uses a local Kubernetes cluster named
`laboratorio`, provisioned using kind.

### Create the Cluster

If the cluster does not already exist:

```bash
kind create cluster --name laboratorio
```

### Select the Cluster Context

```bash
kubectl config use-context kind-laboratorio
```

### Verify Cluster Status

```bash
kubectl get nodes
kubectl get namespaces
kubectl get pods -A
```

The expected result is a functional Kubernetes control
plane with healthy system components.

**Note:** Cluster creation is a one-time provisioning
operation. An existing cluster should be verified rather
than recreated unnecessarily.

## 5. Application Workload Deployment

The laboratory uses representative application workloads
to support Kubernetes management and runtime security testing.

Example workloads include:

- `python-web`: Python-based containerized application.
- `nginx-demo`: NGINX-based application deployment.

These workloads provide controlled targets for security
engineering exercises.

### Verify Application Workloads

```bash
kubectl get deployments -A
kubectl get pods -A
kubectl get services -A
```

Inspect a specific workload:

```bash
kubectl describe pod <pod-name> -n <namespace>
```

The deployment should be considered successful when the
expected application Pods are running and their readiness
conditions are satisfied.

## 6. Runtime Security Deployment – Falco

Falco provides runtime threat detection for Kubernetes
workloads and supported host activity.

The laboratory uses Helm to manage Falco deployment.

### Verify Falco Deployment

```bash
helm list -n falco
kubectl get pods -n falco
kubectl get daemonsets -n falco
```

### Inspect Falco Logs

```bash
kubectl logs -n falco -l app.kubernetes.io/name=falco \
  --all-containers=true --tail=100
```

Falco deployment validation should confirm:

- The Helm release is present.
- The expected Falco Pods are running.
- Runtime instrumentation is functioning.
- Detection rules are loaded successfully.
- Security events can be generated and inspected.

Installing Falco does not, by itself, demonstrate that
the complete detection pipeline is operational.

## 7. Centralized Logging Deployment – Loki

Grafana Loki provides centralized log aggregation
and querying capabilities.

The laboratory uses Helm for deployment and configuration
management.

### Verify Loki Deployment

```bash
helm list -n monitoring
kubectl get pods -n monitoring
kubectl get services -n monitoring
```

### Inspect Loki Logs

```bash
kubectl logs -n monitoring \
  -l app.kubernetes.io/name=loki \
  --all-containers=true --tail=100
```

### Configuration Management

Deployment-specific settings should be maintained in
version-controlled configuration files where practical.

For example:

```text
monitoring/
    loki-values.yaml
```

The deployed Helm values and runtime settings should be
verified against the intended configuration.

Log ingestion must be tested independently of successful
Helm installation.

## 8. Security Observability – Grafana

Grafana is intended to provide dashboards, log exploration,
and investigation capabilities.

The deployment should establish connectivity between
Grafana and Loki through an appropriately configured
data source.

### Deployment Validation

The following checks should be performed:

1. Verify that Grafana is deployed and healthy.
2. Confirm access to the Grafana interface.
3. Configure and test the Loki data source.
4. Verify that security-relevant logs can be queried.
5. Validate dashboards or alerting rules where configured.

The observability capability should only be considered
operational once successful log retrieval is demonstrated.

## 9. CI/CD Deployment Validation

GitHub Actions provides automated execution of configured
validation workflows.

The intended deployment process separates application
testing from the promotion of changes into Kubernetes.

### CI Validation Stages

1. Source code is committed to Git.
2. Changes are pushed to GitHub.
3. GitHub Actions executes configured workflows.
4. Automated tests and security checks run.
5. Workflow results are reviewed before deployment.

### Verification

CI/CD validation should include evidence of:

- Successful workflow execution.
- Automated test results.
- Failure reporting when validation does not pass.
- Appropriate workflow permissions.

Automated deployment to Kubernetes should not be assumed
unless a corresponding deployment stage is implemented.

## 10. GitOps Deployment – Argo CD (Planned)

Argo CD is planned as a future enhancement to provide
declarative GitOps deployment management.

The intended model uses Git as the source of truth for
Kubernetes application configurations.

Planned capabilities include:

- Automated or controlled synchronization.
- Configuration drift detection.
- Version-controlled deployment definitions.
- Auditable deployment changes.

Argo CD is not part of the validated deployment baseline
until installed and tested.

## 11. Deployment Verification

A successful deployment requires verification at multiple
levels.

| Component | Verification |
|-----------|--------------|
| Docker | Docker daemon operational |
| Kubernetes | Nodes and system Pods healthy |
| Application workloads | Deployments and Pods ready |
| Helm | Expected releases installed |
| Falco | Runtime detection functioning |
| Loki | Logs successfully ingested |
| Grafana | Security logs available for querying |
| GitHub Actions | Automated workflows execute |
| Argo CD | Planned; not yet validated |

Useful verification commands:

```bash
docker ps
kind get clusters
kubectl get nodes
kubectl get pods -A
helm list -A
```

Any incomplete or failing components should be documented
with their observed status and troubleshooting evidence.

## 12. Operational Considerations

The environment runs inside a local virtual machine
and is not designed for production availability.

Operational considerations include:

- Docker daemon availability after VM restarts.
- Kubernetes cluster connectivity.
- Container resource consumption.
- Persistent storage requirements.
- Helm release configuration management.
- Log storage and retention.
- Recovery from failed deployments.

The laboratory supports controlled experimentation,
and deployment changes should be validated before
being documented as operational.

## 13. Deployment Evidence

Deployment verification should be supported by
reproducible command output and relevant screenshots.

Evidence may include:

- Kubernetes node and Pod status.
- Helm release information.
- Falco detection events.
- Loki log ingestion.
- Grafana queries and dashboards.
- GitHub Actions workflow results.

Supporting evidence is maintained in the
[evidence directory](../evidence/).

The objective is to demonstrate not only that security
technologies can be deployed, but that their operation
can be independently verified.
