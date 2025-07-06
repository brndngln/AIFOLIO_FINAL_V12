import logging
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from typing import List, Dict, Any, Optional, Union, cast

# For numpy ndarray typing
from numpy.typing import NDArray


class AIAnalyticsEngine:
    """
    Advanced AI analytics engine for AIFOLIO: clustering, anomaly detection, trend prediction, and actionable insights.
    Integrates with event and compliance logs, and can push results to Notion, Airtable, Slack, and dashboard.
    """

    def __init__(self) -> None:
        self.scaler: StandardScaler = StandardScaler()
        self.kmeans: Optional[KMeans] = None
        self.n_clusters: int = 5
        self.last_run: Optional[datetime] = None

    def run_clustering(self, event_data: List[Dict[str, Any]]) -> Optional[NDArray[Any]]:
        # event_data: list of dicts with numeric features
        if not event_data:
            return None
        X: NDArray[Any] = np.array(
            [
                [
                    float(e.get("revenue", 0)),
                    float(e.get("downloads", 0)),
                    float(e.get("rating", 0)),
                ]
                for e in event_data
            ]
        )
        X_scaled: NDArray[Any] = self.scaler.fit_transform(X)
        self.kmeans = KMeans(n_clusters=self.n_clusters, n_init=10)
        labels: NDArray[Any] = self.kmeans.fit_predict(X_scaled)
        return labels

    def detect_anomalies(self, event_data: List[Dict[str, Any]], threshold: float = 2.5) -> List[int]:
        # Simple anomaly detection using z-score
        if not event_data:
            return []
        X: NDArray[Any] = np.array(
            [
                [
                    float(e.get("revenue", 0)),
                    float(e.get("downloads", 0)),
                    float(e.get("rating", 0)),
                ]
                for e in event_data
            ]
        )
        X_scaled: NDArray[Any] = self.scaler.fit_transform(X)
        z_scores: NDArray[Any] = np.abs((X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0))
        anomalies: List[int] = [i for i, row in enumerate(z_scores) if any(row > threshold)]
        return anomalies

    def predict_trends(self, event_data: List[Dict[str, Any]], window: int = 7) -> Dict[str, str]:
        # Predict rising/falling trends using moving average
        if not event_data:
            return {}
        trends: Dict[str, str] = {}
        for key in ["revenue", "downloads", "rating"]:
            values: List[float] = [float(e.get(key, 0)) for e in event_data]
            if len(values) < window:
                trends[key] = "insufficient data"
                continue
            avg_now: float = float(np.mean(values[-window:]))
            avg_prev: float = (
                float(np.mean(values[-2 * window : -window]))
                if len(values) >= 2 * window
                else avg_now
            )
            if avg_now > avg_prev * 1.1:
                trends[key] = "rising"
            elif avg_now < avg_prev * 0.9:
                trends[key] = "falling"
            else:
                trends[key] = "stable"
        return trends

    def actionable_insights(self, event_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Generate actionable insights for dashboard and event router
        labels: Optional[NDArray[Any]] = self.run_clustering(event_data)
        anomalies: List[int] = self.detect_anomalies(event_data)
        trends: Dict[str, str] = self.predict_trends(event_data)
        insights: Dict[str, Any] = {
            "clusters": labels.tolist() if labels is not None else [],
            "anomalies": anomalies,
            "trends": trends,
            "timestamp": datetime.utcnow().isoformat(),
        }
        logging.info(f"AI Analytics Insights: {insights}")
        return insights
