import logging

from varg.utils.compare_mixin import CompareMixin

LOG = logging.getLogger(__name__)


class Comparison(CompareMixin):
    """Class for a comparison"""

    def __init__(self, record_1, record_2, vcf_keys, sample_idx_map=None):
        """ Compare two vcf records based on the keys specified in vcf_keys"""
        self.record_1 = record_1
        self.record_2 = record_2
        self.sample_idx_map = sample_idx_map
        comparison = dict()
        for key, value in vcf_keys.items():
            record_1_value = None
            record_2_value = None
            for alt_key in value["ID"]:
                if value.get("column", None) is None:
                    record_1_value, record_2_value = self._compare_columns(alt_key)
                elif value["column"] == "INFO":
                    if record_1_value is None:
                        record_1_value = record_1.INFO.get(alt_key)
                    if record_2_value is None:
                        record_2_value = record_2.INFO.get(alt_key)
                elif value["column"] == "FORMAT":
                    if record_1_value is None:
                        try:
                            record_1_value = record_1.format(alt_key)
                        except KeyError:
                            record_1_value = None
                    if record_2_value is None:
                        try:
                            record_2_value = record_2.format(alt_key)
                        except KeyError:
                            record_2_value = None
            if (record_1_value is not None) and (record_2_value is not None):
                conv_value_1 = value["type_conv"](record_1_value)
                conv_value_2 = value["type_conv"](record_2_value)
                if value.get("rearrange") and sample_idx_map:
                    conv_value_1 = self._rearrange_samples(
                        conv_value_1, sample_idx_map[0]
                    )
                    conv_value_2 = self._rearrange_samples(
                        conv_value_2, sample_idx_map[1]
                    )

                comp_eval = self._evaluate_comparison(
                    conv_value_1, conv_value_2, value_ids=value["ID"]
                )
                comparison[key] = (conv_value_1, conv_value_2, comp_eval)
            else:
                log_msg = (
                    f"key {' or '.join(value['ID'])} not found in one of the records"
                )
                LOG.debug(log_msg)

        self.comparison = comparison

    @staticmethod
    def _rearrange_samples(value_list, idx_list):
        return [value_list[idx] for idx in idx_list]

    def _compare_columns(self, column_id):
        """given a column name, find the value for the two records"""
        record_1_value = None
        record_2_value = None
        if column_id == "POS":
            record_1_value = self.record_1.POS
            record_2_value = self.record_2.POS
        if column_id == "QUAL":
            record_1_value = self.record_1.QUAL
            record_2_value = self.record_2.QUAL
        if column_id == "GT":
            record_1_value = self.record_1.genotypes
            record_2_value = self.record_2.genotypes
        if column_id == "CHROM":
            record_1_value = self.record_1.CHROM
            record_2_value = self.record_2.CHROM
        if column_id == "REF":
            record_1_value = self.record_1.REF
            record_2_value = self.record_2.REF
        if column_id == "ALT":
            record_1_value = self.record_1.ALT
            record_2_value = self.record_2.ALT
        if column_id == "ID":
            record_1_value = self.record_1.ID
            record_2_value = self.record_2.ID
        return record_1_value, record_2_value

    @staticmethod
    def _make_record_id(record):
        """Make record id based on CHROM POS REF ALT"""
        alt = record.ALT[0]
        ref = record.REF
        if len(alt) > 10:
            alt = alt[0:7] + "..."
        if len(ref) > 10:
            ref = ref[0:7] + "..."
        record_id = "{}_{}_{}_{}".format(record.CHROM, record.POS, ref, alt)
        return record_id

    def __str__(self):
        """String representation of object"""
        variant_id = self._make_record_id(self.record_1)
        comp_list = []
        for vcf_id, value in self.comparison.items():
            id_comp_str = f"{vcf_id}: {value[0]} , {value[1]} | {value[2]}"
            comp_list.append(id_comp_str)
        comp_str = "\n\t".join(comp_list)
        return variant_id + "\n\t" + comp_str

    __repr__ = __str__
