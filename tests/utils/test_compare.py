import pytest
from varg.utils.compare import Comparison

def test_instatiate(truth_set_path, vcf_record, compare_fields):

    # Given an two cyvcf2 records, vcf keys to be compared and a sample to sample
    # index map
    record_1 = vcf_record(truth_set_path, variant_type='SNV')
    record_2 = vcf_record(truth_set_path, variant_type='SV')
    sample_idx_map = ((0, 1, 2), (0, 1, 2))

    # WHEN making a comparison between records
    comp = Comparison(record_1, record_2,
                      vcf_keys=compare_fields,
                      sample_idx_map=sample_idx_map)

    # Then check that the records have been compared using the fields specified
    assert set(comp.comparison.keys()).issubset(set(compare_fields.keys()))
