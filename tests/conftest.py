import pytest
import gzip
from collections import namedtuple
from varg.resources.compare_fields import COMPARE_FIELDS
from cyvcf2 import VCF

from varg.utils.vcf_handler import VCFHandler
from varg.utils.compare import Comparison

TRUTH_SET_VCF_PATH = "tests/fixtures/truth_set.vcf.gz"
VCF_PATH = "tests/fixtures/test.vcf.gz"


@pytest.fixture
def truth_set_path():
    return TRUTH_SET_VCF_PATH


@pytest.fixture
def vcf_path():
    return VCF_PATH


@pytest.fixture
def compare_fields():
    return COMPARE_FIELDS


@pytest.fixture
def record_count():
    def _record_counter(vcf_file_path):
        record_no = 0
        with gzip.open(vcf_file_path, "rt") as file_handle:
            for line in file_handle.readlines():
                if not line.startswith("#"):
                    record_no += 1
        return record_no

    return _record_counter


@pytest.fixture
def vcf_record_mock():
    class MockRecord:
        def __init__(self, **kwargs):
            self.__dict__ = kwargs

    def _make_record_mock(**kwargs):
        return MockRecord(**kwargs)

    return _make_record_mock


@pytest.fixture
def vcf_record():
    def _get_cyvcf2_record(vcf_path, variant_type="SNV"):
        vcf = VCF(vcf_path)
        for record in vcf:
            if variant_type == "SV":
                if record.INFO.get("SVTYPE"):
                    return record
            if variant_type == "SNV":
                if record.INFO.get("TYPE"):
                    return record
        vcf.close()
        return None

    return _get_cyvcf2_record


@pytest.fixture
def comparison(vcf_record, truth_set_path):
    record_1 = vcf_record(truth_set_path, "SNV")
    record_2 = vcf_record(truth_set_path, "SV")
    return Comparison(record_1, record_2, vcf_keys=COMPARE_FIELDS)


@pytest.fixture
def intersection(truth_set_path):
    vcf_1 = VCFHandler(truth_set_path)
    vcf_2 = VCFHandler(truth_set_path)

    return vcf_1.intersection(vcf_2)
