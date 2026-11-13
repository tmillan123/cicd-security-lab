
# 01 - Environment Setup

## Objective

Build and maintain a reproducible Kubernetes laboratory for cloud-native workload security engineering.

The environment supports containerized application deployment, runtime security monitoring, automated testing, and security observability.

## 1. Laboratory Environment

| Component | Technology | Purpose |
|-----------|------------|---------|
| Virtualization | VMware Workstation | Host the laboratory VM |
| Operating System | Ubuntu Linux | Development and execution environment |
| Container Runtime | Docker | Run containers and kind nodes |
| Container Orchestration | Kubernetes (kind) | Manage containerized workloads |
| Kubernetes CLI | kubectl | Manage and inspect Kubernetes resources |
| Package Management | Helm | Deploy and manage Kubernetes applications |
| Development | VS Code, Python | Develop and test applications |
| Source Control | Git and GitHub | Version control and collaboration |

The laboratory runs locally on an Ubuntu virtual machine.

## 2. Initial Environment Setup

This section documents the initial configuration of the laboratory.

Installation is generally performed once. Subsequent sessions use the existing environment.

### 2.1 Docker

Docker provides the container infrastructure used by kind.

Official documentation:
https://docs.docker.com/engine/install/ubuntu/

Docker must be installed and its daemon running before creating the Kubernetes cluster.

### 2.2 Kubernetes Using kind

kind (Kubernetes in Docker) creates local Kubernetes clusters using Docker containers as Kubernetes nodes.

Official documentation:
https://kind.sigs.k8s.io/

Create the laboratory cluster:

```bash
kind create cluster --name laboratorio
```

**Note:** This command creates a new cluster. Do not execute it when restoring an existing laboratory after a VM reboot.

### 2.3 kubectl

kubectl is the command-line interface used to communicate with the Kubernetes API server.

Official documentation:
https://kubernetes.io/docs/tasks/tools/

### 2.4 Helm

Helm is a Kubernetes package manager used to deploy and manage applications through versioned charts.

Official documentation:
https://helm.sh/docs/intro/install/

In this laboratory, Helm is used to manage security and monitoring components such as Falco and Loki.

Detailed deployments are documented in:

- [Deployment](deployment.md)
- [Security Controls](security-controls.md)

## 3. Environment Validation

### Objective

Verify that Docker, Kubernetes, and Helm are operational and ready for workload deployment.

### 3.1 Docker Validation

```bash
docker info
docker ps
```

**Expected result:**

- Docker daemon is accessible.
- Running containers are listed.
- The kind control-plane container is running.

### 3.2 Kubernetes Cluster Validation

```bash
kind get clusters
kubectl cluster-info
kubectl get nodes -o wide
```

**Expected result:**

- The `laboratorio` cluster is listed.
- The Kubernetes API server is reachable.
- Kubernetes nodes report `Ready`.

### 3.3 Kubernetes Workload Validation

```bash
kubectl get pods -A
```

**Expected result:**

- Kubernetes system components are healthy.
- Expected application and monitoring workloads are operational.
- No unexpected `CrashLoopBackOff`, `ImagePullBackOff`, or `CreateContainerError` conditions.

Individual workload status must be reviewed because a running cluster does not guarantee that every application is healthy.

### 3.4 Helm Validation

```bash
helm version
helm list -A
helm list --all-namespaces
```

**Expected result:**

- Helm reports its installed version.
- Existing Helm releases are listed.
- Release status can be inspected for deployment problems.

A deployed Helm release does not necessarily mean that all its pods are healthy.

### 3.5 Validation Evidence

Store command outputs in the project's `evidence/` directory.

Run these commands from the project root:

```bash
docker ps > evidence/01-cluster-baseline/docker-validation.txt
kubectl get nodes -o wide > evidence/01-cluster-baseline/kubernetes-nodes.txt
kubectl get pods -A > evidence/01-cluster-baseline/kubernetes-pods.txt
helm list -A > evidence/01-cluster-baseline/helm-releases.txt
```

Review the generated evidence before committing it to GitHub.

Evidence files:

- [Docker Validation](../evidence/01-cluster-baseline/docker-validation.txt)
- [Kubernetes Nodes](../evidence/01-cluster-baseline/kubernetes-nodes.txt)
- [Kubernetes Pods](../evidence/01-cluster-baseline/kubernetes-pods.txt)
- [Helm Releases](../evidence/01-cluster-baseline/helm-releases.txt)

These links become available once the corresponding files have been created and committed.

### 3.6 Validation Summary

| Component | Validation | Result |
|-----------|------------|--------|
| Docker | Daemon accessible | PASS |
| kind | Cluster exists | PASS |
| Kubernetes | Nodes Ready | PASS |
| Workloads | Expected pods healthy | Pending |
| Helm | Releases accessible | Pending |

Update each result to `PASS` or `FAIL` after executing the corresponding validation commands.

Document any failed checks and their resolution.

## 4. Restarting the Laboratory After a VM Reboot

The existing kind cluster should be reused after restarting the Ubuntu VM.

Recreating the cluster is unnecessary unless the original cluster has been deleted or cannot be recovered.

### 4.1 Start Docker

```bash
sudo systemctl start docker
```

Docker must be operational before the kind cluster can run.

### 4.2 Restore Kubernetes if Required

Docker may automatically restart the kind control-plane container depending on its restart policy.

If Kubernetes is unavailable, inspect the Docker containers:

```bash
docker ps -a
```

If the existing `laboratorio-control-plane` container is stopped, start it:

```bash
docker start laboratorio-control-plane
```

Allow Kubernetes components to initialize before validating cluster readiness.

### 4.3 Validate the Restored Environment

Execute the validation commands documented in [Section 3](#3-environment-validation).

Confirm that:

- Docker is operational.
- Kubernetes nodes report `Ready`.
- Expected workloads are healthy.
- Helm releases are accessible.

### 4.4 Troubleshooting

If Kubernetes remains unavailable, inspect the control-plane container logs:

```bash
docker logs laboratorio-control-plane
```

For Kubernetes workload issues, inspect the affected pod:

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl describe pod cicd-security-lab-8597f79977-dr7vp  -n security-lab 

kubectl logs <pod-name> -n <namespace>
kubectl logs cicd-security-lab-8597f79977-dr7vp -n security-lab
```

Replace `<pod-name>` and `<namespace>` with the actual values.

Investigate the root cause before deleting or recreating cluster resources.

## 5. Scope and Related Documentation

This document covers:

- Laboratory infrastructure
- Initial environment setup
- Operational validation
- Evidence collection
- Startup and recovery procedures

Detailed workload deployment, security monitoring, and detection engineering are documented separately.

| Document | Purpose |
|----------|---------|
| [Architecture](architecture.md) | System components and interactions |
| [Deployment](deployment.md) | Application and platform deployments |
| [Security Controls](security-controls.md) | Workload protection and runtime detection |
| [Limitations](limitations.md) | Known limitations and future improvements |
