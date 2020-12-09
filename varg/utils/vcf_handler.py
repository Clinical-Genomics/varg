import logging
import cyvcf2

LOG = logging.getLogger(__name__)

CI_PADDING = 500
MAX_PADDING = 3000


class VCFHandler(cyvcf2.VCF):
    """ Class to handle cyvcf2.VCF objects """

    def __init__(self, vcf_path):

        super(VCFHandler, self).__init__(vcf_path)
        self.file_path = vcf_path
        self.length = self._no_variants()
        self.not_found_variants = []

    def _reset(self):
        """Reset itereator"""
        self.close()
        super(VCFHandler, self).__init__(self.file_path)

    def _no_variants(self):
        LOG.info("Find number of records in %s", self.file_path)
        variant_no = 0
        for _ in self:
            variant_no += 1
        self._reset()
        return variant_no

    def intersection(self, vcf, samples_map=None):
        """ Finds intersection, i.e. common variants with another VCFHandler object"""
        LOG.info(
            "Find common variants between %s and %s", self.file_path, vcf.file_path
        )
        common_variants = 0
        samples_1 = self.samples
        samples_2 = vcf.samples
        samples_idx_map = None
        if samples_map:
            samples_idx_map = self._samples_map(samples_1, samples_2, samples_map)
        for variant in self:
            if variant.INFO.get("SVTYPE", None) is None:
                record = vcf.find_snv(variant)
            else:
                record = vcf.find_similar_sv(variant)
            if record is not None:
                yield (variant, record, samples_idx_map)
                common_variants += 1
            else:
                self.not_found_variants.append(variant)
        LOG.info("Found %d variant in common", common_variants)

    @staticmethod
    def _samples_map(samples_1, samples_2, samples_map):
        sample_1_idx = []
        sample_2_idx = []
        for sample_pair in samples_map:
            sample_1_idx.append(samples_1.index(sample_pair[0]))
            sample_2_idx.append(samples_2.index(sample_pair[1]))
        return (sample_1_idx, sample_2_idx)

    def find_snv(self, variant_record):
        """Given a cyvcf2 variant record, find a matching variant in vcf"""
        region_str = (
            f"{variant_record.CHROM}:{variant_record.POS}-{variant_record.POS + 1}"
        )
        for record in self(region_str):
            is_same = all(
                (
                    variant_record.CHROM.lower().strip("chr")
                    == record.CHROM.lower().strip("chr"),
                    variant_record.POS == record.POS,
                    variant_record.REF == record.REF,
                    variant_record.ALT == record.ALT,
                )
            )
            if is_same:
                return record
        return None

    def find_similar_sv(self, variant_record):
        """Given a cyvcf2 variant record of a SV, find a matching variant in vcf"""
        pos = variant_record.POS
        end = variant_record.INFO.get("END")
        if end is None:
            end = pos + 1
        type_1 = variant_record.INFO.get("SVTYPE")
        if type_1 is None:
            return None
        type_1 = type_1.upper()
        search_interval = self._find_search_interval(variant_record=variant_record)
        closest_match = None
        for hit in self(
            f"{variant_record.CHROM}:{pos-search_interval}-{pos+search_interval}"
        ):
            type_2 = hit.INFO.get("SVTYPE")
            if type_2 is None or hit.INFO.get("END") is None:
                continue
            type_2 = type_2.upper()
            if hit.POS < pos - search_interval or hit.POS > pos + search_interval:
                continue
            if type_1 in type_2 or type_2 in type_1:
                if closest_match is None:
                    closest_match = hit
                    continue
                else:
                    this_distance = abs(hit.POS - pos) + abs(hit.INFO["END"] - end)
                    match_distance = abs(closest_match.POS - pos) + abs(
                        closest_match.INFO["END"] - end
                    )
                    if this_distance <= match_distance:
                        closest_match = hit
        return closest_match

    @staticmethod
    def _find_search_interval(variant_record):
        """Given a variant, find an appropriate search interval, based on variant length"""
        length_prop = 0.1
        if variant_record.INFO.get("END"):
            variant_length = variant_record.INFO["END"] - variant_record.POS
        elif variant_record.INFO.get("SVLEN"):
            variant_length = abs(variant_record.INFO["SVLEN"])
        else:
            variant_length = 0
        interval = round(variant_length * length_prop)
        ci_interval = _find_ci(variant_record)

        if ci_interval is not None:
            if interval < ci_interval:
                interval = ci_interval + CI_PADDING
                return interval

        if interval > MAX_PADDING:
            interval = MAX_PADDING
        return interval


def _find_ci(variant_record):
    """Given a variant record, returns the largest CIPOS or CIEND if present"""
    intervals = []
    if variant_record.INFO.get("CIPOS") is not None:
        interval = abs(variant_record.INFO["CIPOS"][0])
        intervals.append(interval)
    if variant_record.INFO.get("CIEND") is not None:
        interval = abs(variant_record.INFO["CIEND"][-1])
        intervals.append(interval)
    if not intervals:
        return None
    return max(intervals)
