"""System utilities for hardware information."""

import subprocess
import os
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class SystemTools:
    """System-level tools for hardware probing."""

    @staticmethod
    def get_cpu_info() -> Dict:
        """Get CPU information."""
        try:
            import psutil
            return {
                'cpu_count': psutil.cpu_count(logical=False),
                'cpu_count_logical': psutil.cpu_count(logical=True),
                'freq_ghz': psutil.cpu_freq().current / 1000 if psutil.cpu_freq() else 0
            }
        except Exception as e:
            logger.error(f"Failed to get CPU info: {e}")
            return {'cpu_count': 0, 'cpu_count_logical': 0, 'freq_ghz': 0}

    @staticmethod
    def get_memory_info() -> Dict:
        """Get memory information."""
        try:
            import psutil
            mem = psutil.virtual_memory()
            return {
                'total_gb': mem.total / (1024**3),
                'available_gb': mem.available / (1024**3),
                'percent_used': mem.percent
            }
        except Exception as e:
            logger.error(f"Failed to get memory info: {e}")
            return {'total_gb': 0, 'available_gb': 0, 'percent_used': 0}

    @staticmethod
    def get_storage_info() -> Dict:
        """Get storage device information."""
        disks = []
        try:
            import psutil
            for partition in psutil.disk_partitions():
                disks.append({
                    'device': partition.device,
                    'name': partition.device.split('/')[-1],
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype
                })
            return {'disks': disks}
        except Exception as e:
            logger.error(f"Failed to get storage info: {e}")
            return {'disks': []}

    @staticmethod
    def get_network_info() -> Dict:
        """Get network interface information."""
        interfaces = []
        try:
            import psutil
            net_if_addrs = psutil.net_if_addrs()
            for interface, addrs in net_if_addrs.items():
                iface_type = "ethernet" if "eth" in interface or "enp" in interface else "other"
                interfaces.append({
                    'name': interface,
                    'type': iface_type,
                    'addresses': str(addrs)
                })
            return {'interfaces': interfaces}
        except Exception as e:
            logger.error(f"Failed to get network info: {e}")
            return {'interfaces': []}
