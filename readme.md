# Kubernetes Multi-Tier Application



A multi-tier web application containerized with Docker and deployed to Kubernetes using minikube. Features a Python Flask backend, Nginx frontend, and PostgreSQL database, all orchestrated with Kubernetes and automated via a GitHub Actions CI/CD pipeline that builds and pushes images to Amazon ECR.

---

## Architecture



All external traffic enters through the Nginx Ingress Controller which routes requests to the appropriate service. `/` routes to the frontend service which serves the static HTML page. `/api/` routes to the backend Flask API which connects to the PostgreSQL database over a private cluster network.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Docker | Containerize frontend and backend applications |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| Nginx | Frontend web server and reverse proxy |
| Python Flask | Backend REST API |
| PostgreSQL | Relational database |
| Amazon ECR | Container image registry |
| GitHub Actions | CI/CD pipeline |

---

---

## Prerequisites

- [Docker](https://docker.com) installed and running
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
- [AWS CLI](https://aws.amazon.com/cli/) installed and configured

---

## How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/YOURUSERNAME/kubernetes-eks-app.git
cd kubernetes-eks-app
```

### 2. Start Minikube
```bash
minikube start --driver=docker
```

### 3. Enable the Ingress Addon
```bash
minikube addons enable ingress
minikube addons enable metrics-server
```

### 4. Build and Load Docker Images
```bash
docker build -t frontend:local ./app/frontend
docker build -t backend:local ./app/backend
minikube image load frontend:local
minikube image load backend:local
```

### 5. Apply Kubernetes Manifests
```bash
kubectl apply -f kubernetes/database/
kubectl apply -f kubernetes/backend/
kubectl apply -f kubernetes/frontend/
```

### 6. Verify Everything is Running
```bash
kubectl get pods
kubectl get services
kubectl get ingress
kubectl get hpa
```
All pods should show `Running` status.

### 7. Access the Application
```bash
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80 --address 0.0.0.0
```
Open your browser to `http://localhost:8080`

---

## Kubernetes Resources

**Deployments** — define the desired state for each service including the container image, environment variables, and resource limits. Used for the frontend, backend, and database.

**Services** — expose each deployment within the cluster under a stable DNS name. The database is only accessible internally. The frontend is exposed via NodePort.

**ConfigMap** — stores non-sensitive backend environment variables like the database host and port. Keeps configuration separate from application code.

**Secrets** — stores sensitive values like database credentials. Referenced by deployments as environment variables so credentials are never hardcoded in manifests.

**Ingress** — routes external traffic into the cluster. Routes `/` to the frontend service and `/api/` to the backend service under a single entry point.

**HorizontalPodAutoscaler** — automatically scales the frontend and backend deployments based on CPU utilization. Backend scales between 1-5 replicas, frontend between 1-3 replicas, both targeting 50% CPU utilization.

---

## CI/CD Pipeline

The GitHub Actions pipeline runs on every push and pull request to main:

**On every push and PR:**
- Builds frontend and backend Docker images
- Pushes images to Amazon ECR tagged with the commit SHA and `latest`
- Validates all Kubernetes manifests using kubeconform

Images are tagged with both the commit SHA for traceability and `latest` for convenience:

ECR_REGISTRY/kubernetes-eks-app/frontend:abc1234
ECR_REGISTRY/kubernetes-eks-app/frontend:latest

---

## Horizontal Pod Autoscaler

The HPA automatically scales deployments based on CPU usage:

| Service | Min Replicas | Max Replicas | CPU Target |
|---|---|---|---|
| Frontend | 1 | 3 | 50% |
| Backend | 1 | 5 | 50% |

When CPU usage exceeds 50% Kubernetes automatically adds pods to handle the load. When usage drops pods are removed to save resources.

---

## Security Decisions

**Kubernetes Secrets** — database credentials are stored as Kubernetes Secrets and injected as environment variables at runtime. They are never hardcoded in manifests or application code.

**ConfigMaps** — non-sensitive configuration like database host and port are stored in ConfigMaps, keeping configuration separate from sensitive data.

**Internal services** — the database service has no external exposure. It is only accessible from within the cluster by the backend service.

---

## Future Improvements

- Deploy to EKS for a production-grade cloud deployment
- Add Helm charts for templating and environment management
- Replace emptyDir with a PersistentVolume for database storage so data survives pod restarts
- Add readiness and liveness probes to all deployments
- Add Prometheus and Grafana for cluster monitoring and alerting
- Add network policies to restrict pod-to-pod communication

---

## How to Tear Down

```bash
kubectl delete -f kubernetes/ --recursive
minikube stop
```

---

## Author

Patrick McGuffin
[GitHub](https://github.com/patrickmcguffin) | [LinkedIn](https://linkedin.com/in/patrickmcguffin/)