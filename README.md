# Variant Validation Report Generation (VARG)

*varg* is a simple tool that can be used to benchmark vcf-files against a truth-set of positive controls.

*varg* simply finds variants between two vcf-files, finds what variants that are common in the two files (with support for imprecise structural variants)
and aggregate statistics generated from comparisons between each common variant. The user can dynamically enter what fields and columns that should be compared between the vcf-files. *varg* supports multi-sample vcf-files.

# Installation

*varg* can be installed with pip

```console
pip install git+https://github.com/adrosenbaum/varg
```

# Usage

To compare two vcf-files, one vcf with positive controls TRUTH_VCF, with the vcf to be benchmarked BENCH_VCF run the command

```console
varg compare -t $TRUTH_VCF -v $BENCH_VCF
```

The samples that are compared between the vcf will default to the respective order of the samples in the vcf-files. The user can specify what samples that should be compared with the ```-m/--samples-map``` option e.g. ```-m child=sample_1,father=sample_2,mother=sample_3``` will compare the sample 'child' in the truth-set vcf with sample 'sample_1' in the benchmark-vcf, etc.

To control what fields are compared between the two vcf-files, the user must specify a .py file with the ```-f/--vcf-fields``` option. This will default to the file in varg/resources/compare_fields. In this file a constant COMPARE_FIELDS of python type dict must be declared. 
