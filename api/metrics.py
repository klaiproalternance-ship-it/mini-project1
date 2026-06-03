import psutil

def get_system_metrics() -> dict:
    """
    Returns a snapshot of the current machine's CPU percentage, 
    memory percentage, memory usage in GB, and disk usage percentage.
    """
    # Non-blocking CPU check
    cpu = psutil.cpu_percent(interval=None)
    
    # Memory metrics
    vm = psutil.virtual_memory()
    # Convert memory used from bytes to GB
    memory_used_gb = round(vm.used / (1024 ** 3), 2)
    
    # Disk metrics (root partition)
    disk = psutil.disk_usage('/')
    
    return {
        "cpu_percent": cpu,
        "memory_percent": vm.percent,
        "memory_used_gb": memory_used_gb,
        "disk_percent": disk.percent
    }
