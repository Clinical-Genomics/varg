import pytest
from varg.utils.write_report import ReportWriter

def test_instatiate(intersection, compare_fields):

    writer = ReportWriter(intersection, compare_fields)
    assert isinstance(writer.aggr_stats.stats, dict)
