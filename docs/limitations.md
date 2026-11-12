
# Laboratory Limitations and Future Improvements

## 1. Purpose

This document describes the known limitations, implementation
constraints, validation gaps, and planned improvements of the
Cloud-Native Workload Security Engineering Lab.

The laboratory is designed for practical security engineering,
controlled experimentation, and validation of Kubernetes
workload security capabilities.

It is not intended to provide a production-ready Kubernetes
platform or a fully operational enterprise security service.

Architectural constraints and design decisions are documented
separately in [Architecture](architecture.md).

## 2. Infrastructure Limitations

### Local Virtualization

The laboratory runs on an Ubuntu Linux virtual machine
hosted on VMware Workstation.

This introduces several constraints:

- Compute, memory, and storage capacity depend on the
  resources allocated to the virtual machine.
- The environment depends on a single physical host.
- Host or VM failures may interrupt the entire laboratory.
- Enterprise availability and disaster recovery mechanisms
  are not implemented.

### Kubernetes Environment

The laboratory uses kind (Kubernetes in Docker), rather than
a managed Kubernetes platform such as Azure Kubernetes
Service (AKS).

Consequently, the environment does not currently validate:

- Managed Kubernetes control-plane security.
- Azure identity and workload identity integration.
- Cloud networking and enterprise network segmentation.
- Managed cluster upgrades and cloud provider operations.
- Production-scale workload scheduling and resilience.

However, Kubernetes-native workload security concepts
remain applicable across these environments.

## 3. Security Detection Limitations

### Falco Runtime Detection

Falco provides runtime event monitoring and detection
through configurable security rules.

Current limitations and validation considerations include:

- Detection coverage depends on the available system
  events and configured detection rules.
- Runtime detection does not automatically provide
  comprehensive threat prevention.
- False positives and false negatives require analysis.
- Detection rules require tuning for specific workloads.
- Performance overhead has not been formally benchmarked.

### Detection Engineering Maturity

The laboratory does not yet demonstrate a complete
enterprise detection engineering lifecycle.

Future validation should include:

- Custom Falco detection rules.
- Controlled attack simulation and detection testing.
- False-positive analysis and rule tuning.
- Detection coverage documentation.
- Repeatable security test scenarios.

## 4. Security Telemetry and Observability Limitations

The observability architecture includes Falco, Loki,
and Grafana.

However, deployment of individual components does not
guarantee a fully operational security monitoring pipeline.

### Integration Validation

The end-to-end telemetry pipeline requires confirmation
that:

1. Falco generates a security event.
2. A compatible forwarding component collects the event.
3. Loki successfully ingests the event.
4. Grafana can retrieve and display the event.
5. The event contains sufficient context for investigation.

### Operational Considerations

Additional areas requiring evaluation include:

- Log retention and storage capacity.
- Secure transmission of security telemetry.
- Access control for logs and dashboards.
- Monitoring of ingestion failures.
- Alerting and incident response integration.
- Centralized telemetry availability.

These capabilities would require additional engineering
before the monitoring architecture could be considered
production-ready.

## 5. CI/CD and Software Supply Chain Limitations

GitHub Actions provides a foundation for automated
testing and security validation.

The maturity of the CI/CD security capability depends
on the workflows and controls actually implemented.

Potential improvements include:

- Automated dependency vulnerability scanning.
- Container image security scanning.
- Kubernetes manifest and Helm configuration validation.
- Static application security testing (SAST).
- Software Bill of Materials (SBOM) generation.
- Container image signing and provenance verification.
- Automated enforcement of security quality gates.

Any control not yet implemented should be treated as
a planned enhancement rather than an existing capability.

## 6. GitOps Limitations

Argo CD is currently a planned architectural component.

Consequently, the laboratory does not yet demonstrate:

- Automated GitOps deployment reconciliation.
- Continuous configuration drift detection.
- Git-based deployment recovery.
- GitOps access control and deployment governance.
- GitOps-driven application lifecycle management.

These capabilities are candidates for future
implementation and validation.

## 7. Operational and Security Process Limitations

The laboratory focuses primarily on technical deployment
and security control validation.

It does not currently reproduce the full operational
processes required by an enterprise security function.

Examples include:

- Formal change management and approval workflows.
- Continuous vulnerability management.
- Security incident response procedures.
- Enterprise SIEM/SOAR integration.
- Security service-level objectives and monitoring.
- Production backup and disaster recovery procedures.
- Formal compliance assessment and audit processes.

These processes would require additional organizational
controls, governance, and operational integration.

## 8. Planned Improvements

The following improvements are proposed to extend the
laboratory's security engineering capabilities.

| Priority | Improvement | Expected Outcome |
|----------|-------------|------------------|
| High | Validate Falco runtime alerts | Demonstrate operational threat detection |
| High | Integrate Falco with Loki | Establish centralized security telemetry |
| High | Validate Grafana log queries | Demonstrate security event investigation |
| High | Expand GitHub Actions security checks | Automate preventive security validation |
| Medium | Implement custom Falco rules | Demonstrate detection engineering |
| Medium | Introduce workload hardening | Strengthen Kubernetes security posture |
| Medium | Add container image scanning | Improve software supply-chain security |
| Medium | Deploy Argo CD | Demonstrate GitOps and drift detection |
| Low | Evaluate enterprise cloud integration | Assess transferability to managed Kubernetes |

Priorities represent proposed engineering work and
should be reviewed as capabilities are completed.

## 9. Validation and Evidence

A capability should be considered validated only when
its expected behavior has been demonstrated through
repeatable testing.

Evidence should include, where appropriate:

- Configuration files.
- Relevant execution commands.
- Expected and observed results.
- Screenshots or command output.
- Test results and failure conditions.
- References to supporting evidence.

Validated outcomes should be documented in
[Security Controls](security-controls.md) and the
[evidence directory](../evidence/).

## 10. Conclusion

The laboratory provides a controlled environment for
exploring and validating cloud-native workload security
engineering practices.

Its limitations reflect the differences between a
resource-constrained development laboratory and a
production enterprise Kubernetes platform.

Documenting these limitations supports transparent
assessment of the implemented capabilities, helps
prioritize engineering improvements, and provides a
foundation for progressively increasing the maturity
of the security architecture.
