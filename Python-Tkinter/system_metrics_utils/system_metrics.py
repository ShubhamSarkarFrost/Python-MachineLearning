import psutil
import  os


def get_cpu_usage():
    return  psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory_info = psutil.virtual_memory()
    total_gb = memory_info.total / (1024**3)
    used_gb = memory_info.used / (1024**3)
    return {
        "percent": memory_info.percent,
        "used_gb": used_gb,
        "total_gb": total_gb
    }

def get_disk_usage(path='/'):
    if os.name == 'nt':
        path = 'C:\\'  # Default to C: drive on Windows

    disk_info = psutil.disk_usage(path)
    total_gb = disk_info.total / (1024 ** 3)
    used_gb = disk_info.used / (1024 ** 3)
    return {
        "percent": disk_info.percent,
        "used_gb": used_gb,
        "total_gb": total_gb
    }

def get_network_activity():
    """
    Returns a dictionary with network activity details (bytes_sent_gb, bytes_recv_gb).
    """
    net_io = psutil.net_io_counters()
    bytes_sent_gb = net_io.bytes_sent / (1024**3)
    bytes_recv_gb = net_io.bytes_recv / (1024**3)
    return {
        "bytes_sent_gb": bytes_sent_gb,
        "bytes_recv_gb": bytes_recv_gb
    }