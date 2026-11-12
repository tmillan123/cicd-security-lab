# Architecture – Cloud-Native Workload Security Lab

## Architecture Overview

This laboratory implements a local Kubernetes environment for workload security engineering, runtime threat detection, and security observability.

## Architecture Diagram

![Cloud-Native Workload Security Architecture](../evidence/Architecture-and-Flows.png)

## Architecture Components
- GitHub Actions for CI/CD automation
- Docker and kind for containerized Kubernetes workloads
- Helm for Kubernetes deployments
- Falco for runtime threat detection
- Loki for centralized log aggregation
- Grafana for security observability
- Argo CD for planned GitOps integration
## Security Architecture and Runtime Detection

### Falco Runtime Security

Falco is deployed in the Kubernetes environment to provide
runtime visibility into container and workload activity.

Falco monitors supported system events and evaluates them
against configurable security detection rules.

Examples of suspicious activity include:

- Unexpected shell execution inside containers
- Access to sensitive system files
- Suspicious process execution
- Unauthorized changes to critical files

### Runtime Detection Flow

1. A containerized workload generates system activity.
2. Falco observes the relevant runtime events.
3. Falco evaluates events against its detection rules.
4. Matching rules generate security alerts.
5. Alerts can be forwarded to the observability platform
   for investigation and analysis.

### Security Engineering Considerations

Falco provides detection capabilities rather than
comprehensive automated prevention.

Effective runtime security also requires:

- Appropriate Kubernetes RBAC permissions
- Container security contexts and least privilege
- Workload configuration hardening
- Security event collection and investigation
- Incident response procedures

The laboratory aims to validate these capabilities
through controlled security testing.

### Architectural Overview

The security observability architecture is designed to provide
centralized visibility into Kubernetes workload activity and
runtime security events.

The architecture combines Falco for runtime threat detection,
Grafana Loki for log aggregation, and Grafana for security
event visualization and investigation.

Together, these components establish the foundation for a
security monitoring capability that supports threat detection,
investigation, and operational awareness.

### Security Telemetry Architecture

The intended security telemetry pipeline follows this flow:

**Kubernetes Workloads → Falco → Log Forwarding → Loki → Grafana**

Each component performs a distinct architectural function:

- **Kubernetes workloads:** Generate runtime activity through
  application processes, system calls, and container operations.

- **Falco:** Observes supported runtime events and evaluates them
  against security detection rules. Matching events generate
  structured security alerts.

- **Log forwarding layer:** Collects and transports Falco alerts
  to the centralized logging platform. This requires a compatible
  integration such as Falcosidekick or a log collection agent.

- **Grafana Loki:** Receives and stores security logs, indexes
  selected metadata labels, and supports efficient querying.

- **Grafana:** Queries Loki to enable security event investigation,
  visualization, and alerting.

### Security Monitoring Use Cases

The architecture is intended to support security monitoring
scenarios including:

- Detection of unexpected shell execution inside containers.
- Identification of suspicious process activity.
- Monitoring access to sensitive files.
- Investigation of anomalous Kubernetes workload behavior.
- Correlation of runtime security alerts with application logs.

### Security Design Considerations

The observability architecture introduces several important
security requirements:

- **Telemetry integrity:** Security events must be collected and
  transported reliably to minimize the risk of missing evidence.

- **Access control:** Access to Grafana dashboards and security
  logs should follow least-privilege principles.

- **Data protection:** Logs may contain sensitive operational
  information and require appropriate access restrictions.

- **Detection coverage:** Falco detection capabilities depend on
  event visibility, configured rules, and supported runtime
  instrumentation.

- **Operational resilience:** Production implementations require
  appropriate log retention, storage capacity, and monitoring
  of telemetry pipeline health.

### Implementation Status

Falco and Loki have been deployed in the laboratory using Helm.

The end-to-end integration between Falco, log forwarding,
Loki, and Grafana requires validation before the complete
security telemetry pipeline can be considered operational.

Successful validation should demonstrate that a controlled
runtime security event can be detected by Falco, collected
by Loki, and retrieved through Grafana.

---

## CI/CD and GitOps

### Architectural Overview

The deployment architecture is designed to introduce automated
validation, controlled configuration management, and
reproducible Kubernetes deployments.

GitHub provides the source control platform, GitHub Actions
supports continuous integration and security validation,
and Helm manages Kubernetes application deployments.

Argo CD is planned as an additional GitOps capability for
declarative deployment management and configuration
drift detection.

### CI/CD Architecture – GitHub Actions

GitHub Actions provides a mechanism for automating quality
and security checks throughout the development lifecycle.

The intended CI workflow follows these stages:

1. A developer commits and pushes changes to GitHub.
2. A GitHub Actions workflow is triggered.
3. Automated tests validate application functionality.
4. Security checks assess relevant dependencies,
   container images, or Kubernetes configurations.
5. Workflow results provide feedback before changes
   are promoted for deployment.

This approach supports the principle of **shifting security
left**, identifying potential vulnerabilities and
configuration weaknesses earlier in the development process.

### Kubernetes Deployment Management – Helm

Helm provides package management and configuration
templating for Kubernetes applications.

Within the laboratory, Helm is used to deploy and manage
security and observability components such as Falco and Loki.

