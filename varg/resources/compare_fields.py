class Genotype:
    """Make string representation of cyvcf2 genotype"""
    def __init__(self, li):
        self.alleles = li[:-1]
        self.phased = li[-1]
    def __str__(self):
        sep = "/|"[int(self.phased)]
        return sep.join("0123."[a] for a in self.alleles)
    __repr__ = __str__


# Conversion functions
get_score = lambda score: int(score.split(':')[-1])
get_alt_DP = lambda DP: [int(dp) if int(dp) >= 0 else None for dp in list(DP)]
get_alt_AD = lambda DP: [[int(i) if int(i) >= 0 else None for i in dp][-1] for dp in list(DP)]
get_GQ = lambda GQ: [int(gq[0]) if int(gq[0]) >= 0 else None for gq in GQ]
get_genotypes = lambda genotypes: [str(Genotype(gt)) for gt in genotypes]
get_qual = lambda qual: float(qual) if isinstance(qual, float) else str(qual)


# INFO_keys dictionary states what fields in the vcf that should be compared
# To add a field/fields that should be compared between two VCFs, add
#   NAME: {'type_conv': function, 'ID': (ID1,ID2), 'column': 'INFO'|FORMAT}
# Where NAME is a chosen name for the value, function a function that converts
# the value from cyvcf2 to something else, IDs are the name of the fields in the
# VCFs, these may be more than one, if the IDs in the two VCFs are different for
# The same measure. and column name, which is either of 'INFO' or 'FORMAT'
COMPARE_FIELDS = {
    'CHROM': {'type_conv': str, 'ID': ('CHROM',)},
    'POS': {'type_conv': int, 'ID': ('POS',)},
    'END': {'type_conv': int, 'ID': ('END',), 'column': 'INFO'},
    'RANK_SCORE': {'type_conv': get_score, 'ID': ('MutaccRankScore', 'RankScore'), 'column': 'INFO'},
    'TYPE': {'type_conv': str, 'ID': ('TYPE', 'SVTYPE', 'type',), 'column': 'INFO'},
    'DEPTH': {'type_conv': get_alt_DP, 'ID': ('DP',), 'column': 'FORMAT', 'rearrange': True},
    'ALT DEPTH': {'type_conv': get_alt_AD, 'ID': ('AD', 'AF',), 'column': 'FORMAT', 'rearrange': True},
    'GQ': {'type_conv': get_GQ, 'ID': ('GQ',), 'column': 'FORMAT', 'rearrange': True},
    'GENOTYPES': {'type_conv': get_genotypes, 'ID': ('GT',), 'rearrange': True},
    'QUAL': {'type_conv': float, 'ID': ('QUAL',)},
    'SV_LEN': {'type_conv': int, 'ID': ('SVLEN',), 'column': 'INFO'}
}
