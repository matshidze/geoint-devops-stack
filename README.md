# GeoInt DevOps Stack

## Overview
This repository contains a containerised Python web application deployed on Kubernetes (Minikube) with CI/CD automation, monitoring, logging, and security controls applied. The purpose of the project is to demonstrate a practical DevOps workflow from development to deployment, observability, and security.

---

## 1. Process

### 1.1 Steps Followed

1. **Application Development**
   - Built a simple Flask web service using the app factory pattern.
   - Implemented '/healthz' and '/metrics' endpoints for monitoring and health checks.
   - Added unit tests using 'pytest'.

2. **Containerisation**
   - Created a Dockerfile using 'python:3.12-slim'.
   - Configured the container to run as a non-root user.
   - Built and tested the image locally.

3. **Local Orchestration**
   - Used Docker Compose for initial integration testing (app + PostgreSQL).

4. **Migration to Kubernetes**
   - Deployed the application to Minikube.
   - Created Kubernetes manifests for:
     - Namespace
     - ConfigMaps and Secrets
     - PostgreSQL StatefulSet with persistent storage
     - Application Deployment and Service
     - Ingress for external access

5. **CI/CD Pipeline**
   - Implemented GitHub Actions pipeline to:
     - Run tests
     - Build the Docker image
     - Validate deployment

6. **Monitoring and Logging**
   - Deployed Prometheus and Grafana.
   - Configured Prometheus to scrape '/metrics'.
   - Built dashboards and alerts in Grafana.

----

### 1.2 Tools Used

| Area | Tool |
|------|------|
| Containerisation | Docker |
| Orchestration | Kubernetes (Minikube) |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus, Grafana |
| Logging | Kubernetes logs |
| Database | PostgreSQL |
| Language | Python (Flask) |

---

## 2. Findings

### What worked well
- Minikube provided a fast and simple Kubernetes environment for local testing.
- Prometheus and Grafana integrated easily and gave clear visibility into application health.
- CI/CD pipeline automation reduced manual errors and ensured repeatable deployments.

### What was tricky
- Handling image availability between local Docker and Minikube (`ImagePullBackOff`).
- Ensuring the app did not connect to PostgreSQL at import time during testing.
- Correctly configuring RBAC and security contexts.
- Understanding Grafana’s changing UI between versions.

---

## 3. Learnings & Improvements

If more time were available, the following improvements would be made:

- Implement auto-scaling (HPA) based on CPU or request rate.
- Introduce centralized logging (e.g. Grafana Loki or ELK).
- Replace static secrets with a secrets manager (Vault or Sealed Secrets).
- Deploy to a managed Kubernetes platform (AKS/EKS/GKE).
- Add chaos testing and resilience testing.

---

## 4. Security & Compliance

### Security Controls Implemented
- Non-root containers.
- Kubernetes RBAC with namespace-scoped permissions.
- Secrets stored in Kubernetes Secrets.
- Network segmentation between application and database.
- Health and readiness probes.

### Compliance Considerations
- **GDPR:** Personal data protection, minimal data retention, encryption in transit.
- **ISO 27001:** Access control, auditability, and change management.
- **CIS Kubernetes Benchmark:** RBAC enabled, no cluster-admin usage, restricted privileges.

---

## 5. Conclusion

This project demonstrates a realistic DevOps pipeline covering development, deployment, observability, and security. It highlights the importance of automation, monitoring, and least-privilege access when operating modern cloud-native systems.

---

## How to Run Locally

'''bash
minikube start
kubectl apply -f k8s/
kubectl port-forward -n geoint svc/geoint-app 5000:80
