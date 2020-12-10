import pytest
from copy import deepcopy

from varg.utils.compare import Comparison


def test_basic(truth_set_path, vcf_record, compare_fields):

    # Given an two cyvcf2 records, vcf keys to be compared and a sample to sample
    # index map
    record_1 = vcf_record(truth_set_path, variant_type="SNV")
    record_2 = vcf_record(truth_set_path, variant_type="SV")
    sample_idx_map = ((0, 1, 2), (0, 1, 2))

    # WHEN making a comparison between records
    comp = Comparison(
        record_1, record_2, vcf_keys=compare_fields, sample_idx_map=sample_idx_map
    )

    # Then check that the records have been compared using the fields specified
    assert set(comp.comparison.keys()).issubset(set(compare_fields.keys()))


def test_nonexisting_format_id(truth_set_path, vcf_record, compare_fields):

    modified_keys = deepcopy(compare_fields)
    modified_keys["SVLEN"] = {
        "column": "FORMAT",
        "ID": "SVLEN",
        "type_conv": lambda x: x,
    }
    record_1 = vcf_record(truth_set_path, variant_type="SNV")
    record_2 = vcf_record(truth_set_path, variant_type="SV")
    sample_idx_map = ((0, 1, 2), (0, 1, 2))

    # WHEN making a comparison between records
    comp = Comparison(
        record_1, record_2, vcf_keys=modified_keys, sample_idx_map=sample_idx_map
    )

    assert "SVLEN" not in comp.comparison.keys()
