"""
AI Engine — Anomaly Detection & Prediction
Uses a lightweight Z-score based statistical model to flag anomalies,
with an Isolation Forest for multi-dimensional outlier scoring.

In production, swap with a trained model loaded via joblib:
    model = joblib.load('models/isolation_forest.pkl')
"""

import math
import random
from collections import deque


class AnomalyDetector:
    """
    Rolling Z-score anomaly detector.
    Signals when a metric exceeds N standard deviations from the rolling mean.
    """

    def __init__(self, window: int = 30, threshold: float = 2.5):
        self.window = window
        self.threshold = threshold
        self._history: deque = deque(maxlen=window)

    def score(self, value: float) -> dict:
        self._history.append(value)
        if len(self._history) < 5:
            return {"anomaly": False, "z_score": 0.0, "value": value}

        mean = sum(self._history) / len(self._history)
        variance = sum((x - mean) ** 2 for x in self._history) / len(self._history)
        std = math.sqrt(variance) or 1e-9

        z = abs(value - mean) / std
        return {
            "anomaly": z > self.threshold,
            "z_score": round(z, 3),
            "mean": round(mean, 2),
            "std": round(std, 2),
            "value": value,
        }


class IsolationForestLite:
    """
    Lightweight simulation of Isolation Forest scoring.
    In production use: sklearn.ensemble.IsolationForest
    """

    def predict(self, cpu: float, memory: float) -> float:
        """Returns anomaly score 0-1. Higher = more anomalous."""
        score = 0.0
        if cpu > 85:
            score += (cpu - 85) / 15 * 0.5
        if memory > 85:
            score += (memory - 85) / 15 * 0.5
        if cpu > 90 and memory > 80:
            score += 0.2  # Compound spike
        return min(1.0, round(score + random.uniform(-0.02, 0.02), 3))


# Singleton instances
cpu_detector = AnomalyDetector(window=30, threshold=2.5)
mem_detector = AnomalyDetector(window=30, threshold=2.5)
isolation_forest = IsolationForestLite()
