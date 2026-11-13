
# 02 – Helm Deployment and Validation

## 1. Objective

Demonstrate the use of Helm to deploy, configure,
manage, and validate applications running in a
Kubernetes environment.

The objectives of this exercise are to:

- Understand Helm charts and release management.
- Deploy Kubernetes applications using Helm.
- Manage application configuration through values files.
- Validate deployment status and workload health.
- Inspect deployment history for auditing and troubleshooting.
- Document reproducible deployment procedures.

## 2. Technology Overview

Helm is a package manager for Kubernetes.

It simplifies the management of Kubernetes
applications by packaging resources into reusable
deployment units called **charts**.

Key concepts:

| Concept | Description |
|---|---|
| Chart | Package of Kubernetes resource templates |
| Release | Installed instance of a Helm chart |
| Repository | Location from which charts can be obtained |
| values.yaml | Configuration supplied to chart templates |
| Revision | Version of an installed release |
| Rollback | Restoration of a previous release revision |

Helm provides deployment and release management
capabilities but does not, by itself, constitute
a CI/CD pipeline or a GitOps implementation.

## 3. Laboratory Environment

The deployment validation uses the following
environment:

| Component | Technology |
|---|---|
| Host | Ubuntu Linux VM running on VMware |
| Container runtime | Docker |
| Kubernetes | kind |
| Package manager | Helm |
| Configuration | YAML values files |
| Source control | Git and GitHub |

The Kubernetes cluster runs locally without
requiring a managed cloud Kubernetes service.

## 4. Helm Installation and Verification

Verify that Helm is installed and accessible:

```bash
helm version
```

Verify connectivity to the Kubernetes cluster:

```bash
kubectl cluster-info
kubectl get nodes
```

List installed Helm releases across all namespaces:

```bash
helm list -A
```

This provides visibility into applications managed
by Helm within the Kubernetes cluster.

## 5. Helm Deployment Configuration

Helm supports configuration customization through
values files and command-line parameters.

This laboratory includes the following
configuration file:

[monitoring/loki-values.yaml](../monitoring/loki-values.yaml)

The values file is used to customize the Loki
deployment for the local Kubernetes environment.

Configuration values can be supplied during
installation using:

```bash
helm install <release-name> <chart> \
  --namespace <namespace> \
  --create-namespace \
  -f <values-file>
```

Using version-controlled configuration files
improves deployment reproducibility and makes
configuration changes easier to review.

It is important to distinguish between:

- Configuration stored in Git
- The Helm chart being deployed
- The actual release installed in Kubernetes
- The resulting Kubernetes workload status

A successful Helm command does not necessarily
mean all deployed workloads are healthy.

## 6. Helm Release Management

### 6.1 List installed releases

```bash
helm list -A
```

This command displays information such as:

- Release name
- Kubernetes namespace
- Release revision
- Deployment status
- Chart version
- Application version

### 6.2 Inspect release status

```bash
helm status <release-name> \
  -n <namespace>
```

This provides information about a specific
Helm release.

### 6.3 Inspect release history

```bash
helm history <release-name> \
  -n <namespace>
```

Release history supports operational
troubleshooting and helps identify previous
deployment revisions.

### 6.4 Inspect deployment configuration

```bash
helm get values <release-name> \
  -n <namespace>
```

To inspect the computed values:

```bash
helm get values <release-name> \
  -n <namespace> -a
```

### 6.5 Upgrade a release

The following command illustrates a controlled
Helm upgrade:

```bash
helm upgrade <release-name> <chart> \
  -n <namespace> \
  -f <values-file>
```

An upgrade should be followed by validation of
the Helm release and Kubernetes workloads.

### 6.6 Rollback procedure

Helm supports rollback to a previous release
revision:

```bash
helm rollback <release-name> \
  <revision> -n <namespace>
```

**Note:** These upgrade and rollback commands
describe available operational procedures.
They should not be interpreted as completed
tests unless corresponding evidence is captured.

