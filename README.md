# H200 Test System - MVP

Minimal Viable Product for H200 AI Cluster Testing and Validation.

## Quick Start

### Installation

```bash
cd h200-test-system
pip install -e .
# or
pip install -r requirements.txt
```

### Generate Default Config

```bash
h200-test init-config --config h200_config.yaml
```

### Run Tests (Sequential Mode)

```bash
h200-test start --config h200_config.yaml --mode sequential
```

### View Reports

```bash
cat reports/h200_test_report.json
```

## Structure

- `src/h200_test/framework.py` - Core TestFramework class with 3 execution modes
- `src/h200_test/config.py` - YAML configuration management
- `src/h200_test/cli.py` - Click-based CLI interface
- `src/h200_test/tools/` - Hardware tool wrappers
- `src/h200_test/validators/` - Test implementations

## Current MVP Scope

✓ Framework infrastructure with sequential/parallel/hybrid modes  
✓ CLI with start/config/status commands  
✓ YAML configuration management  
✓ GPU hardware validation (detect 8 GPUs)  
✓ CPU/Memory validation (detect 96+ cores, 2TB RAM)  
✓ Network interface detection  
✓ JSON/text report generation  

## Next Steps (Phase 2)

- Performance benchmarks (NCCL, IB bandwidth)
- Thermal/power monitoring
- Bare-metal lifecycle management
- REST API and Prometheus integration
