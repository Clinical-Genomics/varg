import pytest
from varg.utils.vcf_handler import VCFHandler


def test_instatiate_VCFHandler(truth_set_path, record_count):

    # GIVEN a vcf-file path

    # WHEN instatiating a VCFhandler object
    vcf = VCFHandler(vcf_path=truth_set_path)

    # THEN the file-path and number of variants in vcf should be set
    assert vcf.file_path == truth_set_path
    assert vcf.length == record_count(truth_set_path)


def test_reset_vcf(truth_set_path, record_count):

    # GIVEN a vcf-file path and a VCFHandler object exhausted iterator
    vcf = VCFHandler(vcf_path=truth_set_path)
    records = [str(record) for record in vcf]
    assert len(records) == record_count(truth_set_path)

    # WHEN trying to iterate over vcf again
    records_empty = [str(record) for record in vcf]

    # THEN no records have been found
    assert len(records_empty) == 0

    # WHEN object is reset
    vcf._reset()

    # THEN it is iteratable from the beginning
    assert [str(record) for record in vcf] == records


def test_intersection(truth_set_path, vcf_path, record_count):

    # GIVEN two VCFHandler objects using the same vcf
    vcf_1 = VCFHandler(vcf_path=truth_set_path)
    vcf_2 = VCFHandler(vcf_path=truth_set_path)

    # WHEN intersection between files are searched
    intersection = vcf_1.intersection(vcf=vcf_2)

    # THEN the intersection are all variants in the vcf
    vcf_len = record_count(truth_set_path)
    vcf_count = 0
    for variant_pair in intersection:
        assert str(variant_pair[0]) == str(variant_pair[1])
        vcf_count += 1
    assert vcf_count == vcf_len


def test_sample_map():

    # GIVEN two lists of samples and one sample-to-sample list of tuples
    samples_1 = ("sample_1_1", "sample_1_2", "sample_1_3")
    samples_2 = ("sample_2_1", "sample_2_2", "sample_2_3")
    sample_map = (
        ("sample_1_1", "sample_2_3"),
        ("sample_1_2", "sample_2_2"),
        ("sample_1_3", "sample_2_1"),
    )
    # WHEN converting the samples map to a index map
    sample_idx_map = VCFHandler._samples_map(samples_1, samples_2, sample_map)

    # THEN it should be as expected
    assert sample_idx_map == ([0, 1, 2], [2, 1, 0])


def test_find_snv(truth_set_path, vcf_record_mock):

    # GIVEN a VCFHandler instance and a mocked cyvcf2 record of a non-existing snv
    vcf = VCFHandler(vcf_path=truth_set_path)
    vcf_record = vcf_record_mock(CHROM="X", POS=12348, REF="A", ALT="C")
    # WHEN trying to find record in vcf
    found_snv = vcf.find_snv(variant_record=vcf_record)
    # THEN nothing should have been found
    assert found_snv is None
    # GIVEN a SNV that exists in the vcf
    vcf_record = vcf_record_mock(CHROM="X", POS=99662167, REF="CA", ALT=["C"])
    # WHEN trying to find record in vcf
    found_snv = vcf.find_snv(variant_record=vcf_record)
    # THEN a SNV should have been found
    assert found_snv is not None


def test_find_similar_sv(truth_set_path, vcf_record_mock):

    # GIVEN a VCFHandler instance and a mocked cyvcf2 record of a non existing SV
    vcf = VCFHandler(vcf_path=truth_set_path)
    info = {"SVTYPE": "INV", "END": 23456}
    vcf_record = vcf_record_mock(CHROM="X", POS=12345, INFO=info)
    # WHEN searching for SV in vcf
    found_sv = vcf.find_similar_sv(vcf_record)
    # THEN nothing has been found
    assert found_sv is None
    # GIVEN a variant that exists, with different pos and end
    info = {"SVTYPE": "INV", "SVLEN": 100000}
    vcf_record = vcf_record_mock(CHROM="20", POS=57437611, INFO=info)
    # WHEN searching for SV in vcf
    found_sv = vcf.find_similar_sv(vcf_record)
    # THEN nothing has been found
    assert found_sv is not None