## 7. Kubernetes Deployment Validation

After deploying an application with Helm,
validate the underlying Kubernetes resources.

### 7.1 Inspect workloads

```bash
kubectl get pods -A
kubectl get deployments -A
kubectl get daemonsets -A
kubectl get statefulsets -A
```

### 7.2 Inspect deployment problems

```bash
kubectl describe pod <pod-name> \
  -n <namespace>
```

### 7.3 Inspect application logs

```bash
kubectl logs <pod-name> \
  -n <namespace>
```

### 7.4 Inspect Kubernetes events

```bash
kubectl get events -n <namespace> \
  --sort-by=.metadata.creationTimestamp
```

These checks help identify issues such as:

- Image pull failures
- Pending pods
- Container startup errors
- Resource constraints
- Failed readiness checks
- Configuration errors

## 8. Deployment Evidence

The following evidence files are maintained
separately from the implementation documentation.

### 8.1 Helm Release Inventory

[helm-releases.txt](../evidence/02-helm-deployment/helm-releases.txt)

Captures the inventory of installed Helm releases.

### 8.2 Helm Release History

[helm-history.txt](../evidence/02-helm-deployment/helm-history.txt)

Captures the revision history of a Helm release.

### 8.3 Kubernetes Deployment Status

[deployment-status.txt](../evidence/02-helm-deployment/deployment-status.txt)

Captures the status of deployed Kubernetes
resources at the time of validation.

The collected evidence should be reviewed to
confirm which components were deployed and
whether their workloads reached a healthy state.

## 9. Validation Results

Record actual results after reviewing the evidence.

| Validation criterion | Result |
|---|---|
| Helm CLI available | To verify |
| Kubernetes cluster accessible | To verify |
| Helm releases listed | To verify |
| Release history captured | To verify |
| Workload health validated | To verify |
| Configuration file versioned | To verify |
| Upgrade tested | Not yet evidenced |
| Rollback tested | Not yet evidenced |

## 10. Security Engineering Considerations

### Configuration management

Helm values files should be version-controlled
and reviewed before deployment.

Sensitive credentials and secrets must not be
committed to source control.

### Least privilege

Kubernetes service accounts and RBAC permissions
should be configured according to the
application's operational requirements.

### Deployment integrity

Container image versions and chart versions
should be controlled to reduce the risk of
unexpected deployment changes.

### Operational validation

A Helm release with status `deployed` does not
guarantee that all related pods and services
are functioning correctly.

### Rollback and recovery

Helm release history provides a mechanism
for restoring earlier release configurations.

However, rollback does not necessarily restore
external data or reverse all application-level
changes.

## 11. Limitations

This laboratory uses a local Kubernetes cluster
rather than a production managed Kubernetes
service.

The following capabilities are not established
by the existing Helm evidence alone:

- Production-scale deployment management
- Automated deployment approval workflows
- Tested rollback and recovery
- Multi-cluster deployment orchestration
- GitOps-based reconciliation
- Enterprise deployment governance

These capabilities require additional
implementation and validation.

## 12. Future Improvements

Potential extensions include:

1. Validate a Helm upgrade and rollback.
2. Capture before-and-after deployment evidence.
3. Implement Helm chart linting.
4. Run Helm template validation during CI.
5. Integrate Helm validation with GitHub Actions.
6. Introduce GitOps-based reconciliation
   using Argo CD.
7. Document configuration changes and
   operational recovery procedures.

## 13. Conclusion

This laboratory demonstrates the principles
of Helm-based Kubernetes deployment management.

Helm enables consistent deployment configuration,
release inspection, revision tracking, and
controlled application lifecycle operations.

The documented procedures and collected evidence
provide a foundation for evaluating deployment
reproducibility and operational reliability.

Further validation is required before claiming
automated deployment, tested rollback, or
production-grade release management.
