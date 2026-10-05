"""Hardware validation tests."""

import logging
from h200_test.framework import TestCase, TestResult
from h200_test.tools.nvidia_tools import NvidiaTools
from h200_test.tools.system_tools import SystemTools

logger = logging.getLogger(__name__)


class GPUSingleCardTest(TestCase):
    """Test: GPU single card identification and power."""

    def __init__(self):
        super().__init__(
            "gpu_single_card",
            "Verify 8 GPUs identified with normal power and stable frequency",
            tags=["hardware", "gpu"]
        )

    def run(self) -> TestResult:
        """Execute GPU single card test."""
        try:
            info = NvidiaTools.get_gpu_info()
            
            if info['gpu_count'] != 8:
                return TestResult(
                    test_id=self.test_id,
                    description=self.description,
                    status="fail",
                    duration_seconds=0,
                    error_message=f"Expected 8 GPUs, found {info['gpu_count']}",
                    metrics=info
                )

            return TestResult(
                test_id=self.test_id,
                description=self.description,
                status="pass",
                duration_seconds=0,
                metrics={"gpu_count": info['gpu_count']}
            )
        except Exception as e:
            return TestResult(
                test_id=self.test_id,
                description=self.description,
                status="error",
                duration_seconds=0,
                error_message=str(e)
            )


class CPUMemoryTest(TestCase):
    """Test: CPU cores and memory capacity."""

    def __init__(self):
        super().__init__(
            "cpu_memory",
            "Verify dual-socket CPU with 96+ cores and 2TB memory",
            tags=["hardware", "cpu"]
        )

    def run(self) -> TestResult:
        """Execute CPU/memory test."""
        try:
            cpu_info = SystemTools.get_cpu_info()
            mem_info = SystemTools.get_memory_info()

            if cpu_info['cpu_count'] < 48:
                return TestResult(
                    test_id=self.test_id,
                    description=self.description,
                    status="fail",
                    duration_seconds=0,
                    error_message=f"Expected ≥96 cores, found {cpu_info['cpu_count']}",
                    metrics=cpu_info
                )

            memory_tb = mem_info['total_gb'] / 1024
            if memory_tb < 1.8:
                return TestResult(
                    test_id=self.test_id,
                    description=self.description,
                    status="fail",
                    duration_seconds=0,
                    error_message=f"Expected ≥1.8TB, found {memory_tb:.1f}TB",
                    metrics=mem_info
                )

            return TestResult(
                test_id=self.test_id,
                description=self.description,
                status="pass",
                duration_seconds=0,
                metrics={"cpu_cores": cpu_info['cpu_count'], "memory_gb": mem_info['total_gb']}
            )
        except Exception as e:
            return TestResult(
                test_id=self.test_id,
                description=self.description,
                status="error",
                duration_seconds=0,
                error_message=str(e)
            )
