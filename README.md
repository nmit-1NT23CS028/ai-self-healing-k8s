
# AI Self-Healing Kubernetes Platform

**Description:**  
A cloud-native, Dockerized Flask microservice demonstrating **self-healing**, **auto-scaling**, and **CI/CD automation** using Kubernetes. Built to showcase **enterprise-grade microservice architecture** with optional AI-driven anomaly detection.

**Tech Stack:** Python · Flask · Kubernetes · Docker · scikit-learn  

---

## Features

- **Self-Healing:** Kubernetes automatically restarts unhealthy pods using liveness/readiness probes.  
- **Auto-Scaling:** Horizontal Pod Autoscaler (HPA) scales pods based on CPU usage.  
- **Containerized:** Dockerized for portability and reproducibility.  
- **CI/CD:** GitHub Actions builds, pushes, and deploys the app automatically.  
- **Persistent Storage (Optional):** PVCs for stateful pods.  
- **Simulated AI:** Optional anomaly detection using Z-score + Isolation Forest.  

---

## Project Structure

```

ai-self-healing-k8s/
├── app/
│   ├── app.py              # Flask API + simulated cluster
│   ├── dashboard.html      # Simple UI
│   └── requirements.txt
├── ai_engine/
│   └── detector.py         # Optional anomaly detection
├── auto_healer/
│   └── healer.py           # Auto-remediation engine
├── docker/
│   └── Dockerfile          # Docker image build
├── k8s/
│   ├── deployment.yaml     # Deployment + HPA
│   └── service.yaml        # Service definition
└── README.md

````

---

## Quick Start

### Local (Docker)
```bash
# Build Docker image
docker build -t ai-healing-app:latest .

# Run container
docker run -p 5000:5000 ai-healing-app:latest
````

Open browser: `http://localhost:5000`

---

### Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check pods and services
kubectl get pods
kubectl get svc
```

---

### Optional CI/CD

GitHub Actions can automatically:

1. Build Docker image
2. Push to Docker Hub
3. Deploy Kubernetes manifests

---
---

## Highlights

* Dockerized Flask microservice with **self-healing**
* **Auto-scaling** using Kubernetes HPA
* CI/CD automation with **GitHub Actions**
* Demonstrates skills in **cloud-native architecture, Kubernetes, Docker, and AI integration**

---

## Author

**Anshika – AI & Cloud Enthusiast**

*Built to demonstrate: Python · Flask · Kubernetes · Docker · ML (scikit-learn) · Real-time dashboards · Chaos Engineering*
