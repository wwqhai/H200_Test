"""Core testing framework for H200 cluster validation."""

import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """Test execution modes."""
    SEQUENTIAL = "sequential"
    ISOLATED_PARALLEL = "isolated_parallel"
    HYBRID = "hybrid"


@dataclass
class TestResult:
    """Result of a single test execution."""
    test_id: str
    description: str
    status: str  # "pass", "fail", "skip", "error"
    duration_seconds: float
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = None
    timestamp: str = None

    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class TestCase(ABC):
    """Base class for test cases."""

    def __init__(self, test_id: str, description: str, tags: List[str] = None):
        self.test_id = test_id
        self.description = description
        self.tags = tags or []

    @abstractmethod
    def run(self) -> TestResult:
        """Execute the test and return result."""
        pass

    def setup(self):
        """Optional setup before test."""
        pass

    def teardown(self):
        """Optional cleanup after test."""
        pass


class TestFramework:
    """Framework for orchestrating H200 cluster tests."""

    def __init__(self, execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL,
                 max_workers: int = 8, output_dir: str = "reports"):
        self.execution_mode = execution_mode
        self.max_workers = max_workers
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.tests: List[TestCase] = []
        self.results: List[TestResult] = []

    def register_test(self, test: TestCase):
        """Register a test case."""
        self.tests.append(test)
        logger.info(f"Registered test: {test.test_id}")

    def register_tests(self, tests: List[TestCase]):
        """Register multiple test cases."""
        for test in tests:
            self.register_test(test)

    def discover_tests(self, test_dir: str, pattern: str = "test_*.py"):
        """Discover tests from a directory (placeholder for dynamic discovery)."""
        logger.info(f"Discovering tests from {test_dir} with pattern {pattern}")

    def filter_by_tags(self, tags: List[str]) -> List[TestCase]:
        """Filter tests by tags."""
        filtered = []
        for test in self.tests:
            if any(tag in test.tags for tag in tags):
                filtered.append(test)
        return filtered

    def _run_test(self, test: TestCase) -> TestResult:
        """Run a single test with error handling."""
        logger.info(f"Running test: {test.test_id}")
        start_time = time.time()

        try:
            test.setup()
            result = test.run()
            test.teardown()
            result.duration_seconds = time.time() - start_time
            return result
        except Exception as e:
            logger.error(f"Test {test.test_id} failed: {str(e)}")
            return TestResult(
                test_id=test.test_id,
                description=test.description,
                status="error",
                duration_seconds=time.time() - start_time,
                error_message=str(e)
            )

    def run_sequential(self) -> List[TestResult]:
        """Run tests sequentially (safe, but slow)."""
        logger.info("Starting sequential test execution")
        results = []
        for test in self.tests:
            result = self._run_test(test)
            results.append(result)
            logger.info(f"  [{result.status.upper()}] {test.test_id} ({result.duration_seconds:.2f}s)")
        return results

    def run_isolated_parallel(self) -> List[TestResult]:
        """Run tests in parallel with isolation (fast, requires careful coordination)."""
        logger.info(f"Starting isolated parallel execution with {self.max_workers} workers")
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_test = {executor.submit(self._run_test, test): test for test in self.tests}

            for future in as_completed(future_to_test):
                test = future_to_test[future]
                result = future.result()
                results.append(result)
                logger.info(f"  [{result.status.upper()}] {test.test_id} ({result.duration_seconds:.2f}s)")

        return results

    def run_hybrid(self) -> List[TestResult]:
        """Run tests in hybrid mode (parallel hardware verification, sequential others)."""
        logger.info("Starting hybrid test execution")
        results = []

        # For MVP, treat as sequential - full hybrid scheduling deferred
        return self.run_sequential()

    def run(self) -> List[TestResult]:
        """Execute tests according to execution mode."""
        logger.info(f"Running {len(self.tests)} tests in {self.execution_mode.value} mode")

        if self.execution_mode == ExecutionMode.SEQUENTIAL:
            self.results = self.run_sequential()
        elif self.execution_mode == ExecutionMode.ISOLATED_PARALLEL:
            self.results = self.run_isolated_parallel()
        elif self.execution_mode == ExecutionMode.HYBRID:
            self.results = self.run_hybrid()

        return self.results

    def generate_report(self, format_type: str = "json") -> str:
        """Generate test report."""
        if not self.results:
            logger.warning("No test results to report")
            return ""

        passed = sum(1 for r in self.results if r.status == "pass")
        failed = sum(1 for r in self.results if r.status == "fail")
        errors = sum(1 for r in self.results if r.status == "error")
        total = len(self.results)
        pass_rate = (passed / total * 100) if total > 0 else 0

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate_percent": pass_rate
            },
            "tests": [r.to_dict() for r in self.results]
        }

        if format_type == "json":
            report_str = json.dumps(report, indent=2)
        else:
            report_str = self._format_text_report(report)

        return report_str

    def _format_text_report(self, report: dict) -> str:
        """Format report as plain text."""
        lines = [
            "=" * 80,
            "H200 Test System Report",
            "=" * 80,
            f"Timestamp: {report['timestamp']}",
            "",
            "Summary:",
            f"  Total: {report['summary']['total']}",
            f"  Passed: {report['summary']['passed']}",
            f"  Failed: {report['summary']['failed']}",
            f"  Errors: {report['summary']['errors']}",
            f"  Pass Rate: {report['summary']['pass_rate_percent']:.1f}%",
            "",
            "Results:",
        ]

        for test in report['tests']:
            status = test['status'].upper()
            lines.append(f"  [{status:5}] {test['test_id']:30} ({test['duration_seconds']:6.2f}s)")
            if test['error_message']:
                lines.append(f"           Error: {test['error_message']}")

        lines.append("=" * 80)
        return "\n".join(lines)

    def save_report(self, filename: str = "report.json"):
        """Save report to file."""
        report = self.generate_report(format_type="json")
        filepath = self.output_dir / filename
        filepath.write_text(report)
        logger.info(f"Report saved to {filepath}")
        return filepath

    def print_summary(self):
        """Print test execution summary."""
        if not self.results:
            logger.warning("No test results")
            return

        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "pass")
        failed = sum(1 for r in self.results if r.status == "fail")
        errors = sum(1 for r in self.results if r.status == "error")
        total_time = sum(r.duration_seconds for r in self.results)

        logger.info("-" * 60)
        logger.info(f"Test Execution Summary")
        logger.info(f"  Total: {total} | Passed: {passed} | Failed: {failed} | Errors: {errors}")
        logger.info(f"  Total Time: {total_time:.2f}s")
        logger.info(f"  Pass Rate: {(passed/total*100):.1f}%")
        logger.info("-" * 60)
