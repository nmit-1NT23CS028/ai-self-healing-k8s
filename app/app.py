"""
AI Self-Healing Kubernetes Platform
Advanced Edition — Real-time anomaly detection, auto-remediation simulation,
multi-pod orchestration monitoring with ML-based prediction engine.
"""
from flask import render_template
from flask import Flask, jsonify, request
import random
import time
import math
import json
import os
from datetime import datetime, timedelta
from collections import deque
import threading

app = Flask(__name__)

# ─── Simulated State ────────────────────────────────────────────────────────
class ClusterState:
    def __init__(self):
        self.tick = 0
        self.pods = {
            f"pod-{i}": {
                "name": f"healing-pod-{i:03d}",
                "status": "Running",
                "restarts": 0,
                "cpu": 30 + random.randint(0, 20),
                "memory": 40 + random.randint(0, 15),
                "age": random.randint(1, 720),
                "node": f"node-{(i % 3) + 1}",
            }
            for i in range(1, 7)
        }
        self.events = deque(maxlen=50)
        self.healer_log = deque(maxlen=20)
        self.anomaly_history = deque(maxlen=60)
        self.healing_count = 0
        self.uptime_start = datetime.now()
        self.cluster_health = 100.0
        self.lock = threading.Lock()
        self._inject_scenario_at = None
        self._scenario_type = None

    def tick_update(self):
        with self.lock:
            self.tick += 1
            t = self.tick

            # Inject anomaly scenario every ~45 ticks
            if t % 45 == 0:
                self._inject_scenario_at = t + random.randint(2, 8)
                self._scenario_type = random.choice([
                    "OOMKilled", "CrashLoopBackOff", "CPUThrottle",
                    "NetworkLatency", "DiskPressure", "NodeNotReady"
                ])

            anomaly_detected = False

            for pod_id, pod in self.pods.items():
                # Sinusoidal base load + noise
                base_cpu = 35 + 20 * math.sin(t * 0.08 + hash(pod_id) % 10)
                base_mem = 45 + 15 * math.sin(t * 0.05 + hash(pod_id) % 7)

                # Inject scenario
                if (self._inject_scenario_at and
                        t >= self._inject_scenario_at and
                        pod_id == "pod-2"):
                    scenario = self._scenario_type
                    if scenario == "OOMKilled":
                        pod["memory"] = min(98, pod["memory"] + 25)
                        if pod["memory"] > 92:
                            pod["status"] = "OOMKilled"
                            anomaly_detected = True
                    elif scenario == "CrashLoopBackOff":
                        pod["status"] = "CrashLoopBackOff"
                        pod["restarts"] += 1
                        anomaly_detected = True
                    elif scenario == "CPUThrottle":
                        pod["cpu"] = min(99, pod["cpu"] + 35)
                        anomaly_detected = True
                    elif scenario == "NetworkLatency":
                        pod["status"] = "Warning"
                        anomaly_detected = True
                    elif scenario == "DiskPressure":
                        pod["status"] = "Pending"
                        anomaly_detected = True
                    elif scenario == "NodeNotReady":
                        pod["status"] = "NodeLost"
                        anomaly_detected = True

                    # Auto-heal after 8 ticks
                    if t >= self._inject_scenario_at + 8:
                        pod["status"] = "Running"
                        pod["cpu"] = base_cpu + random.uniform(-5, 5)
                        pod["memory"] = base_mem + random.uniform(-5, 5)
                        self.healing_count += 1
                        heal_msg = {
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "action": f"Auto-healed {pod['name']}",
                            "type": scenario,
                            "result": "✓ Recovered",
                            "duration_ms": random.randint(120, 890),
                        }
                        self.healer_log.appendleft(heal_msg)
                        self.events.appendleft({
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "level": "INFO",
                            "msg": f"[AI-Healer] Remediated {scenario} on {pod['name']} in {heal_msg['duration_ms']}ms",
                        })
                        self._inject_scenario_at = None
                else:
                    pod["cpu"] = max(5, min(95, base_cpu + random.uniform(-4, 4)))
                    pod["memory"] = max(5, min(95, base_mem + random.uniform(-3, 3)))
                    pod["age"] += 1

                # Random minor events
                if random.random() < 0.01 and pod["status"] == "Running":
                    self.events.appendleft({
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "level": "DEBUG",
                        "msg": f"Probe check OK on {pod['name']} — latency {random.randint(1,12)}ms",
                    })

            # Anomaly detection log
            if anomaly_detected:
                self.events.appendleft({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "level": "WARN",
                    "msg": f"[ML-Detector] Anomaly signature detected: {self._scenario_type} — initiating remediation",
                })

            # Cluster health score
            bad = sum(1 for p in self.pods.values() if p["status"] != "Running")
            self.cluster_health = max(0, 100 - bad * 15 - random.uniform(0, 2))

            avg_cpu = sum(p["cpu"] for p in self.pods.values()) / len(self.pods)
            avg_mem = sum(p["memory"] for p in self.pods.values()) / len(self.pods)
            self.anomaly_history.append({
                "t": t,
                "cpu": round(avg_cpu, 1),
                "mem": round(avg_mem, 1),
                "health": round(self.cluster_health, 1),
            })


cluster = ClusterState()

def background_ticker():
    while True:
        cluster.tick_update()
        time.sleep(2)

ticker_thread = threading.Thread(target=background_ticker, daemon=True)
ticker_thread.start()


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/api/cluster")
def api_cluster():
    with cluster.lock:
        uptime_s = int((datetime.now() - cluster.uptime_start).total_seconds())
        h, rem = divmod(uptime_s, 3600)
        m, s = divmod(rem, 60)
        return jsonify({
            "health": round(cluster.cluster_health, 1),
            "uptime": f"{h:02d}:{m:02d}:{s:02d}",
            "healings": cluster.healing_count,
            "pods": list(cluster.pods.values()),
            "events": list(cluster.events)[:15],
            "healer_log": list(cluster.healer_log)[:8],
            "history": list(cluster.anomaly_history),
            "tick": cluster.tick,
        })


@app.route("/api/metrics")
def api_metrics():
    with cluster.lock:
        avg_cpu = sum(p["cpu"] for p in cluster.pods.values()) / len(cluster.pods)
        avg_mem = sum(p["memory"] for p in cluster.pods.values()) / len(cluster.pods)
        running = sum(1 for p in cluster.pods.values() if p["status"] == "Running")
        return jsonify({
            "cpu_usage": round(avg_cpu, 1),
            "memory_usage": round(avg_mem, 1),
            "pods_running": running,
            "pods_total": len(cluster.pods),
            "cluster_health": round(cluster.cluster_health, 1),
        })


@app.route("/api/trigger-anomaly", methods=["POST"])
def trigger_anomaly():
    scenario = request.json.get("type", "CrashLoopBackOff")
    with cluster.lock:
        cluster._inject_scenario_at = cluster.tick + 1
        cluster._scenario_type = scenario
        cluster.events.appendleft({
            "time": datetime.now().strftime("%H:%M:%S"),
            "level": "WARN",
            "msg": f"[Manual] Anomaly triggered: {scenario}",
        })
    return jsonify({"status": "triggered", "scenario": scenario})


@app.route("/crash")
def crash():
    time.sleep(20)
    return "System Delay Simulated"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
