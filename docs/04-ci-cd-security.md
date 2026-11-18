
# 04 – CI/CD Security Validation with GitHub Actions

## 1. Objective

Implement and validate automated security and
quality checks as part of a CI/CD workflow using
GitHub Actions.

The purpose is to demonstrate how security
validation can be integrated into the software
development lifecycle rather than performed
only after deployment.

**Security engineering objectives:**

- Automate application testing.
- Detect failures before changes are merged.
- Validate Python application dependencies.
- Introduce security checks into CI pipelines.
- Improve traceability of test execution.
- Establish a foundation for secure container
  build and deployment automation.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Git | Source control and change tracking |
| GitHub | Repository and workflow hosting |
| GitHub Actions | CI/CD automation |
| Python | Application runtime |
| pytest | Automated application testing |
| Docker | Container image packaging |
| Kubernetes (kind) | Local container orchestration |
| Helm | Kubernetes release management |
| YAML | Workflow and deployment configuration |

The exact checks executed depend on the
GitHub Actions workflow configuration.

## 3. CI/CD Security Architecture

The intended workflow separates source control,
continuous integration, security validation,
and deployment.

```text
Developer
    |
    v
Git Commit / Push
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +--> Python Dependency Installation
    |
    +--> Automated Tests (pytest)
    |
    +--> Security Validation
    |
    +--> Helm / Kubernetes Configuration Checks
    |
    v
CI Validation Result
    |
    v
Deployment Stage (future integration)
    |
    v
Kubernetes Workload
    |
    v
Falco Runtime Monitoring
```

Only stages configured in the actual workflow
should be considered implemented.

Falco operates at runtime and is not itself
a substitute for CI security checks.

## 4. GitHub Actions Configuration

GitHub Actions workflows are defined as YAML
files in:

`.github/workflows/`

The workflows define:

- Events that trigger execution.
- Jobs and their dependencies.
- Runner environments.
- Commands executed during each job.
- Conditions under which jobs succeed or fail.

Typical workflow triggers include:

- Push events.
- Pull requests.
- Manual execution.

### 4.1 Verify the configured workflow

Inspect the YAML files in:

[GitHub Actions workflows](../.github/workflows/)

Review the configured triggers, permissions,
jobs, and security validation steps.

The actual workflow definition is the
authoritative source for which checks have
been implemented.

## 5. Continuous Integration Validation

### 5.1 Python environment

The application uses Python dependencies
defined in:

[requirements.txt](../requirements.txt)

A CI workflow can install dependencies using:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Dependency installation validates that the
required packages can be resolved in the
selected runner environment.

It does not automatically establish that
those dependencies are free from vulnerabilities.

### 5.2 Automated testing

Application tests are maintained in:

[tests/](../tests/)

The test suite can be executed using:

```bash
python -m pytest -v
```

Tests should fail with a non-zero exit code
when assertions are not satisfied.

When this command is included in GitHub Actions,
the workflow can report the test result
automatically.

### 5.3 Docker build validation

A Docker image can be built using:

```bash
docker build -t cicd-security-lab:test .
```

This validates that the Dockerfile and
build context can produce a container image.

A successful build does not establish that
the image is secure.

Image vulnerability scanning and runtime
configuration validation require separate
security checks.

## 6. Security Checks in CI

Security controls can be introduced at
different points in the CI workflow.

| Security check | Purpose |
|---|---|
| Automated tests | Validate expected application behaviour |
| Dependency scanning | Identify known vulnerable dependencies |
| Static analysis (SAST) | Identify potentially insecure source code patterns |
| Secret scanning | Detect accidentally committed credentials |
| Container image scanning | Identify known vulnerabilities in image packages |
| Helm linting | Identify chart structure and template issues |

These checks are potential controls.

Only checks configured and successfully
executed in the repository should be reported
as completed.

### 6.1 Helm validation

For repositories containing Helm charts,
chart structure can be checked using:

```bash
helm lint ./charts/<chart-name>
```

Rendered Kubernetes manifests can be
inspected using:

```bash
helm template test-release ./charts/<chart-name>
```

These commands require an actual Helm chart
at the specified path.

Helm linting does not replace Kubernetes
manifest security validation.

