
# Security Controls – Cloud-Native Workload Security Lab

## 1. Security Control Objectives

This document describes the security controls, validation
scenarios, and supporting evidence associated with the
Cloud-Native Workload Security Engineering Lab.

The objective is to demonstrate how preventive, detective,
and automated security controls can be applied to
containerized workloads running in Kubernetes.

The laboratory focuses on:

- Kubernetes workload security and least privilege.
- Runtime threat detection using Falco.
- Security event collection and observability.
- Automated security validation using GitHub Actions.
- Repeatable security testing and evidence collection.

The architecture is documented in
[Architecture](architecture.md).

Deployment procedures are documented in
[Deployment](deployment.md).

## 2. Security Control Matrix

The following matrix identifies the security capabilities
under evaluation.

Status values distinguish implemented controls from
capabilities requiring further validation.

| ID | Security Control | Technology | Status |
|----|------------------|------------|--------|
| SC-01 | Runtime threat detection | Falco | Installed; validation pending |
| SC-02 | Container security contexts | Kubernetes | To validate |
| SC-03 | Least-privilege access | Kubernetes RBAC | To validate |
| SC-04 | Workload network isolation | NetworkPolicies | Planned |
| SC-05 | Centralized security logging | Loki | Installed; ingestion pending |
| SC-06 | Security event visualization | Grafana | To validate |
| SC-07 | Automated application tests | GitHub Actions | To validate |
| SC-08 | Container image vulnerability scanning | CI security tooling | Planned |
| SC-09 | Configuration drift detection | Argo CD | Planned |

These statuses represent the currently documented
laboratory progress and must be updated following
successful verification.

## 3. Runtime Threat Detection – Falco

### SC-01: Runtime Threat Detection

**Security Objective**

Detect suspicious activity occurring within containerized
workloads, including unexpected process execution and
potentially unauthorized access to sensitive resources.

**Threats Addressed**

- Execution of interactive shells inside containers.
- Suspicious process activity.
- Unexpected access to sensitive files.
- Potential indicators of container compromise.

**Control Implementation**

Falco is deployed using Helm in the Kubernetes cluster.

Falco observes supported runtime events through its
configured instrumentation and evaluates them against
security detection rules.

Matching events generate alerts containing information
that may support further investigation.

### Validation Scenario: Unexpected Shell Execution

**Test ID:** SC-01-T01

**Objective:** Verify that Falco detects interactive
shell execution within a monitored container.

**Test Procedure**

1. Confirm that Falco Pods are running.
2. Select a suitable test workload.
3. Execute an interactive shell inside the test container.
4. Inspect Falco logs for the expected detection.
5. Record the observed rule, priority, and event details.

Example commands:

```bash
kubectl get pods -n falco

kubectl get pods -A

kubectl exec -n <namespace> -it <pod-name> \
  -- /bin/sh
```

Inspect Falco events:

```bash
kubectl logs -n falco \
  -l app.kubernetes.io/name=falco \
  --all-containers=true --since=5m
```

**Expected Result**

Falco generates an alert when the test activity matches
an enabled detection rule.

**Observed Result:** Pending validation.

**Evidence:** Pending.

**Note:** Detection depends on enabled rules, workload
behavior, and Falco runtime visibility.

## 4. Kubernetes Workload Hardening

### SC-02: Container Security Contexts

**Security Objective**

Reduce the privileges available to containerized workloads
and limit the impact of potential compromise.

**Recommended Controls**

- Run application processes as non-root users.
- Prevent privilege escalation where feasible.
- Drop unnecessary Linux capabilities.
- Use read-only root filesystems where supported.
- Apply appropriate seccomp profiles.
- Avoid privileged containers unless explicitly required.

Example Kubernetes security context:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
  seccompProfile:
    type: RuntimeDefault
```

This example illustrates recommended controls.
Application compatibility must be verified before
applying these settings.

**Validation Approach**

Inspect workload manifests and the deployed Pod
security configuration.

**Status:** To validate.

### SC-03: Kubernetes RBAC

**Security Objective**

Restrict access to Kubernetes resources according
to least-privilege principles.

**Validation Approach**

1. Review service accounts and role bindings.
2. Identify excessive permissions.
3. Verify that application identities have only the
   permissions required for their functions.
4. Test authorization using Kubernetes access checks.

Example:

```bash
kubectl auth can-i list secrets \
  --as=system:serviceaccount:app:default \
  -n app
