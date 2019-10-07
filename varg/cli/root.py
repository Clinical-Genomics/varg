""" varg root command """
import logging

import click
import yaml
import coloredlogs

from .compare import compare as compare_command

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

@click.group()
@click.option('--loglevel', default='INFO', type=click.Choice(LOG_LEVELS))
@click.option('-c', '--config-file', type=click.Path(exists=True),
              help='configuration file')
@click.pass_context
def root_command(context, loglevel, config_file):
    """Variants-Validation-Report-Generator base command"""
    coloredlogs.install(level = loglevel)
    LOG.info("Running VARG")
    varg_configs = {}
    if config_file is not None:
        varg_configs = yaml.load(config_file)
    context.obj = varg_configs
    
root_command.add_command(compare_command)
