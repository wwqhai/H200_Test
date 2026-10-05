"""NVIDIA GPU tools and utilities."""

import subprocess
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class NvidiaTools:
    """Wrapper for nvidia-smi and CUDA tools."""

    @staticmethod
    def run_command(cmd: List[str]) -> str:
        """Run command and return output."""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(cmd)}")
            raise
        except Exception as e:
            logger.error(f"Failed to run command {' '.join(cmd)}: {e}")
            raise

    @staticmethod
    def get_gpu_count() -> int:
        """Get number of GPUs."""
        try:
            output = NvidiaTools.run_command(['nvidia-smi', '--query-gpu=count', '--format=csv,noheader'])
            count = int(output.strip().split('\n')[0])
            return count
        except Exception as e:
            logger.error(f"Failed to get GPU count: {e}")
            return 0

    @staticmethod
    def get_gpu_info() -> Dict:
        """Get detailed GPU information."""
        info = {'gpu_count': 0, 'gpus': []}
        try:
            output = NvidiaTools.run_command([
                'nvidia-smi',
                '--query-gpu=index,name,driver_version',
                '--format=csv,noheader'
            ])
            for line in output.strip().split('\n'):
                if line:
                    parts = [p.strip() for p in line.split(',')]
                    gpu_info = {
                        'index': parts[0],
                        'name': parts[1] if len(parts) > 1 else 'unknown',
                        'driver_version': parts[2] if len(parts) > 2 else 'unknown'
                    }
                    info['gpus'].append(gpu_info)
            info['gpu_count'] = len(info['gpus'])
            return info
        except Exception as e:
            logger.error(f"Failed to get GPU info: {e}")
            return info

    @staticmethod
    def get_gpu_stats() -> Dict:
        """Get current GPU statistics."""
        stats = {'gpus': []}
        try:
            output = NvidiaTools.run_command([
                'nvidia-smi',
                '--query-gpu=index,power.draw,clocks.current.graphics,temperature.gpu',
                '--format=csv,noheader'
            ])
            for line in output.strip().split('\n'):
                if line:
                    parts = [p.strip() for p in line.split(',')]
                    gpu_stats = {
                        'index': parts[0],
                        'power_draw_w': float(parts[1].split()[0]) if len(parts) > 1 else 0,
                        'clock_mhz': int(parts[2]) if len(parts) > 2 else 0,
                        'temperature_c': int(parts[3]) if len(parts) > 3 else 0
                    }
                    stats['gpus'].append(gpu_stats)
            return stats
        except Exception as e:
            logger.error(f"Failed to get GPU stats: {e}")
            return stats