From an architectural perspective, Helm enables:

- Repeatable application deployments.
- Version-controlled configuration values.
- Consistent installation and upgrade procedures.
- Simplified management of Kubernetes resources.
- Rollback capabilities for supported Helm releases.

Helm provides deployment packaging and lifecycle management;
it does not independently implement a continuous delivery
pipeline.

### GitOps Architecture – Argo CD (Planned)

Argo CD is planned to extend the deployment architecture
with GitOps-based continuous delivery.

Under the GitOps model, version-controlled Kubernetes
manifests and Helm configurations define the desired
state of the environment.

Argo CD continuously compares this desired state against
the actual state of the Kubernetes cluster.

The intended GitOps workflow is:

1. Deployment configuration is updated in Git.
2. Changes undergo review and automated validation.
3. Argo CD detects changes in the desired configuration.
4. Differences between Git and the cluster are identified.
5. Argo CD synchronizes the deployment according to
   the configured synchronization policy.

This architecture separates continuous integration from
deployment reconciliation:

- **GitHub Actions:** Validates changes before deployment.
- **Helm:** Packages and templates Kubernetes applications.
- **Argo CD:** Reconciles the cluster with the desired
  configuration stored in Git.

### CI/CD and GitOps Security Considerations

The deployment architecture must account for the security
of the software delivery process.

Key considerations include:

- **Pipeline permissions:** GitHub Actions workflows should
  operate with minimum required permissions.

- **Secrets management:** Credentials, tokens, and sensitive
  configuration values must not be committed to Git.

- **Supply-chain security:** Dependencies and container
  images should be assessed for vulnerabilities and integrity.

- **Deployment authorization:** Access to modify Kubernetes
  resources should be restricted through appropriate RBAC.

- **Change traceability:** Deployment changes should be
  associated with version-controlled commits and
  validation results.

- **Configuration integrity:** GitOps reconciliation should
  identify unexpected drift between the declared and
  actual cluster configuration.

### Architectural Evolution

The target deployment model combines automated security
validation with declarative Kubernetes deployment management.

**Source Code → CI Validation → Git Configuration → Argo CD
→ Kubernetes Deployment → Runtime Security Monitoring**

This model illustrates how preventive security checks,
controlled deployment processes, and runtime detection
capabilities can contribute to a defense-in-depth approach
to cloud-native workload security.

Argo CD remains a planned enhancement and should not be
considered an implemented capability until deployment
and reconciliation have been validated.
## Architecture Decisions and Limitations

### Architecture Decisions

The laboratory architecture was designed to provide a practical,
reproducible environment for evaluating cloud-native workload
security capabilities.

Technology selection was guided by compatibility with the existing
Ubuntu-based home laboratory, ease of deployment, resource efficiency,
and relevance to enterprise security engineering practices.

The key architectural decisions include:

- **kind (Kubernetes in Docker):** Selected to provide a lightweight,
  locally managed Kubernetes environment suitable for testing workload
  deployments, configurations, and security controls without requiring
  cloud infrastructure.

- **Falco:** Selected for its open-source runtime threat detection
  capabilities, enabling the observation of suspicious system and
  container activity.

- **Grafana Loki:** Selected to provide centralized log aggregation
  and querying with relatively low operational complexity.

- **Grafana:** Selected to support security observability through
  dashboards, log exploration, and investigation.

- **GitHub Actions:** Selected to introduce automated testing and
  security validation into the development lifecycle, using the
  project's existing GitHub repository.

- **Helm:** Selected to simplify deployment and configuration
  management of Kubernetes applications.

These technologies provide a foundation for demonstrating how
security controls, deployment automation, and observability
capabilities can be integrated into a Kubernetes-based environment.

### Architecture Limitations

The laboratory operates within a single Ubuntu virtual machine
and is intended for security engineering experimentation and
control validation rather than production workloads.

Key limitations include:

- **Infrastructure resilience:** The environment does not provide
  production-grade high availability, fault tolerance, or disaster
  recovery capabilities.

- **Scalability:** Computing resources are limited by the host
  machine, restricting the ability to simulate large-scale
  enterprise workloads.

- **Cloud integration:** Managed cloud capabilities such as Azure
  Kubernetes Service (AKS), cloud-native identity integration,
  and managed networking are outside the current scope.

- **Security operations:** Detection, telemetry collection,
  alerting, and incident response integrations require individual
  implementation and validation.

- **Deployment maturity:** GitOps-based deployment management
  using Argo CD remains a planned enhancement.

### Enterprise Applicability

Although implemented locally, the laboratory uses Kubernetes-native
components and security engineering principles applicable to
enterprise container platforms, including Azure Kubernetes
Service (AKS).

The architecture supports practical exploration of workload
hardening, runtime threat detection, security observability,
and automated security validation.

However, transferring these capabilities to an enterprise
environment would require additional architectural considerations,
including:

- Identity and access management (IAM)
- Network segmentation and Kubernetes NetworkPolicies
- Secrets management
- Scalability and high availability
- Security governance and compliance
- Integration with enterprise detection and incident response platforms

**The objective is not to reproduce a production Kubernetes platform,
but to demonstrate and validate security engineering patterns
that can inform enterprise workload security architectures.**
