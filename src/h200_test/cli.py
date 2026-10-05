"""Command-line interface for H200 test system."""

import click
import logging
from pathlib import Path
from .framework import TestFramework, ExecutionMode
from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def cli(ctx):
    """H200 AI Cluster Testing and Validation System."""
    ctx.ensure_object(dict)


@cli.command()
@click.option('--mode', type=click.Choice(['sequential', 'isolated_parallel', 'hybrid']),
              default='sequential', help='Test execution mode')
@click.option('--config', type=click.Path(exists=True), help='Configuration file (YAML)')
@click.option('--output-dir', type=click.Path(), default='reports', help='Output directory for reports')
@click.option('--max-workers', type=int, default=8, help='Max parallel workers')
@click.option('--tag', multiple=True, help='Filter tests by tags')
@click.pass_context
def start(ctx, mode, config, output_dir, max_workers, tag):
    """Start test execution."""
    # Load configuration
    cfg = Config(config)
    if config:
        cfg.load(config)

    # Override with CLI options
    if mode:
        cfg.set('execution_mode', mode)
    if output_dir:
        cfg.set('output_dir', output_dir)
    if max_workers:
        cfg.set('max_workers', max_workers)

    # Create framework
    execution_mode = ExecutionMode(cfg.get('execution_mode'))
    framework = TestFramework(
        execution_mode=execution_mode,
        max_workers=cfg.get('max_workers'),
        output_dir=cfg.get('output_dir')
    )

    click.echo(f"Starting H200 tests in {execution_mode.value} mode")
    click.echo(f"Output directory: {cfg.get('output_dir')}")

    # TODO: Register actual tests from validators
    click.echo("Note: No tests registered yet (integration in progress)")

    # Run tests
    results = framework.run()

    # Display summary
    framework.print_summary()

    # Save report
    framework.save_report('h200_test_report.json')
    click.echo(f"Report saved to {Path(cfg.get('output_dir')) / 'h200_test_report.json'}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='Configuration file to generate')
def init_config(config):
    """Initialize a configuration file with defaults."""
    if not config:
        config = 'h200_config.yaml'

    if Path(config).exists():
        click.confirm(f'{config} already exists. Overwrite?', abort=True)

    cfg = Config()
    cfg.save(config)
    click.echo(f"Configuration file created: {config}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='Configuration file')
def show_config(config):
    """Display current configuration."""
    cfg = Config(config)
    import yaml
    click.echo(yaml.dump(cfg.to_dict(), default_flow_style=False))


@cli.command()
@click.pass_context
def status(ctx):
    """Show framework status."""
    click.echo("H200 Test System Status")
    click.echo("  Framework: initialized")
    click.echo("  Tests registered: 0 (pending registration)")
    click.echo("  Ready for test execution")


def main():
    """Entry point."""
    cli()


if __name__ == '__main__':
    main()
