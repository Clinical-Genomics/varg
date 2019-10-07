""" varg root command """
import logging
import importlib

import click

from varg.utils.vcf_handler import VCFHandler
from varg.utils.write_report import ReportWriter
from varg.resources import path_to_compare_fields

LOG = logging.getLogger(__name__)

@click.command('compare')
@click.option('-t', '--truth-set', type=click.Path(exists=True), required=True,
              help="VCF with positive controls")
@click.option('-v', '--variants', type=click.Path(exists=True),
              help="VCF with variants that should be compared against truth-set")
@click.option('-m', '--samples-map', type=str,
              help="Specification of what samples that should be compared. E.g. 'sample1=proband,sample2=mother'")
@click.option('-f', '--vcf-fields', type=click.Path(exists=True),
              help="Path compare-specifications .py file")
@click.pass_context
def compare(context, truth_set, variants, samples_map, vcf_fields):

    truth_vcf = VCFHandler(truth_set)
    bench_vcf = VCFHandler(variants)

    LOG.info("Comparing %s and %s", truth_vcf.file_path, bench_vcf.file_path)
    LOG.info("Number of records in %s: %s", truth_vcf.file_path, truth_vcf.length)
    LOG.info("Number of records in %s: %s", bench_vcf.file_path, bench_vcf.length)

    if samples_map:
        samples_map = parse_samples_map(samples_map)
    else:
        samples_map = ','.join(['='.join((sample_1, sample_2))
                                for sample_1, sample_2
                                in zip(truth_vcf.samples, bench_vcf.samples)])
        samples_map = parse_samples_map(samples_map)

    intersection = truth_vcf.intersection(vcf=bench_vcf, samples_map=samples_map)

    vcf_fields_path = vcf_fields or path_to_compare_fields
    vcf_fields = get_dynamic_module(vcf_fields_path)

    report_writer = ReportWriter(intersection, vcf_fields)
    report_writer.write()


def parse_samples_map(samples_map_str):

    samples_map = [(sample_pair.split('=')[0], sample_pair.split('=')[1])
                   for sample_pair in samples_map_str.split(',')]
    samples_str = '\t'.join(['/'.join((samples[0], samples[1])) for samples in samples_map])
    LOG.info(f"Comparing samples: {samples_str}")
    return samples_map


def get_dynamic_module(module_path):

    spec = importlib.util.spec_from_file_location("compare_fields", module_path)
    compare_fields_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compare_fields_module)

    return compare_fields_module.COMPARE_FIELDS