### 6.2 Container security scanning

Container image scanning can identify known
vulnerabilities in operating system packages
and application dependencies.

A future improvement is to introduce an image
scanner such as Trivy into the GitHub Actions
workflow.

The scan results should be preserved as
security evidence.

## 7. CI Workflow Evidence

Evidence of automated execution should be
collected from actual GitHub Actions runs.

Suggested directory:

`evidence/04-ci-cd-security/`

Useful evidence includes:

- Workflow execution summary.
- Successful automated test results.
- Failed test execution and subsequent fix.
- Security scan output, if implemented.
- Helm validation output, if implemented.

For reproducibility, record:

- Workflow name.
- Commit SHA.
- Execution date.
- Job name.
- Result.
- Relevant log excerpt or report.

Do not publish tokens, credentials, or other
sensitive information contained in logs.

## 8. Validation Results

Update this table based on completed
GitHub Actions executions.

| Validation criterion | Result |
|---|---|
| GitHub workflow YAML created | To verify |
| Workflow triggered automatically | To verify |
| Python dependencies installed | To verify |
| pytest executed in CI | To verify |
| CI failure behaviour validated | To verify |
| Docker build automated | Not yet evidenced |
| Dependency scanning integrated | Not yet evidenced |
| Container scanning integrated | Not yet evidenced |
| Helm validation automated | Not yet evidenced |
| Kubernetes deployment automated | Not yet evidenced |

## 9. Security Engineering Considerations

### Least privilege

GitHub Actions permissions should follow
the principle of least privilege.

Workflows should request only the permissions
required for their operations.

### Secrets management

Credentials must not be hardcoded in workflow
definitions or source code.

Where possible, short-lived credentials and
federated authentication should be preferred
over long-lived secrets.

### Third-party actions

External GitHub Actions should be reviewed
and pinned to immutable commit identifiers
where practical.

### Branch protection

Protected branches and required status checks
can prevent changes from being merged before
mandatory validation succeeds.

### Supply chain security

Dependencies, build tools, actions, container
images, and deployment artifacts form part
of the software supply chain.

Each introduces potential security risks
that should be assessed and controlled.

## 10. CI Versus CD

Continuous Integration (CI) automates checks
associated with changes to source code.

Continuous Delivery or Continuous Deployment
(CD) extends automation into the release
and deployment lifecycle.

This laboratory distinguishes between:

**Implemented CI:**

Automated checks that are configured and
verified through GitHub Actions execution.

**Planned CD:**

Automated deployment of validated application
artifacts into Kubernetes.

Using Helm manually to install an application
does not, by itself, demonstrate an automated
CD pipeline.

Similarly, using Git as source control does not
constitute a GitOps implementation.

## 11. Limitations

The implemented capabilities should be
evaluated against the actual workflow files
and execution evidence.

Potential limitations include:

- Lack of automated image scanning.
- No demonstrated deployment approval process.
- No automated rollback.
- No production Kubernetes deployment.
- No established GitOps reconciliation.
- Limited security test coverage.

Capabilities not yet implemented should
remain documented as future improvements
rather than completed validation results.

## 12. Future Improvements

1. Add Python dependency vulnerability scanning.
2. Introduce container image scanning using Trivy.
3. Add Helm linting and manifest validation.
4. Configure required CI checks for pull requests.
5. Capture successful and failed pipeline evidence.
6. Implement an automated deployment to a
   suitable Kubernetes test environment.
7. Evaluate GitOps reconciliation using Argo CD.
8. Introduce security policies for deployment
   validation and release approval.

## 13. Conclusion

This laboratory demonstrates the implementation and validation of runtime threat detection in a local Kubernetes environment using Falco.

The successful detection of a shell spawned inside a container provides evidence that Falco can identify the specific runtime behaviour under test.

Reproducible test procedures, structured security events, and preserved detection logs support the validation of security controls and the investigation of suspicious workload activity.

The laboratory also establishes a foundation for extending runtime detection into centralized log aggregation, visualization, alerting, and potentially SIEM/XDR integration.

The results demonstrate detection capability for the tested scenarios, rather than comprehensive threat detection effectiveness or production readiness.