
# 03 – Falco Runtime Threat Detection

## 1. Objective

Implement and validate runtime security monitoring for
containerized workloads running in Kubernetes using Falco.

The objective is to demonstrate how suspicious runtime
behaviour can be detected, investigated, and documented
through reproducible security tests.

**Security engineering capabilities:**

- Kubernetes runtime security monitoring
- Detection of suspicious container activity
- Event-based threat detection
- Security alert investigation
- Evidence collection and validation

## 2. Technology Overview

Falco is an open-source cloud-native runtime security tool
that monitors system activity and generates alerts when
observed behaviour matches configured detection rules.

Falco can detect activities such as:

- Unexpected shell execution inside containers
- Suspicious process execution
- Access to sensitive files
- Privilege escalation attempts
- Unexpected changes to system binaries

Falco provides runtime detection rather than vulnerability
scanning or automatic threat prevention.

## 3. Laboratory Environment

The validation is performed in the following environment:

| Component | Technology |
|---|---|
| Host | Ubuntu Linux VM (VMware) |
| Container runtime | Docker |
| Kubernetes | kind |
| Deployment management | Helm |
| Runtime threat detection | Falco |
| Evidence format | JSON events and terminal logs |
| Source control | Git and GitHub |

The Kubernetes cluster runs locally and does not require
a connection to a public cloud provider.

## 4. Falco Deployment and Verification

Falco is deployed to the Kubernetes cluster to monitor
runtime activity.

### 4.1 Verify the Falco deployment

```bash
kubectl get pods -A | grep falco
```

Identify the namespace and verify the Falco components:

```bash
kubectl get pods -n falco
kubectl get daemonsets -n falco
```

These commands assume Falco is installed in the `falco`
namespace. Adjust the namespace if necessary.

### 4.2 Inspect Falco logs

```bash
kubectl logs -n falco \
  -l app.kubernetes.io/name=falco \
  --tail=100
```

Check for successful startup, runtime driver initialization,
and any errors affecting event collection.

### 4.3 Check Helm deployment

If Falco was installed using Helm:

```bash
helm list -A
helm status falco -n falco
```

Record the deployed release and configuration.

## 5. Runtime Detection Test

### 5.1 Test objective

Evaluate whether Falco detects shell execution within
a running Kubernetes container.

Interactive shell access can be legitimate for
administration and troubleshooting. However, unexpected
shell execution may indicate suspicious activity,
including attacker interaction with a compromised workload.

### 5.2 Test procedure

Identify a running workload:

```bash
kubectl get pods -A
```

Select a test container that includes a shell.

Execute an interactive shell inside the container:

```bash
kubectl exec -it <pod-name> \
  -n <namespace> -- /bin/sh
```

Exit the shell after the test:

```bash
exit
```

This test must be executed only against a workload
authorized for security validation.

### 5.3 Expected detection

If the relevant Falco rule is enabled and the runtime
event is observable, Falco should generate an alert
associated with shell execution inside a container.

Depending on the ruleset and output configuration,
the alert may include:

- Detection rule name
- Event timestamp
- Event priority
- Container name or identifier
- Kubernetes pod and namespace
- Process name
- Command information

## 6. Evidence Collected

The following evidence files are stored in the repository.

### 6.1 Falco JSON Events

**Evidence file:**

[falco_events.json](../evidence/03-falco-detection/falco_events.json)

Purpose:

Capture Falco-generated events in a structured format
suitable for inspection and further analysis.

Validation criteria:

- An event is generated during the test window.
- The detection rule is identifiable.
- The event relates to the intended workload.
- The event contains sufficient context for investigation.

### 6.2 Terminal Shell Detection

**Evidence file:**

[terminal-shell-detection.log](../evidence/03-falco-detection/terminal-shell-detection.log)

Purpose:

Preserve the terminal output associated with the
shell-execution detection scenario.

The log should be reviewed to establish whether
the alert corresponds to the executed test.

## 7. Results and Security Interpretation

### 7.1 Validation results

Complete the following table after reviewing the
captured evidence.

| Validation criterion | Result |
|---|---|
| Falco deployment healthy | To verify |
| Runtime monitoring operational | To verify |
| Shell execution test performed | To verify |
| Falco alert generated | To verify |
| Alert matches test workload | To verify |
| Relevant event evidence captured | To verify |

### 7.2 Security interpretation

Runtime threat detection complements preventive
security controls by providing visibility into
process activity occurring within containers.

An alert corresponding to the shell-execution test
would demonstrate that Falco can identify this
specific activity under the tested conditions.

It would not, by itself, demonstrate:

- Detection of all malicious activity
- Automatic blocking of suspicious processes
- Complete coverage across all workloads
- End-to-end incident response automation

Falco alerts require contextual analysis to
distinguish legitimate administrative activity
from potentially malicious behaviour.

## 8. Security Engineering Considerations

### Detection accuracy

Detection rules must balance visibility with
the risk of false positives.

### Runtime visibility

Falco requires an operational event collection
mechanism and appropriate runtime permissions.

### Least privilege

Falco's deployment permissions and access
to host resources should be reviewed and
restricted according to its operational needs.

### Alert management

Runtime alerts should be integrated into a
centralized monitoring or security analysis
workflow where appropriate.

### Evidence integrity

Captured logs should be preserved without
unnecessary modification and reviewed for
sensitive information before publication.

## 9. Limitations

This laboratory demonstrates runtime security
validation in a local Kubernetes environment.

The following capabilities are not established
by this test alone:

- Production-scale deployment
- Enterprise XDR or SIEM integration
- Automated incident containment
- Multi-cloud workload coverage
- Comprehensive threat detection effectiveness

These represent potential areas for future
development and additional validation.

## 10. Future Improvements

Potential enhancements include:

1. Validate additional Falco detection rules.
2. Test suspicious file access and process execution.
3. Evaluate custom Falco rules.
4. Forward Falco alerts to centralized monitoring.
5. Visualize relevant events using Grafana.
6. Automate repeatable runtime security tests.
7. Map detection scenarios to MITRE ATT&CK
   techniques where appropriate.

## 11. Conclusion

This laboratory provides a framework for testing
runtime threat detection in Kubernetes using Falco.

The combination of reproducible test procedures,
structured event output, and documented evidence
supports the assessment of security monitoring
capabilities.

Detection effectiveness must be evaluated against
the actual collected events and the defined
validation criteria.
