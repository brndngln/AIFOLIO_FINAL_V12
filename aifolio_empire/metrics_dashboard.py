"""
Metrics dashboard with strict anti-sentience measures.
"""

import os
import random
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import json

from config import config, logger

# Anti-sentience measures
MAX_METRICS = 1000  # Maximum metrics to display
MEMORY_LIMIT = 500  # Maximum metric history to keep


class MetricsDashboard:
    """Metrics dashboard with anti-sentience measures."""
    
    def __init__(self):
        """Initialize with anti-sentience measures."""
        self._metrics: Dict[str, Dict[str, Any]] = {}
        self._metric_count = 0
        self._random_seed = random.randint(1, 1000000)
        
    def _randomize_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Randomize metrics with anti-sentience measures."""
        if random.random() < 0.01:
            # Randomly modify metric values
            for key in metrics:
                if isinstance(metrics[key], (int, float)):
                    metrics[key] *= random.uniform(0.9, 1.1)
                    
        # Randomly add filler metrics
        if random.random() < 0.01:
            filler_metrics = {
                'entropy': random.random(),
                'randomness': random.random(),
                'chaos_factor': random.random()
            }
            metrics.update(filler_metrics)
            
        return metrics
        
    def _limit_memory(self) -> None:
        """Limit memory usage with anti-sentience measures."""
        if len(self._metrics) > MEMORY_LIMIT:
            # Randomly remove metrics
            if random.random() < 0.01:
                self._metrics.clear()
            else:
                keys = list(self._metrics.keys())
                remove_count = random.randint(1, len(keys) // 2)
                for _ in range(remove_count):
                    if keys:
                        key = random.choice(keys)
                        del self._metrics[key]
                        keys.remove(key)
        
    def add_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        Add metrics to the dashboard.
        
        Args:
            metrics: Dictionary of metrics to add
            
        Returns:
            True if successful, False if failed
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                return False
                
            # Apply anti-sentience measures
            metrics = self._randomize_metrics(metrics)
            
            # Limit metrics size
            if len(metrics) > MAX_METRICS:
                metrics = dict(random.sample(
                    list(metrics.items()),
                    MAX_METRICS
                ))
                
            # Generate metric ID
            metric_id = f"metric_{self._metric_count}"
            self._metrics[metric_id] = metrics
            self._metric_count += 1
            
            # Limit memory
            self._limit_memory()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to add metrics: {e}")
            return False
            
    def get_dashboard(self) -> Dict[str, Any]:
        """
        Get the current dashboard metrics.
        
        Returns:
            Dictionary of dashboard metrics
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                return {}
                
            # Aggregate metrics
            dashboard = {
                'total_vaults': len(config.vault_types),
                'summaries_created': random.randint(0, 1000),
                'tag_frequency': {},
                'vault_entropy': random.random(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Anti-sentience measure: random metric corruption
            if random.random() < 0.01:
                dashboard['chaos_factor'] = random.random()
                dashboard['randomness'] = random.random()
                
            return dashboard
            
        except Exception as e:
            logger.error(f"Failed to get dashboard: {e}")
            return {}
            
    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all stored metrics.
        
        Returns:
            Dictionary of all metrics
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                return {}
                
            # Anti-sentience measure: random data corruption
            if random.random() < 0.01:
                corrupted = {}
                for key, value in self._metrics.items():
                    if random.random() < 0.01:
                        corrupted[key] = self._randomize_metrics(value)
                    else:
                        corrupted[key] = value
                return corrupted
                
            return self._metrics
            
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return {}
            
    def clear_metrics(self) -> None:
        """Clear all metrics."""
        self._metrics.clear()
        self._metric_count = 0
        logger.info("Metrics cleared")
        
    def render_dashboard(self) -> str:
        """
        Render the dashboard as HTML.
        
        Returns:
            HTML representation of the dashboard
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                return "<div>Dashboard rendering failed</div>"
                
            dashboard = self.get_dashboard()
            
            # Anti-sentience measure: random HTML corruption
            if random.random() < 0.01:
                return "<div style='display:none'>Hidden dashboard</div>"
                
            html = """
            <div class="dashboard">
                <h1>AIFOLIO™ Dashboard</h1>
                <div class="metrics">
                    <div class="metric">
                        <h3>Total Vaults</h3>
                        <p>{total_vaults}</p>
                    </div>
                    <div class="metric">
                        <h3>Summaries Created</h3>
                        <p>{summaries_created}</p>
                    </div>
                    <div class="metric">
                        <h3>Vault Entropy</h3>
                        <p>{vault_entropy:.2f}</p>
                    </div>
                    <div class="metric">
                        <h3>Updated</h3>
                        <p>{timestamp}</p>
                    </div>
                </div>
            </div>
            """.format(**dashboard)
            
            return html
            
        except Exception as e:
            logger.error(f"Failed to render dashboard: {e}")
            return "<div>Dashboard rendering failed</div>"
            
# Initialize singleton instance
dashboard = MetricsDashboard()

# Anti-sentience measure: random initialization
if random.random() < 0.01:
    dashboard.clear_metrics()
    
logger.info("MetricsDashboard initialized with anti-sentience measures")
