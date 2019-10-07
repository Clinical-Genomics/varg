""" varg root command """
import logging

import click
import coloredlogs

from varg import __version__
from .compare import compare as compare_command


LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

@click.group()
@click.option('--loglevel', default='INFO', type=click.Choice(LOG_LEVELS))
@click.version_option(__version__)
@click.pass_context
def root_command(context, loglevel):
    """Variants-Validation-Report-Generator base command"""
    coloredlogs.install(level = loglevel)
    LOG.info("Running varg")

root_command.add_command(compare_command)
