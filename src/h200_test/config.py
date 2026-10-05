"""Configuration management for H200 test system."""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager."""

    DEFAULT_CONFIG = {
        "execution_mode": "sequential",
        "max_workers": 8,
        "output_dir": "reports",
        "timeouts": {
            "hardware_validation": 60,
            "performance_test": 600,
            "baremetal_lifecycle": 1800
        },
        "thresholds": {
            "gpu_temp_warning": 80,
            "gpu_temp_critical": 85,
            "nccl_bandwidth_min_gb_s": 200,
            "ib_400g_bandwidth_min_gb_s": 370,
            "ib_200g_bandwidth_min_gb_s": 180
        },
        "baseline": {
            "idle_duration_seconds": 30,
            "load_duration_seconds": 30
        }
    }

    def __init__(self, config_file: Optional[str] = None):
        self.config = self.DEFAULT_CONFIG.copy()
        if config_file and Path(config_file).exists():
            self.load(config_file)

    def load(self, config_file: str) -> None:
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r') as f:
                user_config = yaml.safe_load(f) or {}
            # Deep merge user config with defaults
            self._merge_config(self.config, user_config)
            logger.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.error(f"Failed to load config file {config_file}: {e}")
            raise

    def _merge_config(self, base: Dict, override: Dict) -> None:
        """Recursively merge override config into base."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation (e.g., 'thresholds.gpu_temp_warning')."""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot notation."""
        keys = key.split(".")
        target = self.config
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    def to_dict(self) -> Dict:
        """Get full configuration as dictionary."""
        return self.config

    def save(self, output_file: str) -> None:
        """Save current configuration to YAML file."""
        with open(output_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        logger.info(f"Configuration saved to {output_file}")