```

**Expected Result**

A workload identity should not have permission to
access Kubernetes Secrets unless explicitly required.

**Status:** To validate.

### SC-04: Network Isolation

**Security Objective**

Limit unnecessary communication between workloads
and reduce opportunities for lateral movement.

Kubernetes NetworkPolicies can restrict ingress
and egress traffic between Pods and namespaces.

Effective enforcement requires a compatible
networking implementation.

**Status:** Planned.

## 5. Security Logging and Observability

### SC-05: Centralized Security Logging

**Security Objective**

Collect security-relevant events centrally to
support investigation and monitoring.

**Technology:** Grafana Loki.

**Validation Approach**

1. Confirm the Loki deployment is healthy.
2. Configure a compatible log forwarding component.
3. Generate a controlled Falco detection event.
4. Verify that the event is ingested into Loki.
5. Query the event and inspect its metadata.

**Expected Result**

Security events can be retrieved from centralized
logging with sufficient context for investigation.

**Status:** Integration validation pending.

### SC-06: Security Event Visualization

**Security Objective**

Provide a visual interface for investigating
security-relevant workload activity.

**Technology:** Grafana.

**Validation Approach**

1. Verify Grafana availability.
2. Configure Loki as a data source.
3. Execute a security-relevant log query.
4. Confirm the event is visible.
5. Review the available investigation context.

**Expected Result**

Security analysts can retrieve and investigate
runtime detection events through Grafana.

**Status:** To validate.

## 6. CI/CD Security Controls

### SC-07: Automated Application Testing

**Security Objective**

Identify defects and potential security weaknesses
before changes are promoted for deployment.

**Technology:** GitHub Actions.

**Validation Approach**

1. Review the GitHub Actions workflow configuration.
2. Commit and push a controlled code change.
3. Confirm that the configured workflow executes.
4. Review the test results.
5. Introduce a controlled failing test.
6. Verify that the workflow reports failure.

**Expected Result**

Automated checks provide reliable feedback and
fail when configured validation requirements
are not satisfied.

**Status:** To validate.

### SC-08: Container Image Vulnerability Scanning

**Security Objective**

Identify known vulnerabilities in container images
before deployment.

**Potential Technologies**

- Trivy
- Grype
- Docker Scout

**Planned Validation**

1. Build or select a test container image.
2. Execute a vulnerability scan.
3. Review detected vulnerabilities.
4. Apply a defined severity policy.
5. Verify that the CI workflow reports violations.

**Status:** Planned.

## 7. Security Validation Methodology

Security controls are evaluated through repeatable,
controlled test scenarios.

Each validation should document:

1. **Control ID:** Unique control identifier.
2. **Objective:** Security requirement being evaluated.
3. **Test procedure:** Steps required to reproduce the test.
4. **Expected result:** Intended security behavior.
5. **Observed result:** Actual behavior.
6. **Evidence:** Supporting command output or screenshots.
7. **Status:** Validation outcome.

Validation outcomes use the following classifications:

| Status | Meaning |
|--------|---------|
| Planned | Control has not yet been implemented |
| Implemented | Control has been configured or deployed |
| Pass | Expected security behavior has been demonstrated |
| Fail | Observed behavior does not meet the expected result |
| Blocked | Validation cannot proceed due to a dependency |
| Not tested | Control or test exists but validation has not been performed |

A successful installation alone does not constitute
successful security control validation.

## 8. Validation Results and Evidence

The following table tracks security control validation.

| Test ID | Test Scenario | Result | Evidence |
|---------|---------------|--------|----------|
| SC-01-T01 | Unexpected shell execution | Not tested | Pending |
| SC-02-T01 | Container privilege restrictions | Not tested | Pending |
| SC-03-T01 | Kubernetes RBAC authorization | Not tested | Pending |
| SC-04-T01 | Network isolation | Planned | Pending |
| SC-05-T01 | Falco event ingestion into Loki | Not tested | Pending |
| SC-06-T01 | Grafana security event query | Not tested | Pending |
| SC-07-T01 | GitHub Actions test execution | Not tested | Pending |
| SC-07-T02 | CI pipeline failure handling | Not tested | Pending |
| SC-08-T01 | Container image vulnerability scanning | Planned | Pending |

Security evidence should be stored in the
[evidence directory](../evidence/).

Results must be updated after each test execution,
including failures and unexpected behavior.

## 9. Security Control Maturity and Next Steps

The laboratory is being developed incrementally,
prioritizing operational validation of security
controls before expanding the technology stack.

The immediate priorities are:

1. Validate Falco runtime detection using controlled events.
2. Verify security event ingestion into Loki.
3. Investigate security events through Grafana.
4. Validate GitHub Actions automated testing.
5. Implement and test Kubernetes workload hardening.
6. Extend automated security checks to container images
   and Kubernetes configurations.

Future enhancements include GitOps-based deployment
management using Argo CD.

The objective is to progress from individual tool
deployment to validated, integrated security
engineering capabilities.
