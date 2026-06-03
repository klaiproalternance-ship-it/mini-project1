import sys
import os

# Add the devops-monitor folder to PYTHONPATH to import api modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from api.metrics import get_system_metrics

def test_get_system_metrics():
    metrics = get_system_metrics()
    
    # Verify dict contains keys
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "disk_percent" in metrics
    assert "memory_used_gb" in metrics
    
    # Verify values are between 0 and 100 for percentages
    assert 0 <= metrics["cpu_percent"] <= 100
    assert 0 <= metrics["memory_percent"] <= 100
    assert 0 <= metrics["disk_percent"] <= 100
    assert metrics["memory_used_gb"] >= 0
