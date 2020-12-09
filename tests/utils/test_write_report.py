import pytest
from varg.utils.write_report import ReportWriter


def test_instatiate(intersection, compare_fields):

    writer = ReportWriter(intersection, compare_fields)
    assert isinstance(writer.aggr_stats.stats, dict)


def test_write(intersection, compare_fields):

    writer = ReportWriter(intersection, compare_fields)

    for record in writer.write():
        assert len(str(record).split("\n")) > 1
