# ⎈ AI Self-Healing Kubernetes Platform — Advanced Edition

> **Production-grade autonomous cluster management** with real-time ML anomaly detection, chaos engineering, and automated remediation.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.29-326CE5?style=flat-square&logo=kubernetes)
![Docker](https://img.shields.io/badge/Docker-Multi--stage-2496ED?style=flat-square&logo=docker)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?style=flat-square&logo=scikit-learn)

---

## 🧠 Architecture

```
┌────────────────────────────────────────────────────┐
│              AI Self-Healing K8s Platform           │
│                                                    │
│  ┌──────────┐    ┌──────────────┐    ┌──────────┐  │
│  │  Flask   │───▶│ AI Anomaly   │───▶│  Auto    │  │
│  │Dashboard │    │  Detector    │    │  Healer  │  │
│  └──────────┘    │ (Z-score +   │    │(Playbook │  │
│       │          │  Iso Forest) │    │ Engine)  │  │
│       │          └──────────────┘    └──────────┘  │
│       ▼                                    │       │
│  ┌──────────────────────────────────────┐  │       │
│  │     Kubernetes Cluster (Simulated)   │◀─┘       │
│  │  pod-001  pod-002  pod-003           │          │
│  │  pod-004  pod-005  pod-006           │          │
│  └──────────────────────────────────────┘          │
└────────────────────────────────────────────────────┘
```

## ✨ Key Features

| Feature | v1 (Basic) | v2 (Advanced) |
|---------|-----------|---------------|
| Dashboard | Static HTML | Real-time animated command center |
| Metrics | CPU + Memory | CPU, Memory, Health Score, Per-pod |
| Anomaly Detection | ❌ | ✅ Z-score + Isolation Forest |
| Auto-Healing | ❌ | ✅ 6-scenario remediation playbook |
| Chaos Engineering | ❌ | ✅ 6 injectable failure types |
| Pod Visibility | ❌ | ✅ 6 pods with status + metrics |
| Historical Chart | ❌ | ✅ Rolling 30-point time-series |
| Event Stream | ❌ | ✅ Live log with severity levels |
| Kubernetes Config | Basic | HPA + PDB + NetworkPolicy + Security |
| Docker | Single-stage | Multi-stage (builder + production) |
| Security | None | Non-root user, ReadOnly FS, dropped caps |

## 🚀 Quick Start

### Local (Docker)
```bash
# Build
docker build -f docker/Dockerfile -t ai-healing-app:2.0 .

# Run
docker run -p 5000:5000 ai-healing-app:2.0

# Visit
open http://localhost:5000
```

### Kubernetes
```bash
# Apply all manifests
kubectl apply -f k8s/

# Watch pods
kubectl get pods -n ai-healing -w

# Get dashboard URL
kubectl get svc -n ai-healing
```

### Local Dev
```bash
pip install -r app/requirements.txt
cd app && python app.py
```

## 🎯 Supported Anomaly Scenarios

| Scenario | Trigger | Remediation |
|----------|---------|-------------|
| `OOMKilled` | Memory > 92% | Scale memory limits +25%, restart |
| `CrashLoopBackOff` | Repeated exit | Exponential backoff + probe tweak |
| `CPUThrottle` | CPU > 90% | HPA scale-out + limit adjustment |
| `NetworkLatency` | High inter-pod RTT | Sidecar proxy restart + reroute |
| `DiskPressure` | Node disk full | PVC expand + log rotation |
| `NodeNotReady` | Node unreachable | Cordon + drain + reschedule |

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Live dashboard |
| GET | `/api/cluster` | Full cluster state (JSON) |
| GET | `/api/metrics` | Aggregated metrics |
| POST | `/api/trigger-anomaly` | Inject failure scenario |

### Trigger anomaly via curl:
```bash
curl -X POST http://localhost:5000/api/trigger-anomaly \
  -H "Content-Type: application/json" \
  -d '{"type": "OOMKilled"}'
```

## 🏗️ Project Structure

```
ai-self-healing-k8s/
├── app/
│   ├── app.py              # Flask API + cluster simulation
│   ├── dashboard.html      # Real-time UI (no framework needed)
│   └── requirements.txt
├── ai_engine/
│   └── detector.py         # Z-score + Isolation Forest anomaly detection
├── auto_healer/
│   └── healer.py           # 6-scenario remediation playbook engine
├── docker/
│   └── Dockerfile          # Multi-stage production build
├── k8s/
│   ├── deployment.yaml     # Deployment + HPA + PDB
│   └── service.yaml        # Service + NetworkPolicy
└── README.md
```

## 🔮 Production Extensions

- **Prometheus + Grafana** — Replace simulated metrics with real scraping
- **Kubernetes Operator** — Convert healer to a CRD-based operator pattern
- **Trained ML Model** — Load `IsolationForest` from `joblib` with real historical data
- **Slack/PagerDuty** — Wire healer actions to alert channels
- **RBAC** — Add `ServiceAccount` + `ClusterRole` for kubectl access from within pods

---

*Built to demonstrate: Python · Flask · Kubernetes · Docker · ML (scikit-learn) · Real-time dashboards · Chaos Engineering*
